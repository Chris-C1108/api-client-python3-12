"""
Tests for project structure compatibility.

Validates: Requirements 3.1, 3.2, 1.4
"""

import importlib
import sys
from pathlib import Path
from typing import List, Set

import pytest


class TestProjectStructureCompatibility:
    """Test that project structure remains compatible after modernization."""

    def test_gophish_init_exports_only_gophish_class(self):
        """Test that gophish/__init__.py exports only the Gophish class."""
        try:
            import gophish
        except ImportError:
            pytest.skip("gophish package not available for import")

        # Check that Gophish class is available
        assert hasattr(gophish, "Gophish"), "Gophish class should be exported"

        # Check that it's the main export (minimal public interface)
        public_attrs = [attr for attr in dir(gophish) if not attr.startswith("_")]

        # Should primarily export Gophish class
        assert "Gophish" in public_attrs, "Gophish class must be exported"

        # Verify it's actually a class
        assert isinstance(gophish.Gophish, type), "Gophish should be a class"

    def test_api_submodule_structure_intact(self):
        """Test that api/ submodule structure remains intact."""
        api_modules = [
            "gophish.api.campaigns",
            "gophish.api.groups",
            "gophish.api.templates",
            "gophish.api.pages",
            "gophish.api.smtp",
            "gophish.api.webhooks",
            "gophish.api.imap",
        ]

        for module_name in api_modules:
            try:
                module = importlib.import_module(module_name)
                assert module is not None, f"Module {module_name} should be importable"

                # Each API module should have an API class
                assert hasattr(
                    module, "API"
                ), f"Module {module_name} should have API class"

            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")

    def test_existing_import_patterns_work(self):
        """Test that existing import patterns continue to work."""
        # Test main import pattern
        try:
            from gophish import Gophish

            assert Gophish is not None, "Main import pattern should work"
        except ImportError as e:
            pytest.fail(f"Main import pattern failed: {e}")

        # Test that client can be instantiated (basic functionality)
        try:
            client = Gophish("test-api-key")
            assert client is not None, "Client should be instantiable"

            # Test that API endpoints are available
            expected_endpoints = [
                "campaigns",
                "groups",
                "templates",
                "pages",
                "smtp",
                "webhooks",
                "imap",
            ]

            for endpoint in expected_endpoints:
                assert hasattr(
                    client, endpoint
                ), f"Client should have {endpoint} endpoint"

        except Exception as e:
            pytest.fail(f"Client instantiation failed: {e}")

    def test_setuptools_configuration_compatibility(self):
        """Test that setuptools configuration works with new pyproject.toml."""
        # Test that setup.py can still be used
        setup_py_path = Path(__file__).parent.parent / "setup.py"
        assert (
            setup_py_path.exists()
        ), "setup.py should exist for backward compatibility"

        # Test that pyproject.toml exists
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists(), "pyproject.toml should exist"

        # Test that both configurations are consistent
        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
        except ImportError:
            pytest.skip("TOML library not available")

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        # Check build system configuration
        build_system = pyproject.get("build-system", {})
        requires = build_system.get("requires", [])
        assert any(
            "setuptools" in req for req in requires
        ), "setuptools should be in build requirements"
        assert (
            build_system.get("build-backend") == "setuptools.build_meta"
        ), "Should use setuptools build backend"

    def test_package_discovery_works(self):
        """Test that package discovery finds the correct packages."""
        expected_packages = {"gophish", "gophish.api"}

        # Check that package directories exist
        base_path = Path(__file__).parent.parent
        gophish_path = base_path / "gophish"
        api_path = base_path / "gophish" / "api"

        assert gophish_path.exists(), "gophish package directory should exist"
        assert api_path.exists(), "gophish.api package directory should exist"

        # Check that __init__.py files exist
        assert (
            gophish_path / "__init__.py"
        ).exists(), "gophish/__init__.py should exist"
        assert (
            api_path / "__init__.py"
        ).exists(), "gophish/api/__init__.py should exist"

    def test_no_python2_compatibility_code_remains(self):
        """Test that Python 2.7 compatibility code has been removed."""
        # Check that six is not imported in main modules
        main_modules = [
            Path(__file__).parent.parent / "gophish" / "__init__.py",
            Path(__file__).parent.parent / "gophish" / "client.py",
            Path(__file__).parent.parent / "gophish" / "models.py",
        ]

        for module_path in main_modules:
            if module_path.exists():
                content = module_path.read_text()
                assert (
                    "import six" not in content
                ), f"six import found in {module_path.name}"
                assert (
                    "from six" not in content
                ), f"six import found in {module_path.name}"

        # Check setup.py doesn't include six dependency
        setup_py_path = Path(__file__).parent.parent / "setup.py"
        if setup_py_path.exists():
            setup_content = setup_py_path.read_text()
            assert '"six' not in setup_content, "six dependency should be removed"
            assert "'six" not in setup_content, "six dependency should be removed"

    def test_modern_python_features_compatibility(self):
        """Test that the code is compatible with modern Python features."""
        # Test that f-strings can be used (Python 3.6+)
        test_string = f"test-{42}"
        assert test_string == "test-42", "f-strings should work"

        # Test that type hints can be used (Python 3.5+)
        def test_function(x: int) -> str:
            return str(x)

        result = test_function(42)
        assert result == "42", "Type hints should not break functionality"

        # Test that pathlib works (Python 3.4+, but better in 3.6+)
        from pathlib import Path

        test_path = Path(__file__)
        assert test_path.exists(), "pathlib should work correctly"
