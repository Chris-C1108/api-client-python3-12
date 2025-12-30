"""
Pytest configuration and fixtures for Gophish API client tests.
"""

import pytest
from unittest.mock import Mock, MagicMock
from gophish import Gophish
from gophish.client import GophishClient


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock()
    response.ok = True
    response.status_code = 200
    response.json.return_value = {"id": 1, "name": "test"}
    return response


@pytest.fixture
def mock_client():
    """Create a mock Gophish client."""
    client = Mock(spec=GophishClient)
    client.execute.return_value = Mock()
    client.execute.return_value.ok = True
    client.execute.return_value.json.return_value = {"id": 1, "name": "test"}
    return client


@pytest.fixture
def gophish_client():
    """Create a Gophish client instance for testing."""
    return Gophish("test-api-key", host="https://test.example.com")


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing."""
    return {
        "id": 1,
        "name": "Test Campaign",
        "status": "In progress",
        "created_date": "2024-01-01T00:00:00Z",
        "launch_date": "2024-01-01T00:00:00Z",
        "results": [],
        "timeline": [],
        "groups": [],
        "template": None,
        "page": None,
        "smtp": None,
        "url": "https://test.example.com",
    }


@pytest.fixture
def sample_group_data():
    """Sample group data for testing."""
    return {
        "id": 1,
        "name": "Test Group",
        "modified_date": "2024-01-01T00:00:00Z",
        "targets": [
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "position": "Developer",
            }
        ],
    }


@pytest.fixture
def sample_template_data():
    """Sample template data for testing."""
    return {
        "id": 1,
        "name": "Test Template",
        "subject": "Test Subject",
        "text": "Test text content",
        "html": "<p>Test HTML content</p>",
        "modified_date": "2024-01-01T00:00:00Z",
        "attachments": [],
    }


@pytest.fixture
def sample_page_data():
    """Sample page data for testing."""
    return {
        "id": 1,
        "name": "Test Page",
        "html": "<html><body>Test Page</body></html>",
        "modified_date": "2024-01-01T00:00:00Z",
        "capture_credentials": True,
        "capture_passwords": True,
        "redirect_url": "https://example.com",
    }


@pytest.fixture
def sample_smtp_data():
    """Sample SMTP data for testing."""
    return {
        "id": 1,
        "name": "Test SMTP",
        "interface_type": "SMTP",
        "host": "smtp.example.com",
        "username": "test@example.com",
        "password": "password",
        "from_address": "test@example.com",
        "ignore_cert_errors": False,
        "modified_date": "2024-01-01T00:00:00Z",
        "headers": [],
    }


@pytest.fixture
def sample_webhook_data():
    """Sample webhook data for testing."""
    return {
        "id": 1,
        "name": "Test Webhook",
        "url": "https://webhook.example.com",
        "secret": "secret",
        "is_active": True,
    }


@pytest.fixture
def sample_imap_data():
    """Sample IMAP data for testing."""
    return {
        "enabled": True,
        "host": "imap.example.com",
        "port": 993,
        "username": "test@example.com",
        "password": "password",
        "tls": True,
        "folder": "INBOX",
        "restrict_domain": "example.com",
        "delete_reported_campaign_email": False,
        "last_login": "2024-01-01T00:00:00Z",
        "modified_date": "2024-01-01T00:00:00Z",
        "imap_freq": 60,
    }


# Hypothesis strategies for property-based testing
try:
    from hypothesis import strategies as st

    # Strategy for generating valid email addresses
    email_strategy = st.builds(
        lambda local, domain: f"{local}@{domain}",
        local=st.text(
            min_size=1,
            max_size=20,
            alphabet=st.characters(min_codepoint=97, max_codepoint=122),
        ),
        domain=st.text(
            min_size=3,
            max_size=20,
            alphabet=st.characters(min_codepoint=97, max_codepoint=122),
        ).map(lambda x: f"{x}.com"),
    )

    # Strategy for generating valid URLs
    url_strategy = st.builds(
        lambda scheme, domain, path: f"{scheme}://{domain}{path}",
        scheme=st.sampled_from(["http", "https"]),
        domain=st.text(
            min_size=3,
            max_size=20,
            alphabet=st.characters(min_codepoint=97, max_codepoint=122),
        ).map(lambda x: f"{x}.com"),
        path=st.text(
            min_size=0,
            max_size=50,
            alphabet=st.characters(min_codepoint=97, max_codepoint=122),
        ).map(lambda x: f"/{x}" if x else ""),
    )

    # Strategy for generating API keys
    api_key_strategy = st.text(
        min_size=10,
        max_size=100,
        alphabet=st.characters(min_codepoint=33, max_codepoint=126),
    )

except ImportError:
    # Hypothesis not available, skip strategies
    pass


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "property: marks tests as property-based tests")
    config.addinivalue_line(
        "markers", "security: marks tests as security-related tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark property-based tests
        if "property" in item.name.lower():
            item.add_marker(pytest.mark.property)

        # Mark integration tests
        if "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)

        # Mark security tests
        if "security" in item.name.lower():
            item.add_marker(pytest.mark.security)

        # Mark slow tests (property-based tests are typically slower)
        if hasattr(item, "function") and hasattr(item.function, "__annotations__"):
            # Check if test uses hypothesis (property-based testing)
            if any(
                "hypothesis" in str(annotation)
                for annotation in item.function.__annotations__.values()
            ):
                item.add_marker(pytest.mark.slow)
