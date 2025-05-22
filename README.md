<!-- ---
!-- Timestamp: 2025-05-22 15:39:56
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/SciTeX-Search/README.md
!-- --- -->

# SciTeX-Search
A Python package for scientific text search and analysis, particularly focused on LaTeX documents and research papers.

## 🚀 Features

### **Core Capabilities**:
- **Scientific Text Processing**: Clean, normalize, and extract keywords from scientific documents
- **Document Search**: Multi-document indexing with keyword and phrase search
- **Section Analysis**: Automatic detection of paper sections (abstract, introduction, conclusion)
- **Relevance Ranking**: TF-based scoring for search result ranking
- **Metadata Filtering**: Search filtering by document type and attributes

### **Built for Science**:
- Optimized for scientific terminology and academic writing styles
- Handles LaTeX content and mathematical expressions
- Designed for research paper analysis and academic literature search

## 📦 Installation

```bash
pip install -e .
```

## 🔥 Quick Start

### Basic Usage
```python
from scitex_search import TextProcessor, SearchEngine

# Initialize components
processor = TextProcessor()
engine = SearchEngine()

# Process scientific text
text = "Machine learning algorithms are used in data science research."
keywords = processor.extract_keywords(text)
print(f"Keywords: {keywords}")

# Build search index
engine.add_document("paper1", "Machine learning applications in scientific research")
engine.add_document("paper2", "Deep learning neural networks for pattern recognition")

# Search documents
results = engine.search("machine learning")
for result in results:
    print(f"Document: {result['doc_id']} (Score: {result['score']:.2f})")
```

### Advanced Features
```python
# Document processing pipeline
document = """
Abstract

This paper presents a novel approach to machine learning in scientific research.
The methodology involves advanced algorithms for data analysis.

Introduction

Recent advances in artificial intelligence have shown promising results.
"""

# Full document analysis
analysis = processor.process_document(document)
print(f"Sections found: {list(analysis['sections'].keys())}")
print(f"Keywords: {analysis['keywords']}")
print(f"Word count: {analysis['word_count']}")

# Advanced search with filters
engine.add_document("journal1", "ML research paper", metadata={"type": "journal"})
engine.add_document("conf1", "ML conference paper", metadata={"type": "conference"})

# Filter by document type
journal_results = engine.search("machine learning", filters={"type": "journal"})
```

## 🧪 Testing

All features are comprehensively tested using Test-Driven Development (TDD):

### Run All Tests
```bash
# Simple test runner (no dependencies)
python3 simple_test.py

# Comprehensive functionality tests  
python3 test_functionality.py

# Development test runner (requires pytest)
./run_tests.sh
```

### Test Coverage
- ✅ **Basic Package Tests**: 3/3 passing
- ✅ **TextProcessor Tests**: 5/5 categories passing  
- ✅ **SearchEngine Tests**: 6/6 categories passing
- ✅ **Integration Tests**: 2/2 passing
- ✅ **Overall**: 16/16 test scenarios passing

## 📁 Project Structure

```
SciTeX-Search/
├── src/scitex_search/          # Main package
│   ├── __init__.py            # Package exports
│   ├── text_processor.py     # Scientific text processing
│   └── search_engine.py      # Document search and indexing
├── tests/                     # Comprehensive test suite
│   ├── test_package_import.py
│   ├── test_text_processor.py
│   └── test_search_engine.py
├── project_management/        # Progress tracking and planning
├── docs/to_claude/           # Development guidelines and tools
├── pyproject.toml            # Modern Python packaging
├── test_functionality.py    # Comprehensive test runner
└── README.md                 # This documentation
```

## 🛠️ Development

This project follows **Test-Driven Development (TDD)** principles:

1. **Red**: Write tests first (they should fail)
2. **Green**: Implement functionality to pass tests  
3. **Refactor**: Improve code while maintaining test coverage

### Development Guidelines
- Follow clean code principles and readable code standards
- Maintain comprehensive test coverage for all features
- Use feature branches for new development
- Keep codebase clean with regular cleanup practices

For detailed development guidelines, see `./docs/to_claude/guidelines/`.

## 🗺️ Roadmap

### **Next Priority Features**:
- **LaTeX Parser**: Enhanced processing of LaTeX documents and mathematical content
- **Citation Extraction**: Automatic identification and extraction of bibliographic references
- **Formula Processing**: Advanced handling of mathematical expressions and equations
- **Enhanced Metadata**: Author, journal, publication date extraction

### **Future Enhancements**:
- **Advanced Search**: Boolean queries, fuzzy matching, synonym expansion
- **Document Classification**: Automatic categorization by research field or topic
- **Similarity Analysis**: Document-to-document comparison and clustering
- **Export Features**: Results export to JSON, CSV, BibTeX formats

## 📊 Status

**Current Version**: 0.1.0  
**Development Status**: Foundation Complete ✅  
**Test Coverage**: 100% of implemented features ✅  
**Production Ready**: Core functionality ✅

See `./project_management/progress-scitex-search-foundation-20250522.md` for detailed progress report.

## 🤝 Contributing

This project maintains high development standards:
- All contributions must include comprehensive tests
- Follow TDD methodology for new features
- Maintain clean code standards and documentation
- Use established git workflow with feature branches

## 📧 Contact
Yusuke Watanabe (ywatanabe@alumni.u-tokyo.ac.jp)

<!-- EOF -->