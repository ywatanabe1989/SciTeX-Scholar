#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-01-06 03:05:00 (ywatanabe)"
# File: src/scitex_scholar/paper_acquisition.py

"""
Paper acquisition module for automated literature search and download.

This module provides functionality to search and download scientific papers
from various sources including PubMed, arXiv, bioRxiv, and more.
"""

import asyncio
import aiohttp
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import re
from urllib.parse import quote_plus
import time

logger = logging.getLogger(__name__)


class PaperMetadata:
    """Structured metadata for a scientific paper."""
    
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.authors = kwargs.get('authors', [])
        self.abstract = kwargs.get('abstract', '')
        self.year = kwargs.get('year', '')
        self.doi = kwargs.get('doi', '')
        self.pmid = kwargs.get('pmid', '')
        self.arxiv_id = kwargs.get('arxiv_id', '')
        self.journal = kwargs.get('journal', '')
        self.keywords = kwargs.get('keywords', [])
        self.pdf_url = kwargs.get('pdf_url', '')
        self.source = kwargs.get('source', '')
        self.citation_count = kwargs.get('citation_count', 0)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'year': self.year,
            'doi': self.doi,
            'pmid': self.pmid,
            'arxiv_id': self.arxiv_id,
            'journal': self.journal,
            'keywords': self.keywords,
            'pdf_url': self.pdf_url,
            'source': self.source,
            'citation_count': self.citation_count
        }


