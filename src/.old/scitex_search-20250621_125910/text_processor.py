#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 16:20:00 (ywatanabe)"
# File: src/scitex_search/text_processor.py

"""
Text processing module for scientific documents.

This module provides functionality for cleaning, normalizing, and processing
scientific text documents for search and analysis purposes.
"""

import re
from typing import List, Dict, Any


class TextProcessor:
    """
    Text processor for scientific documents.
    
    Provides methods for cleaning, normalizing, and extracting information
    from scientific texts including LaTeX content.
    """
    
    def __init__(self):
        """Initialize TextProcessor with default settings."""
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        return cleaned
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text to lowercase for consistent processing.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text string
        """
        if not text:
            return ""
        
        return text.lower()
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text by removing stop words.
        
        Args:
            text: Input text
            min_length: Minimum keyword length
            
        Returns:
            List of extracted keywords
        """
        if not text:
            return []
        
        # Normalize and split into words
        normalized = self.normalize_text(text)
        words = re.findall(r'\b[a-zA-Z]+\b', normalized)
        
        # Filter out stop words and short words
        keywords = [
            word for word in words 
            if word not in self.stop_words and len(word) >= min_length
        ]
        
        return list(set(keywords))  # Remove duplicates
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract common sections from scientific documents.
        
        Args:
            text: Input document text
            
        Returns:
            Dictionary mapping section names to content
        """
        sections = {}
        
        # Common scientific paper sections
        section_patterns = {
            'abstract': r'(?i)abstract\s*\n(.*?)(?=\n\s*(?:introduction|keywords|1\.|$))',
            'introduction': r'(?i)introduction\s*\n(.*?)(?=\n\s*(?:method|related|2\.|$))',
            'conclusion': r'(?i)conclusion\s*\n(.*?)(?=\n\s*(?:reference|acknowledgment|$))'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = self.clean_text(match.group(1))
        
        return sections
    
    def process_document(self, document: str) -> Dict[str, Any]:
        """
        Process a complete scientific document.
        
        Args:
            document: Full document text
            
        Returns:
            Dictionary containing processed document information
        """
        cleaned_text = self.clean_text(document)
        keywords = self.extract_keywords(cleaned_text)
        sections = self.extract_sections(document)
        
        return {
            'cleaned_text': cleaned_text,
            'keywords': keywords,
            'sections': sections,
            'word_count': len(cleaned_text.split()),
            'char_count': len(cleaned_text)
        }

# EOF