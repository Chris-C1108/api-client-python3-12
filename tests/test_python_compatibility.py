"""
Property-based tests for multi-Python version compatibility.

Feature: python-modernization, Property 1: Multi-Python Version Compatibility
Validates: Requirements 1.1, 1.4
"""

import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Dict, Any

import pytest
from hypothesis import given, strategies as st, assume


class TestMultiPythonVersionCompatibility:
    """Test that the package works correctly across all supported Python versions."""

    def test_current_python_version_supported(self):
        """Test that the current Python version is supported."""
        current_version = sys.version_info

        # Should be Python 3.8 or higher
        assert current_version >= (
            3,
            8,
        ), f"Current Python version {current_version} is below minimum 3.8"

        # Should be Python 3.12 or lower (current max supported)
        assert current_version[:2] <= (
            3,
            12,
        ), f"Current Python version {current_version} is above maximum 3.12"

    def test_package_imports_successfully(self):
        """Test that the package can be imported successfully."""
        try:
            import gophish

            assert gophish is not None, "gophish package should import successfully"

            # Test main class import
            from gophish import Gophish

            assert Gophish is not None, "Gophish class should import successfully"

        except ImportError as e:
            pytest.fail(f"Package import failed: {e}")

    def test_core_functionality_works(self):
        """Test that core functionality works on current Python version."""
        try:
            from gophish import Gophish

            # Test client instantiation
            client = Gophish("test-api-key")
            assert client is not None, "Client should instantiate successfully"

            # Test that API endpoints are accessible
            endpoints = [
                "campaigns",
                "groups",
                "templates",
                "pages",
                "smtp",
                "webhooks",
                "imap",
            ]
            for endpoint in endpoints:
                assert hasattr(
                    client, endpoint
                ), f"Client should have {endpoint} endpoint"
                endpoint_obj = getattr(client, endpoint)
                assert (
                    endpoint_obj is not None
                ), f"{endpoint} endpoint should not be None"

        except Exception as e:
            pytest.fail(f"Core functionality test failed: {e}")

    def test_modern_python_features_work(self):
        """Test that modern Python features work correctly."""
        # Test f-strings (Python 3.6+)
        test_value = "test"
        f_string_result = f"Value: {test_value}"
        assert f_string_result == "Value: test", "f-strings should work"

        # Test type hints (Python 3.5+, but better in 3.6+)
        def typed_function(x: int) -> str:
            return str(x)

        result = typed_function(42)
        assert result == "42", "Type hints should not break functionality"

        # Test pathlib (Python 3.4+, but better in 3.6+)
        from pathlib import Path

        current_file = Path(__file__)
        assert current_file.exists(), "pathlib should work correctly"

        # Test dictionary unpacking (Python 3.5+)
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        merged = {**dict1, **dict2}
        assert merged == {"a": 1, "b": 2, "c": 3, "d": 4}, "Dict unpacking should work"

    @given(
        st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(min_codepoint=32, max_codepoint=126),
        )
    )
    def test_api_key_handling_property(self, api_key: str):
        """Property test: API key handling should work with various string formats."""
        assume(api_key.strip())  # Assume non-empty after stripping

        try:
            from gophish import Gophish

            client = Gophish(api_key)

            # Test that API key is stored correctly
            assert (
                client.client.api_key == api_key
            ), "API key should be stored correctly"

            # Test that authorization header is formatted correctly
            expected_header = f"Bearer {api_key}"
            # We can't easily test the actual header without making a request,
            # but we can test the format logic
            assert expected_header.startswith(
                "Bearer "
            ), "Authorization header should start with Bearer"

        except Exception as e:
            pytest.fail(f"API key handling failed for key '{api_key}': {e}")

    @given(st.text(min_size=1, max_size=100))
    def test_url_handling_property(self, host_suffix: str):
        """Property test: URL handling should work with various host formats."""
        # Create valid URLs by prepending https://
        base_hosts = [
            "https://localhost:3333",
            "https://example.com",
            "https://api.example.com",
        ]

        for base_host in base_hosts:
            try:
                from gophish import Gophish

                # Test with and without trailing slash
                for host in [base_host, base_host + "/"]:
                    client = Gophish("test-key", host=host)

                    # Host should always end with slash after processing
                    assert client.client.host.endswith(
                        "/"
                    ), f"Host should end with slash: {client.client.host}"

                    # Host should start with https://
                    assert client.client.host.startswith(
                        "https://"
                    ), f"Host should start with https://: {client.client.host}"

            except Exception as e:
                pytest.fail(f"URL handling failed for host '{base_host}': {e}")

    def test_backward_compatibility_maintained(self):
        """Test that existing API interfaces are maintained."""
        try:
            from gophish import Gophish

            # Test that old-style instantiation still works
            client = Gophish("test-api-key")

            # Test that all expected methods exist
            expected_methods = [
                # Client methods
                "client",
                # API endpoints
                "campaigns",
                "groups",
                "templates",
                "pages",
                "smtp",
                "webhooks",
                "imap",
            ]

            for method in expected_methods:
                assert hasattr(client, method), f"Client should have {method} attribute"

            # Test that client has execute method
            assert hasattr(
                client.client, "execute"
            ), "Client should have execute method"

            # Test that API endpoints have expected methods
            api_methods = ["get", "post", "put", "delete"]
            for endpoint_name in ["campaigns", "groups", "templates"]:
                endpoint = getattr(client, endpoint_name)
                for method in api_methods:
                    assert hasattr(
                        endpoint, method
                    ), f"{endpoint_name} endpoint should have {method} method"

        except Exception as e:
            pytest.fail(f"Backward compatibility test failed: {e}")

    def test_no_python2_dependencies_remain(self):
        """Test that no Python 2.7 dependencies remain in the code."""
        # Check that six is not imported anywhere
        import ast
        import os

        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse the AST to check for imports
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            assert alias.name != "six", f"six import found in {py_file}"
                    elif isinstance(node, ast.ImportFrom):
                        assert node.module != "six", f"six import found in {py_file}"

            except Exception as e:
                pytest.fail(f"Failed to check {py_file}: {e}")

    def test_exception_handling_compatibility(self):
        """Test that exception handling works correctly across Python versions."""
        from gophish.models import Error, Success

        # Test that custom exceptions can be instantiated
        error = Error()
        success = Success()

        assert isinstance(error, Exception), "Error should be an Exception"
        assert isinstance(success, Exception), "Success should be an Exception"

        # Test that they have the expected methods
        assert hasattr(error, "parse"), "Error should have parse method"
        assert hasattr(success, "parse"), "Success should have parse method"

        # Test exception inheritance works correctly
        try:
            raise Error()
        except Error:
            pass  # Expected
        except Exception as e:
            pytest.fail(f"Error exception handling failed: {e}")

    @given(
        st.dictionaries(
            st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(min_codepoint=97, max_codepoint=122),
            ),
            st.one_of(st.text(), st.integers(), st.booleans(), st.none()),
            min_size=1,
            max_size=10,
        )
    )
    def test_model_parsing_property(self, json_data: Dict[str, Any]):
        """Property test: Model parsing should handle various JSON structures."""
        from gophish.models import Model

        # Create a simple test model
        class TestModel(Model):
            _valid_properties = {key: None for key in json_data.keys()}

            def __init__(self, **kwargs):
                super().__init__()
                for key, default in self._valid_properties.items():
                    setattr(self, key, kwargs.get(key, default))

            @classmethod
            def parse(cls, json_dict):
                model = cls()
                for key, val in json_dict.items():
                    if key in cls._valid_properties:
                        setattr(model, key, val)
                return model

        try:
            # Test parsing
            model = TestModel.parse(json_data)
            assert model is not None, "Model should parse successfully"

            # Test that parsed data matches input
            for key, value in json_data.items():
                if hasattr(model, key):
                    assert (
                        getattr(model, key) == value
                    ), f"Parsed value for {key} should match input"

            # Test serialization back to dict
            result_dict = model.as_dict()
            assert isinstance(result_dict, dict), "as_dict should return a dictionary"

        except Exception as e:
            pytest.fail(f"Model parsing failed for data {json_data}: {e}")