class PaperAcquisition:
    """Unified interface for paper search and download from multiple sources."""
    
    def __init__(self, download_dir: Optional[Path] = None, email: Optional[str] = None):
        """
        Initialize paper acquisition system.
        
        Args:
            download_dir: Directory to save downloaded PDFs
            email: Email for API compliance (required for some services)
        """
        self.download_dir = download_dir or Path("./downloaded_papers")
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.email = email or "research@example.com"
        
        # API endpoints
        self.pubmed_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.arxiv_base = "http://export.arxiv.org/api/query"
        self.crossref_base = "https://api.crossref.org/works"
        self.unpaywall_base = "https://api.unpaywall.org/v2"
        self.biorxiv_base = "https://api.biorxiv.org/details/biorxiv"
        
        # Rate limiting
        self.rate_limits = {
            'pubmed': 0.34,  # ~3 requests/second
            'arxiv': 0.5,    # 2 requests/second
            'crossref': 0.1, # 10 requests/second
            'unpaywall': 0.1,
            'biorxiv': 0.5
        }
        self.last_request = {}
    
    async def search(self, 
                    query: str,
                    sources: List[str] = None,
                    max_results: int = 20,
                    start_year: Optional[int] = None,
                    end_year: Optional[int] = None) -> List[PaperMetadata]:
        """
        Search for papers across multiple sources.
        
        Args:
            query: Search query
            sources: List of sources to search (default: all)
            max_results: Maximum results per source
            start_year: Filter by start year
            end_year: Filter by end year
            
        Returns:
            List of paper metadata
        """
        sources = sources or ['pubmed', 'arxiv', 'biorxiv']
        all_results = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            if 'pubmed' in sources:
                tasks.append(self._search_pubmed(session, query, max_results, start_year, end_year))
            
            if 'arxiv' in sources:
                tasks.append(self._search_arxiv(session, query, max_results))
            
            if 'biorxiv' in sources:
                tasks.append(self._search_biorxiv(session, query, max_results))
            
            # Execute searches in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Search error: {result}")
                else:
                    all_results.extend(result)
        
        # Remove duplicates based on title similarity
        unique_results = self._deduplicate_results(all_results)
        
        return unique_results
    
    async def _search_pubmed(self, 
                           session: aiohttp.ClientSession,
                           query: str,
                           max_results: int,
                           start_year: Optional[int],
                           end_year: Optional[int]) -> List[PaperMetadata]:
        """Search PubMed/PMC."""
        await self._rate_limit('pubmed')
        
        # Build query with date filters
        date_filter = ""
        if start_year or end_year:
            start = start_year or 1900
            end = end_year or datetime.now().year
            date_filter = f" AND {start}:{end}[pdat]"
        
        search_query = quote_plus(query + date_filter)
        
        # Search for IDs
        search_url = f"{self.pubmed_base}/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': search_query,
            'retmax': max_results,
            'retmode': 'json',
            'email': self.email
        }
        
        async with session.get(search_url, params=params) as resp:
            data = await resp.json()
            pmids = data.get('esearchresult', {}).get('idlist', [])
        
        if not pmids:
            return []
        
        # Fetch details
        await self._rate_limit('pubmed')
        
        fetch_url = f"{self.pubmed_base}/efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml',
            'email': self.email
        }
        
        async with session.get(fetch_url, params=params) as resp:
            xml_data = await resp.text()
        
        # Parse results
        papers = []
        root = ET.fromstring(xml_data)
        
        for article in root.findall('.//PubmedArticle'):
            try:
                # Extract metadata
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else ''
                
                # Authors
                authors = []
                for author in article.findall('.//Author'):
                    lastname = author.find('LastName')
                    forename = author.find('ForeName')
                    if lastname is not None:
                        name = lastname.text
                        if forename is not None:
                            name = f"{forename.text} {name}"
                        authors.append(name)
                
                # Abstract
                abstract_texts = []
                for abstract in article.findall('.//AbstractText'):
                    if abstract.text:
                        abstract_texts.append(abstract.text)
                abstract = ' '.join(abstract_texts)
                
                # Year
                year_elem = article.find('.//PubDate/Year')
                year = year_elem.text if year_elem is not None else ''
                
                # Journal
                journal_elem = article.find('.//Journal/Title')
                journal = journal_elem.text if journal_elem is not None else ''
                
                # PMID
                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else ''
                
                # DOI
                doi = ''
                for id_elem in article.findall('.//ArticleId'):
                    if id_elem.get('IdType') == 'doi':
                        doi = id_elem.text
                        break
                
                # Keywords
                keywords = []
                for kw in article.findall('.//Keyword'):
                    if kw.text:
                        keywords.append(kw.text)
                
                papers.append(PaperMetadata(
                    title=title,
                    authors=authors[:10],  # Limit authors
                    abstract=abstract,
                    year=year,
                    doi=doi,
                    pmid=pmid,
                    journal=journal,
                    keywords=keywords,
                    source='pubmed'
                ))
                
            except Exception as e:
                logger.error(f"Error parsing PubMed article: {e}")
                continue
        
        return papers
    
    async def _search_arxiv(self,
                          session: aiohttp.ClientSession,
                          query: str,
                          max_results: int) -> List[PaperMetadata]:
        """Search arXiv."""
        await self._rate_limit('arxiv')
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        async with session.get(self.arxiv_base, params=params) as resp:
            xml_data = await resp.text()
        
        # Parse results
        papers = []
        root = ET.fromstring(xml_data)
        
        # Handle namespaces
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            try:
                # Title
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip() if title_elem is not None else ''
                
                # Authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                
                # Abstract
                summary_elem = entry.find('atom:summary', ns)
                abstract = summary_elem.text.strip() if summary_elem is not None else ''
                
                # Published date
                published_elem = entry.find('atom:published', ns)
                year = ''
                if published_elem is not None:
                    year = published_elem.text[:4]
                
                # arXiv ID
                id_elem = entry.find('atom:id', ns)
                arxiv_id = ''
                pdf_url = ''
                if id_elem is not None:
                    arxiv_id = id_elem.text.split('/')[-1]
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                
                # Categories as keywords
                keywords = []
                for cat in entry.findall('atom:category', ns):
                    term = cat.get('term')
                    if term:
                        keywords.append(term)
                
                papers.append(PaperMetadata(
                    title=title,
                    authors=authors[:10],
                    abstract=abstract,
                    year=year,
                    arxiv_id=arxiv_id,
                    keywords=keywords,
                    pdf_url=pdf_url,
                    source='arxiv'
                ))
                
            except Exception as e:
                logger.error(f"Error parsing arXiv entry: {e}")
                continue
        
        return papers
    
    async def _search_biorxiv(self,
                            session: aiohttp.ClientSession,
                            query: str,
                            max_results: int) -> List[PaperMetadata]:
        """Search bioRxiv."""
        await self._rate_limit('biorxiv')
        
        # bioRxiv API is limited, using basic search
        # Note: This is a simplified implementation
        # Full implementation would require more sophisticated API usage
        
        papers = []
        logger.info("bioRxiv search is simplified in this implementation")
        
        return papers
    
    async def download_paper(self, 
                           paper: PaperMetadata,
                           filename: Optional[str] = None) -> Optional[Path]:
        """
        Download a paper PDF if available.
        
        Args:
            paper: Paper metadata
            filename: Custom filename (default: generated from title)
            
        Returns:
            Path to downloaded file or None
        """
        if not paper.pdf_url and paper.arxiv_id:
            paper.pdf_url = f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"
        
        if not paper.pdf_url:
            # Try to find open access version
            paper.pdf_url = await self._find_open_access_pdf(paper)
        
        if not paper.pdf_url:
            logger.warning(f"No PDF URL available for: {paper.title}")
            return None
        
        # Generate filename
        if not filename:
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', paper.title)
            clean_title = re.sub(r'[-\s]+', '_', clean_title)[:100]
            filename = f"{clean_title}_{paper.source}_{paper.arxiv_id or paper.pmid or 'unknown'}.pdf"
        
        filepath = self.download_dir / filename
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(paper.pdf_url) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        filepath.write_bytes(content)
                        logger.info(f"Downloaded: {filepath}")
                        return filepath
                    else:
                        logger.error(f"Failed to download (status {resp.status}): {paper.pdf_url}")
                        return None
                        
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None
    
    async def _find_open_access_pdf(self, paper: PaperMetadata) -> Optional[str]:
        """Try to find open access PDF using Unpaywall."""
        if not paper.doi:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.unpaywall_base}/{paper.doi}"
            params = {'email': self.email}
            
            try:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        best_oa = data.get('best_oa_location')
                        if best_oa and best_oa.get('url_for_pdf'):
                            return best_oa['url_for_pdf']
            except Exception as e:
                logger.debug(f"Unpaywall lookup failed: {e}")
        
        return None
    
    async def _rate_limit(self, source: str):
        """Implement rate limiting for API calls."""
        if source in self.last_request:
            elapsed = time.time() - self.last_request[source]
            wait_time = self.rate_limits.get(source, 0.1) - elapsed
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.last_request[source] = time.time()
    
    def _deduplicate_results(self, papers: List[PaperMetadata]) -> List[PaperMetadata]:
        """Remove duplicate papers based on title similarity."""
        unique_papers = []
        seen_titles = set()
        
        for paper in papers:
            # Normalize title for comparison
            normalized = re.sub(r'[^\w\s]', '', paper.title.lower())
            normalized = ' '.join(normalized.split())
            
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique_papers.append(paper)
        
        return unique_papers
    
    async def batch_download(self,
                           papers: List[PaperMetadata],
                           max_concurrent: int = 3) -> Dict[str, Path]:
        """
        Download multiple papers concurrently.
        
        Args:
            papers: List of papers to download
            max_concurrent: Maximum concurrent downloads
            
        Returns:
            Dictionary mapping paper titles to file paths
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def download_with_semaphore(paper):
            async with semaphore:
                path = await self.download_paper(paper)
                return (paper.title, path)
        
        results = await asyncio.gather(
            *[download_with_semaphore(p) for p in papers],
            return_exceptions=True
        )
        
        downloaded = {}
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Download error: {result}")
            elif result[1] is not None:
                downloaded[result[0]] = result[1]
        
        return downloaded


# Convenience functions
async def search_papers(query: str, **kwargs) -> List[PaperMetadata]:
    """Quick search function."""
    acquisition = PaperAcquisition()
    return await acquisition.search(query, **kwargs)


async def download_papers(papers: List[PaperMetadata], download_dir: Path = None) -> Dict[str, Path]:
    """Quick download function."""
    acquisition = PaperAcquisition(download_dir=download_dir)
    return await acquisition.batch_download(papers)


# EOF