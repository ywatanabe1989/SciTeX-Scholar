#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 16:25:00 (ywatanabe)"
# File: test_functionality.py

"""
Comprehensive test runner for SciTeX-Search functionality.

This script runs tests for the core functionality without requiring pytest.
"""

import sys
import traceback
sys.path.insert(0, './src')

def test_text_processor():
    """Test TextProcessor functionality."""
    print("Testing TextProcessor...")
    
    from scitex_search.text_processor import TextProcessor
    processor = TextProcessor()
    
    # Test initialization
    assert processor is not None
    assert hasattr(processor, 'clean_text')
    assert hasattr(processor, 'normalize_text')
    print("  ✓ TextProcessor initialization")
    
    # Test text cleaning
    result = processor.clean_text("  Hello   World!  \n\n  ")
    assert result == "Hello World!"
    print("  ✓ Text cleaning")
    
    # Test normalization
    result = processor.normalize_text("UPPERCASE and lowercase TEXT")
    assert result == "uppercase and lowercase text"
    print("  ✓ Text normalization")
    
    # Test keyword extraction
    keywords = processor.extract_keywords("Machine learning algorithms are used in data science research.")
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert any("machine" in kw.lower() for kw in keywords)
    print("  ✓ Keyword extraction")
    
    # Test document processing
    document = """
    Abstract
    
    This paper presents a novel approach to machine learning in scientific research.
    The methodology involves advanced algorithms for data analysis.
    """
    result = processor.process_document(document)
    assert isinstance(result, dict)
    assert 'cleaned_text' in result
    assert 'keywords' in result
    assert 'sections' in result
    print("  ✓ Document processing")

def test_search_engine():
    """Test SearchEngine functionality."""
    print("Testing SearchEngine...")
    
    from scitex_search.search_engine import SearchEngine
    engine = SearchEngine()
    
    # Test initialization
    assert engine is not None
    assert hasattr(engine, 'search')
    assert hasattr(engine, 'add_document')
    print("  ✓ SearchEngine initialization")
    
    # Test adding documents
    result = engine.add_document("doc1", "Machine learning algorithms for data analysis")
    assert result is True
    assert "doc1" in engine.documents
    print("  ✓ Document addition")
    
    # Add more documents for search testing
    engine.add_document("doc2", "Deep learning neural networks in AI research")
    engine.add_document("doc3", "Statistical methods in scientific computing")
    
    # Test keyword search
    results = engine.search("machine learning")
    assert isinstance(results, list)
    assert len(results) > 0
    assert any(result['doc_id'] == "doc1" for result in results)
    print("  ✓ Keyword search")
    
    # Test phrase search
    engine.add_document("doc4", "machine learning algorithms")
    engine.add_document("doc5", "learning machine algorithms")
    results = engine.search("machine learning", exact_phrase=True)
    assert isinstance(results, list)
    assert len(results) >= 1
    print("  ✓ Phrase search")
    
    # Test search with filters
    engine.add_document("doc6", "machine learning paper", metadata={"type": "paper"})
    engine.add_document("doc7", "machine learning book", metadata={"type": "book"})
    results = engine.search("machine learning", filters={"type": "paper"})
    assert len(results) >= 1
    assert any(result['doc_id'] == "doc6" for result in results)
    print("  ✓ Filtered search")
    
    # Test empty search
    results = engine.search("")
    assert isinstance(results, list)
    assert len(results) == 0
    print("  ✓ Empty search handling")

def test_integration():
    """Test integration between components."""
    print("Testing Integration...")
    
    from scitex_search import TextProcessor, SearchEngine
    
    # Test package imports
    processor = TextProcessor()
    engine = SearchEngine()
    assert processor is not None
    assert engine is not None
    print("  ✓ Package imports")
    
    # Test workflow: process document then search
    documents = [
        ("paper1", "Machine learning applications in scientific research and data analysis"),
        ("paper2", "Deep learning neural networks for pattern recognition"),
        ("paper3", "Statistical methods for scientific computing and analysis")
    ]
    
    # Add processed documents to search engine
    for doc_id, content in documents:
        processed = processor.process_document(content)
        engine.add_document(doc_id, content)
    
    # Search and verify
    results = engine.search("machine learning scientific")
    assert len(results) > 0
    print("  ✓ Full workflow integration")

def main():
    """Run all tests."""
    print("Running SciTeX-Search functionality tests...")
    print("=" * 50)
    
    tests = [
        test_text_processor,
        test_search_engine,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
            print(f"✓ {test.__name__} PASSED")
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            traceback.print_exc()
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

# EOF