# Gophish Python API Client (Python 3.8+ Modernized)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://pypi.org/project/gophish/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This is a modernized fork of the official [Gophish Python API Client](https://github.com/gophish/api-client-python) that has been updated to support Python 3.8-3.12 with modern dependencies and enhanced security.

## 🚀 What's New in This Fork

- **Python 3.8-3.12 Support**: Dropped Python 2.7 support, fully modernized for current Python versions
- **Updated Dependencies**: All dependencies upgraded to latest secure versions
- **Modern Python Features**: Uses f-strings, type hints compatibility, and modern syntax
- **Enhanced Security**: SSL certificate validation enabled by default, secure dependency versions
- **Comprehensive Testing**: Property-based testing with Hypothesis, full test coverage
- **Modern CI/CD**: GitHub Actions with multi-version testing matrix
- **Modern Packaging**: Uses pyproject.toml with backward-compatible setup.py

## 📋 Requirements

- Python 3.8 or higher
- requests >= 2.32.0 (for security)
- python-dateutil >= 2.8.2
- certifi >= 2023.7.22

## 🔧 Installation

Install from PyPI:

```bash
pip install gophish
```

Or install from source:

```bash
git clone https://github.com/Chris-C1108/api-client-python3-12.git
cd api-client-python3-12
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## 🚀 Quick Start

Gophish was built from the ground-up to be API-first. This means that we build out the API endpoints for all of our features, and the UI is simply a wrapper around these endpoints.

To interface with Gophish using Python, we've created a `gophish` client library.

> If you want to access the API directly, please refer to our [API Documentation](https://www.gitbook.com/book/gophish/api-documentation/details)

Getting up and running with the Python library is quick and easy.

To start, simply create a client using the API key found in the [Settings page](https://gophish.gitbooks.io/user-guide/content/documentation/changing_user_settings.html#changing-your-password--updating-settings).

```python
from gophish import Gophish

api_key = 'API_KEY'
api = Gophish(api_key)

# Example: Get all campaigns
campaigns = api.campaigns.get()
print(f"Found {len(campaigns)} campaigns")

# Example: Create a new group
from gophish.models import Group, User

users = [User(first_name="John", last_name="Doe", email="john.doe@example.com")]
group = Group(name="Test Group", targets=users)
created_group = api.groups.post(group)
print(f"Created group: {created_group.name}")
```

## 🔒 Security Features

This modernized version includes several security enhancements:

- **SSL Certificate Validation**: Enabled by default, cannot be easily bypassed
- **Secure Dependencies**: All dependencies updated to versions without known vulnerabilities
- **Modern TLS**: Uses up-to-date certificate authorities via latest certifi
- **Security Scanning**: Automated vulnerability scanning in CI/CD pipeline

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gophish

# Run only fast tests (skip property-based tests)
pytest -m "not slow"

# Run security tests
pytest -m security
```

## 🛠 Development

Set up development environment:

```bash
# Clone the repository
git clone https://github.com/Chris-C1108/api-client-python3-12.git
cd api-client-python3-12

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Run code quality checks
black gophish tests
flake8 gophish tests
mypy gophish --ignore-missing-imports

# Run security checks
bandit -r gophish
safety check
```

## 📚 API Documentation

The API interface remains fully compatible with the original client. All existing code should work without modification.

### Available Endpoints

- **Campaigns**: `api.campaigns`
- **Groups**: `api.groups`
- **Templates**: `api.templates`
- **Landing Pages**: `api.pages`
- **SMTP Settings**: `api.smtp`
- **Webhooks**: `api.webhooks`
- **IMAP Settings**: `api.imap`

Each endpoint supports standard CRUD operations:
- `get()` - Retrieve resources
- `post(resource)` - Create new resource
- `put(resource)` - Update existing resource
- `delete(resource_id)` - Delete resource

## 🔄 Migration from Original Client

This fork is a drop-in replacement for the original client. Simply update your requirements:

```bash
# Old installation
pip install gophish==0.5.1

# New installation (this fork)
pip install gophish>=1.0.0
```

No code changes required! All existing APIs remain compatible.

## 🐛 Differences from Original

- **Python 2.7 Support Removed**: This version only supports Python 3.8+
- **Dependencies Updated**: All dependencies are at secure, modern versions
- **Enhanced Error Handling**: Better error messages and exception chaining
- **Modern Python Syntax**: Uses f-strings and modern language features internally
- **Comprehensive Testing**: Much more extensive test coverage

## 📄 License

This project maintains the same MIT license as the original Gophish API client.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Original [Gophish API Client](https://github.com/gophish/api-client-python) by Jordan Wright
- [Gophish Project](https://getgophish.com/) for the excellent phishing framework
- All contributors to the original project

## 📞 Support

For issues specific to this modernized fork, please open an issue on this repository.

For general Gophish questions, refer to the [official documentation](https://docs.getgophish.com/python-api-client/).

---

**Note**: This is an unofficial modernized fork. For the original client, visit [gophish/api-client-python](https://github.com/gophish/api-client-python).
