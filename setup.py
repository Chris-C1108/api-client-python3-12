"""This is the setup module for the Python Gophish API client."""

from setuptools import setup

# Read version from pyproject.toml if available, fallback to hardcoded
try:
    import tomllib

    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    version = pyproject["project"]["version"]
    description = pyproject["project"]["description"]
    author = pyproject["project"]["authors"][0]["name"]
    author_email = pyproject["project"]["authors"][0]["email"]
    url = pyproject["project"]["urls"]["Homepage"]
    license_text = pyproject["project"]["license"]["text"]
    keywords = pyproject["project"]["keywords"]
    classifiers = pyproject["project"]["classifiers"]
    install_requires = pyproject["project"]["dependencies"]
except (ImportError, FileNotFoundError, KeyError):
    # Fallback values if pyproject.toml is not available or tomllib is not installed
    version = "1.0.0"
    description = "Python API Client for Gophish"
    author = "Jordan Wright"
    author_email = "python@getgophish.com"
    url = "https://github.com/Chris-C1108/api-client-python3-12"
    license_text = "MIT"
    keywords = ["gophish", "phishing", "security", "api", "client"]
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
    install_requires = [
        "requests>=2.32.0,<3.0.0",
        "python-dateutil>=2.8.2",
        "certifi>=2023.7.22",
    ]

setup(
    name="gophish",
    packages=["gophish", "gophish.api"],
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license_text,
    download_url=f"https://github.com/Chris-C1108/api-client-python3-12/tarball/{version}",
    keywords=keywords,
    classifiers=classifiers,
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "test": ["pytest>=7.0.0", "pytest-cov>=4.0.0", "hypothesis>=6.0.0"],
        "lint": ["black>=23.0.0", "flake8>=6.0.0", "mypy>=1.0.0"],
        "security": ["bandit>=1.7.0", "safety>=2.0.0"],
    },
)
