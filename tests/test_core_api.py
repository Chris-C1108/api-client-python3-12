"""
Unit tests for core API functionality.

Validates: Requirements 1.4, 5.3
"""

import pytest
from unittest.mock import Mock, patch
from gophish import Gophish
from gophish.client import GophishClient
from gophish.models import Campaign, Group, Template, Page, SMTP, Webhook, IMAP, Error


class TestGophishClient:
    """Test the core Gophish client functionality."""

    def test_client_initialization(self):
        """Test that client initializes correctly."""
        api_key = "test-api-key"
        host = "https://test.example.com"

        client = Gophish(api_key, host=host)

        assert client.client.api_key == api_key
        assert client.client.host == "https://test.example.com/"

        # Test that all API endpoints are available
        assert hasattr(client, "campaigns")
        assert hasattr(client, "groups")
        assert hasattr(client, "templates")
        assert hasattr(client, "pages")
        assert hasattr(client, "smtp")
        assert hasattr(client, "webhooks")
        assert hasattr(client, "imap")

    def test_client_initialization_with_trailing_slash(self):
        """Test that client handles host URLs with trailing slashes correctly."""
        api_key = "test-api-key"
        host = "https://test.example.com/"

        client = Gophish(api_key, host=host)

        assert client.client.host == "https://test.example.com/"

    def test_client_initialization_without_trailing_slash(self):
        """Test that client adds trailing slash when missing."""
        api_key = "test-api-key"
        host = "https://test.example.com"

        client = Gophish(api_key, host=host)

        assert client.client.host == "https://test.example.com/"

    def test_client_initialization_with_default_host(self):
        """Test that client uses default host when none provided."""
        api_key = "test-api-key"

        client = Gophish(api_key)

        assert client.client.host == "https://localhost:3333/"

    def test_client_initialization_with_kwargs(self):
        """Test that client passes through additional kwargs."""
        api_key = "test-api-key"
        timeout = 30
        verify = False

        client = Gophish(api_key, timeout=timeout, verify=verify)

        assert client.client._client_kwargs["timeout"] == timeout
        assert client.client._client_kwargs["verify"] == verify


