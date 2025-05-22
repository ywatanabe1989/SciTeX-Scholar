<!-- ---
!-- Timestamp: 2025-05-22 15:39:56
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/SciTeX-Search/README.md
!-- --- -->

# SciTeX-Search
A Python package for scientific text search and analysis, particularly focused on LaTeX documents and research papers.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import scitex_search

# Package version and info
print(f"Version: {scitex_search.__version__}")
print(f"Author: {scitex_search.__author__}")
```

## Testing

Run tests using the simple test runner:

```bash
python3 simple_test.py
```

Or use the comprehensive test runner (requires pytest):

```bash
./run_tests.sh
```

## Project Structure

```
SciTeX-Search/
├── src/
│   └── scitex_search/          # Main package
│       └── __init__.py
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_package_import.py
├── docs/                       # Documentation and guidelines
├── pyproject.toml             # Package configuration
├── run_tests.sh               # Test runner script
└── README.md                  # This file
```

## Development

This project follows Test-Driven Development (TDD) principles:

1. Write tests first
2. Implement functionality to pass tests
3. Refactor and improve

For detailed development guidelines, see `./docs/to_claude/guidelines/`.

## Contact
Yusuke Watanabe (ywatanabe@alumni.u-tokyo.ac.jp)

<!-- EOF -->