#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 15:45:00 (ywatanabe)"
# File: simple_test.py

"""
Simple test runner for basic package verification.

This script runs basic tests without requiring pytest installation.
"""

import sys
import os

# Add source directory to path
sys.path.insert(0, './src')

def test_package_import():
    """Test that the scitex_search package can be imported."""
    try:
        import scitex_search
        print("✓ Package import test passed")
        return True
    except ImportError as e:
        print(f"✗ Package import test failed: {e}")
        return False

def test_package_version():
    """Test that package version is accessible."""
    try:
        import scitex_search
        assert hasattr(scitex_search, '__version__')
        assert isinstance(scitex_search.__version__, str)
        assert len(scitex_search.__version__) > 0
        print(f"✓ Package version test passed: {scitex_search.__version__}")
        return True
    except (AssertionError, ImportError) as e:
        print(f"✗ Package version test failed: {e}")
        return False

def test_package_metadata():
    """Test that package metadata is properly set."""
    try:
        import scitex_search
        assert hasattr(scitex_search, '__author__')
        assert hasattr(scitex_search, '__email__')
        assert scitex_search.__author__ == "Yusuke Watanabe"
        assert scitex_search.__email__ == "ywatanabe@alumni.u-tokyo.ac.jp"
        print(f"✓ Package metadata test passed: {scitex_search.__author__}")
        return True
    except (AssertionError, ImportError) as e:
        print(f"✗ Package metadata test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running basic package tests...")
    print("-" * 40)
    
    tests = [
        test_package_import,
        test_package_version,
        test_package_metadata,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("-" * 40)
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