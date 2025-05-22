#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 16:15:00 (ywatanabe)"
# File: tests/test_text_processor.py

"""
Test module for text processing functionality.

This module tests the core text processing capabilities including
text cleaning, normalization, and preprocessing for scientific documents.
"""

import pytest
import sys
sys.path.insert(0, './src')


def test_text_processor_import():
    """Test that text processor module can be imported."""
    try:
        from scitex_search.text_processor import TextProcessor
    except ImportError:
        pytest.fail("Failed to import TextProcessor from scitex_search.text_processor")


def test_text_processor_initialization():
    """Test TextProcessor can be initialized with default settings."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    assert processor is not None
    assert hasattr(processor, 'clean_text')
    assert hasattr(processor, 'normalize_text')


def test_clean_text_basic():
    """Test basic text cleaning functionality."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    
    # Test basic cleaning
    input_text = "  Hello   World!  \n\n  "
    expected = "Hello World!"
    result = processor.clean_text(input_text)
    assert result == expected


def test_clean_text_scientific_content():
    """Test cleaning of scientific text with special characters."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    
    # Test scientific content cleaning
    input_text = "The equation $E = mc^2$ shows the relationship."
    result = processor.clean_text(input_text)
    assert "E = mc^2" in result
    assert len(result) > 0


def test_normalize_text():
    """Test text normalization for consistent processing."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    
    # Test case normalization
    input_text = "UPPERCASE and lowercase TEXT"
    result = processor.normalize_text(input_text)
    assert result.islower()
    assert "uppercase" in result
    assert "lowercase" in result


def test_extract_keywords():
    """Test keyword extraction from scientific text."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    
    input_text = "Machine learning algorithms are used in data science research."
    keywords = processor.extract_keywords(input_text)
    
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert any("machine" in kw.lower() for kw in keywords)
    assert any("learning" in kw.lower() for kw in keywords)


def test_process_scientific_document():
    """Test processing a complete scientific document."""
    from scitex_search.text_processor import TextProcessor
    
    processor = TextProcessor()
    
    document = """
    Abstract
    
    This paper presents a novel approach to machine learning in scientific research.
    The methodology involves advanced algorithms for data analysis.
    
    Introduction
    
    Recent advances in artificial intelligence have shown promising results.
    """
    
    result = processor.process_document(document)
    
    assert isinstance(result, dict)
    assert 'cleaned_text' in result
    assert 'keywords' in result
    assert 'sections' in result
    assert len(result['cleaned_text']) > 0


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])

# EOF