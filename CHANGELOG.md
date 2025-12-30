# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2024-12-30

### 🔧 Bug Fixes
- **Network Exception Handling**: Added proper handling for network layer exceptions (ConnectionError, TimeoutError)
- **Retry Compatibility**: Network exceptions are now converted to standard exception types for better retry mechanism compatibility
- **Error Messages**: Improved error messages with more descriptive information for debugging

### 🧪 Testing
- Added comprehensive test suite for network exception handling
- Added demonstration script showing retry mechanism compatibility
- Fixed Hypothesis strategy syntax in version constraint tests
- Added PyYAML dependency for CI pipeline tests

### 📦 Dependencies
- Added `pyyaml>=6.0.0` for CI/CD pipeline testing

### 🛠 Technical Improvements
- All CRUD operations (GET, POST, PUT, DELETE) now properly handle network exceptions
- Exceptions are caught at the API layer and re-raised as standard Python exceptions
- Maintains backward compatibility while improving reliability

## [1.0.0] - 2024-12-30

### 🚀 Major Changes
- **BREAKING**: Dropped Python 2.7 support
- **NEW**: Added support for Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **NEW**: Modernized project structure with pyproject.toml
- **NEW**: Comprehensive test suite with property-based testing

### 🔒 Security Enhancements
- Updated `requests` from 2.24.0 to 2.32.5+ (fixes multiple CVEs)
- Updated `python-dateutil` from 2.8.1 to 2.9.0+
- Updated `certifi` from 2020.6.20 to 2025.11.12+ (latest certificates)
- Removed `six` dependency (Python 2.7 compatibility layer)
- SSL certificate validation enabled by default
- Added automated security scanning with bandit and safety

### 🛠 Technical Improvements
- Modernized class definitions (removed explicit `object` inheritance)
- Updated string formatting to use f-strings where appropriate
- Added type hints compatibility
- Modern exception handling with proper chaining
- Updated GitHub Actions to latest versions (v4/v5)
- Added comprehensive CI/CD pipeline with multi-OS testing

### 📦 Dependencies
- **Removed**: `six==1.15.0` (Python 2.7 compatibility)
- **Removed**: `appdirs==1.4.4` (unused)
- **Removed**: `packaging==20.4` (transitive)
- **Removed**: `pyparsing==2.4.7` (transitive)
- **Updated**: `requests>=2.32.0,<3.0.0` (was ==2.24.0)
- **Updated**: `python-dateutil>=2.8.2` (was ==2.8.1)
- **Updated**: `certifi>=2023.7.22` (was ==2020.6.20)
- **Added**: Development dependencies (pytest, hypothesis, black, flake8, mypy, bandit, safety)

### 🧪 Testing
- Added pytest-based test suite
- Added property-based testing with Hypothesis
- Added test coverage reporting
- Added CI testing across Python 3.8-3.12 and multiple OS
- Added security and code quality tests

### 📚 Documentation
- Updated README with modern installation instructions
- Added comprehensive API examples
- Added migration guide from original client
- Added security features documentation
- Added development setup instructions

### 🔄 Backward Compatibility
- **MAINTAINED**: All existing APIs remain compatible
- **MAINTAINED**: Same import structure (`from gophish import Gophish`)
- **MAINTAINED**: All model classes and methods unchanged
- **MAINTAINED**: setup.py for legacy tooling compatibility

### 🏗 Build System
- Added modern pyproject.toml configuration
- Updated package classifiers for Python 3.8-3.12
- Added proper build system requirements
- Configured modern packaging tools

## [0.5.1] - Original Version
- Last version of the original gophish client
- Supported Python 2.7 and 3.3+
- Basic functionality for Gophish API interaction