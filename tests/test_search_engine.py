#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 16:15:00 (ywatanabe)"
# File: tests/test_search_engine.py

"""
Test module for search engine functionality.

This module tests the core search capabilities including
keyword search, phrase matching, and document ranking.
"""

import pytest
import sys
sys.path.insert(0, './src')


def test_search_engine_import():
    """Test that search engine module can be imported."""
    try:
        from scitex_search.search_engine import SearchEngine
    except ImportError:
        pytest.fail("Failed to import SearchEngine from scitex_search.search_engine")


def test_search_engine_initialization():
    """Test SearchEngine can be initialized."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    assert engine is not None
    assert hasattr(engine, 'search')
    assert hasattr(engine, 'add_document')


def test_add_document():
    """Test adding documents to search index."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    
    doc_id = "doc1"
    content = "This is a sample scientific document about machine learning."
    
    result = engine.add_document(doc_id, content)
    assert result is True
    assert doc_id in engine.documents


def test_keyword_search():
    """Test basic keyword search functionality."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    
    # Add test documents
    engine.add_document("doc1", "Machine learning algorithms for data analysis")
    engine.add_document("doc2", "Deep learning neural networks in AI research")
    engine.add_document("doc3", "Statistical methods in scientific computing")
    
    # Search for keywords
    results = engine.search("machine learning")
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert any(result['doc_id'] == "doc1" for result in results)


def test_phrase_search():
    """Test exact phrase search functionality."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    
    # Add test documents
    engine.add_document("doc1", "machine learning algorithms")
    engine.add_document("doc2", "learning machine algorithms")
    
    # Search for exact phrase
    results = engine.search("machine learning", exact_phrase=True)
    
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]['doc_id'] == "doc1"


def test_search_scoring():
    """Test search result scoring and ranking."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    
    # Add documents with different relevance
    engine.add_document("doc1", "machine learning machine learning algorithms")
    engine.add_document("doc2", "machine learning in science")
    engine.add_document("doc3", "algorithms and methods")
    
    results = engine.search("machine learning")
    
    assert len(results) >= 2
    # Check that results are scored
    assert all('score' in result for result in results)
    # Check that more relevant document scores higher
    assert results[0]['score'] >= results[1]['score']


def test_search_with_filters():
    """Test search with document type filters."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    
    # Add documents with metadata
    engine.add_document("doc1", "machine learning paper", metadata={"type": "paper"})
    engine.add_document("doc2", "machine learning book", metadata={"type": "book"})
    
    # Search with filter
    results = engine.search("machine learning", filters={"type": "paper"})
    
    assert len(results) == 1
    assert results[0]['doc_id'] == "doc1"


def test_empty_search():
    """Test handling of empty search queries."""
    from scitex_search.search_engine import SearchEngine
    
    engine = SearchEngine()
    engine.add_document("doc1", "sample content")
    
    # Test empty query
    results = engine.search("")
    assert isinstance(results, list)
    assert len(results) == 0
    
    # Test None query
    results = engine.search(None)
    assert isinstance(results, list)
    assert len(results) == 0


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])

# EOF