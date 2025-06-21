#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2025-05-22 15:39:00 (ywatanabe)"
# File: __init__.py

"""
SciTeX-Scholar: A Python package for scientific text search and analysis.

Functionalities:
  - Scientific text processing and search
  - LaTeX document analysis
  - Research paper content extraction

Dependencies:
  - packages: (to be determined based on requirements)

IO:
  - input-files: Scientific documents, LaTeX files
  - output-files: Processed search results, analysis reports
"""

__version__ = "0.1.0"
__author__ = "Yusuke Watanabe"
__email__ = "ywatanabe@alumni.u-tokyo.ac.jp"

# Package imports
from .text_processor import TextProcessor
from .search_engine import SearchEngine
from .latex_parser import LaTeXParser

__all__ = ['TextProcessor', 'SearchEngine', 'LaTeXParser']

# EOF