# CONTRIBUTING.md

## Contributing to Secure File Sharing System

Thank you for interest in contributing! Here's how you can help.

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/secure-file-sharing-system.git`
3. Create a branch: `git checkout -b feature/YourFeature`
4. Make changes and commit: `git commit -m "Add YourFeature"`
5. Push: `git push origin feature/YourFeature`
6. Open a Pull Request

### Code Style

- Follow PEP 8 conventions
- Use type hints where possible
- Document functions with docstrings
- Use meaningful variable names

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Test specific module
pytest tests/test_crypto.py -v
```

### Areas for Contribution

#### Code
- Bug fixes
- Performance optimizations
- New steganography methods (DCT, DFT, etc.)
- Additional encryption algorithms
- Better error handling

#### Documentation
- More examples
- API documentation improvements
- Tutorial guides
- Video tutorials

#### Testing
- More test cases
- Edge case testing
- Performance benchmarks
- Security audits

#### Features
- GUI interface
- Cloud storage integration
- Multi-image support
- Batch processing enhancements

### Reporting Issues

When reporting bugs, include:
- Python version
- Operating system
- Error message (full stack trace)
- Steps to reproduce
- Expected vs actual behavior

### Security Reports

For security vulnerabilities, email: security@example.com
(Do not create public issues for security vulnerabilities)

### Pull Request Process

1. Ensure tests pass: `pytest`
2. Update documentation if needed
3. Add to CHANGELOG.md
4. Follow code style guidelines
5. Request review from maintainers
6. Address feedback
7. Merge after approval

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Format code
black *.py

# Check style
flake8 *.py

# Run tests
pytest -v --cov
```

### Commit Message Guidelines

```
[TYPE] Brief description

More detailed explanation if needed.

Fixes #ISSUE_NUMBER (if applicable)
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`

### Questions?

Open a discussion or issue on GitHub!

Thank you for contributing! 🎉
