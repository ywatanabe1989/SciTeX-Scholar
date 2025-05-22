#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 15:40:00 (ywatanabe)"
# File: tests/test_package_import.py

"""
Test basic package import functionality.

This test verifies that the SciTeX-Search package can be imported correctly
and that basic package metadata is accessible.
"""

import pytest


def test_package_import():
    """Test that the scitex_search package can be imported."""
    try:
        import sys
        sys.path.insert(0, './src')
        import scitex_search
    except ImportError:
        pytest.fail("Failed to import scitex_search package")


def test_package_version():
    """Test that package version is accessible."""
    import sys
    sys.path.insert(0, './src')
    import scitex_search
    
    assert hasattr(scitex_search, '__version__')
    assert isinstance(scitex_search.__version__, str)
    assert len(scitex_search.__version__) > 0


def test_package_metadata():
    """Test that package metadata is properly set."""
    import sys
    sys.path.insert(0, './src')
    import scitex_search
    
    # Test required metadata attributes
    assert hasattr(scitex_search, '__author__')
    assert hasattr(scitex_search, '__email__')
    assert scitex_search.__author__ == "Yusuke Watanabe"
    assert scitex_search.__email__ == "ywatanabe@alumni.u-tokyo.ac.jp"


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__)])

# EOF