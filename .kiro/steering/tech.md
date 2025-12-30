# Technology Stack

## Build System
- **Package Manager**: setuptools (traditional Python packaging)
- **Configuration**: setup.py with setup.cfg for metadata
- **Distribution**: PyPI package distribution

## Core Dependencies
- **HTTP Client**: requests - for API communication
- **Date Handling**: python-dateutil - for ISO 8601 date parsing
- **HTTP/SSL Support**: certifi, urllib3, chardet, idna
- **Utilities**: appdirs - application directories

## Removed Dependencies (Python 2.7 compatibility)
- **six** - No longer needed with Python 3.8+ only support

## Python Support
- Python 3.8+ (modern Python versions only)
- No legacy Python 2.7 compatibility required

## Architecture Patterns
- **Client-Server**: REST API client library
- **Object-Oriented**: Model-based approach with inheritance
- **Factory Pattern**: Model parsing from JSON responses
- **Composition**: Main Gophish class composes API endpoint classes

## Common Commands

### Installation
```bash
pip install gophish
```

### Development Setup
```bash
# Install in development mode
pip install -e .

# Install from source
python setup.py install
```

### Testing
No formal test suite is currently configured in the repository.

### Building Distribution
```bash
# Build source distribution
python setup.py sdist

# Build wheel (if wheel is installed)
python setup.py bdist_wheel
```

## API Communication
- **Protocol**: HTTPS REST API
- **Authentication**: Bearer token (API key)
- **Default Endpoint**: https://localhost:3333
- **Content Type**: JSON request/response bodies