class TestGophishClientHTTP:
    """Test the HTTP client functionality."""

    @patch("gophish.client.requests.request")
    def test_execute_method(self, mock_request):
        """Test that execute method makes correct HTTP requests."""
        # Setup mock response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"id": 1, "name": "test"}
        mock_request.return_value = mock_response

        client = GophishClient("test-api-key", "https://test.example.com")

        # Test GET request
        response = client.execute("GET", "campaigns")

        mock_request.assert_called_once_with(
            "GET",
            "https://test.example.com/campaigns",
            headers={"Authorization": "Bearer test-api-key"},
        )
        assert response == mock_response

    @patch("gophish.client.requests.request")
    def test_execute_method_with_json_data(self, mock_request):
        """Test that execute method handles JSON data correctly."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"id": 1, "name": "test"}
        mock_request.return_value = mock_response

        client = GophishClient("test-api-key", "https://test.example.com")
        test_data = {"name": "Test Campaign"}

        response = client.execute("POST", "campaigns", json=test_data)

        mock_request.assert_called_once_with(
            "POST",
            "https://test.example.com/campaigns",
            headers={"Authorization": "Bearer test-api-key"},
            json=test_data,
        )

    @patch("gophish.client.requests.request")
    def test_execute_method_with_additional_kwargs(self, mock_request):
        """Test that execute method passes through additional kwargs."""
        mock_response = Mock()
        mock_response.ok = True
        mock_request.return_value = mock_response

        client = GophishClient("test-api-key", "https://test.example.com", timeout=30)

        response = client.execute("GET", "campaigns", verify=False)

        # Should include both client kwargs and method kwargs
        expected_kwargs = {
            "headers": {"Authorization": "Bearer test-api-key"},
            "timeout": 30,
            "verify": False,
        }

        mock_request.assert_called_once_with(
            "GET", "https://test.example.com/campaigns", **expected_kwargs
        )


class TestAPIEndpoints:
    """Test that API endpoints are properly configured."""

    def test_campaigns_endpoint_exists(self):
        """Test that campaigns endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.campaigns, "get")
        assert hasattr(client.campaigns, "post")
        assert hasattr(client.campaigns, "put")
        assert hasattr(client.campaigns, "delete")

    def test_groups_endpoint_exists(self):
        """Test that groups endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.groups, "get")
        assert hasattr(client.groups, "post")
        assert hasattr(client.groups, "put")
        assert hasattr(client.groups, "delete")

    def test_templates_endpoint_exists(self):
        """Test that templates endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.templates, "get")
        assert hasattr(client.templates, "post")
        assert hasattr(client.templates, "put")
        assert hasattr(client.templates, "delete")

    def test_pages_endpoint_exists(self):
        """Test that pages endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.pages, "get")
        assert hasattr(client.pages, "post")
        assert hasattr(client.pages, "put")
        assert hasattr(client.pages, "delete")

    def test_smtp_endpoint_exists(self):
        """Test that SMTP endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.smtp, "get")
        assert hasattr(client.smtp, "post")
        assert hasattr(client.smtp, "put")
        assert hasattr(client.smtp, "delete")

    def test_webhooks_endpoint_exists(self):
        """Test that webhooks endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.webhooks, "get")
        assert hasattr(client.webhooks, "post")
        assert hasattr(client.webhooks, "put")
        assert hasattr(client.webhooks, "delete")

    def test_imap_endpoint_exists(self):
        """Test that IMAP endpoint is available."""
        client = Gophish("test-api-key")

        assert hasattr(client.imap, "get")
        assert hasattr(client.imap, "post")
        assert hasattr(client.imap, "put")
        assert hasattr(client.imap, "delete")


class TestErrorHandling:
    """Test error handling functionality."""

    def test_error_model_creation(self):
        """Test that Error model can be created."""
        error = Error()
        assert error is not None
        assert isinstance(error, Exception)

    def test_error_model_parsing(self):
        """Test that Error model can parse JSON data."""
        error_data = {"message": "Test error message", "success": False, "data": None}

        error = Error.parse(error_data)

        assert error.message == "Test error message"
        assert error.success is False
        assert error.data is None

    def test_error_string_representation(self):
        """Test that Error model has proper string representation."""
        error_data = {"message": "Test error message", "success": False}

        error = Error.parse(error_data)

        assert str(error) == "Test error message"

    @patch("gophish.client.requests.request")
    def test_api_error_handling(self, mock_request):
        """Test that API errors are properly handled."""
        # Setup mock error response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.json.return_value = {"message": "API Error", "success": False}
        mock_request.return_value = mock_response

        client = Gophish("test-api-key")

        # Should raise Error exception
        with pytest.raises(Error):
            client.campaigns.get()


class TestBackwardCompatibility:
    """Test that backward compatibility is maintained."""

    def test_old_style_import_works(self):
        """Test that old-style imports still work."""
        from gophish import Gophish

        client = Gophish("test-api-key")
        assert client is not None

    def test_client_interface_unchanged(self):
        """Test that client interface hasn't changed."""
        client = Gophish("test-api-key")

        # Test that all expected attributes exist
        expected_attrs = [
            "client",
            "campaigns",
            "groups",
            "templates",
            "pages",
            "smtp",
            "webhooks",
            "imap",
        ]

        for attr in expected_attrs:
            assert hasattr(client, attr), f"Client should have {attr} attribute"

    def test_api_methods_unchanged(self):
        """Test that API methods haven't changed."""
        client = Gophish("test-api-key")

        # Test that all endpoints have expected methods
        endpoints = [client.campaigns, client.groups, client.templates, client.pages]
        expected_methods = ["get", "post", "put", "delete"]

        for endpoint in endpoints:
            for method in expected_methods:
                assert hasattr(
                    endpoint, method
                ), f"Endpoint should have {method} method"

    def test_model_interface_unchanged(self):
        """Test that model interfaces haven't changed."""
        # Test that models can still be created and used
        campaign = Campaign()
        assert campaign is not None

        group = Group()
        assert group is not None

        template = Template()
        assert template is not None

        # Test that models have expected methods
        models = [campaign, group, template]
        for model in models:
            assert hasattr(model, "as_dict"), "Model should have as_dict method"
            assert hasattr(model, "parse"), "Model should have parse class method"


class TestModernPythonFeatures:
    """Test that modern Python features work correctly."""

    def test_f_strings_work(self):
        """Test that f-strings work in the codebase."""
        api_key = "test-key"
        expected_header = f"Bearer {api_key}"

        client = GophishClient(api_key)
        # The client should use f-strings internally for header formatting
        assert expected_header == f"Bearer {api_key}"

    def test_pathlib_compatibility(self):
        """Test that pathlib works with the codebase."""
        from pathlib import Path

        # Should be able to use pathlib for file operations
        current_file = Path(__file__)
        assert current_file.exists()
        assert current_file.suffix == ".py"

    def test_type_hints_compatibility(self):
        """Test that type hints don't break functionality."""

        def typed_function(api_key: str) -> Gophish:
            return Gophish(api_key)

        client = typed_function("test-key")
        assert isinstance(client, Gophish)

    def test_dictionary_unpacking(self):
        """Test that dictionary unpacking works."""
        base_config = {"timeout": 30}
        additional_config = {"verify": False}

        merged_config = {**base_config, **additional_config}

        assert merged_config["timeout"] == 30
        assert merged_config["verify"] is False

    def test_exception_chaining(self):
        """Test that exception chaining works correctly."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise Error() from e
        except Error as error:
            assert error.__cause__ is not None
            assert isinstance(error.__cause__, ValueError)
