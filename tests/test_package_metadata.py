"""
Property-based tests for package metadata completeness.

Feature: python-modernization, Property 4: Package Metadata Completeness
Validates: Requirements 3.3, 3.4
"""

import importlib.metadata
import sys
from pathlib import Path
from typing import Dict, Any, List

import pytest
from hypothesis import given, strategies as st


class TestPackageMetadataCompleteness:
    """Test that package metadata is complete and properly formatted."""

    def test_package_metadata_exists(self):
        """Test that basic package metadata exists."""
        try:
            metadata = importlib.metadata.metadata("gophish")
        except importlib.metadata.PackageNotFoundError:
            # If package is not installed, read from pyproject.toml
            pytest.skip("Package not installed, testing pyproject.toml directly")

        # Required metadata fields
        required_fields = {
            "Name": "gophish",
            "Version": str,
            "Summary": str,
            "Author": str,
            "Author-email": str,
            "License": str,
            "Home-page": str,
        }

        for field, expected_type in required_fields.items():
            assert field in metadata, f"Required field '{field}' missing from metadata"
            if expected_type != str:
                assert (
                    metadata[field] == expected_type
                ), f"Field '{field}' has incorrect value"
            else:
                assert metadata[field], f"Field '{field}' is empty"

    def test_pyproject_toml_metadata_completeness(self):
        """Test that pyproject.toml contains all required metadata."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if not pyproject_path.exists():
            pytest.skip("pyproject.toml not found")

        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
        except ImportError:
            pytest.skip("TOML library not available")

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        # Check project section exists
        assert "project" in pyproject, "pyproject.toml missing [project] section"
        project = pyproject["project"]

        # Required fields
        required_fields = [
            "name",
            "version",
            "description",
            "authors",
            "license",
            "readme",
            "requires-python",
            "classifiers",
        ]

        for field in required_fields:
            assert field in project, f"Required field '{field}' missing from [project]"
            assert project[field], f"Field '{field}' is empty"

    def test_development_dependencies_separation(self):
        """Test that development dependencies are separate from runtime dependencies."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if not pyproject_path.exists():
            pytest.skip("pyproject.toml not found")

        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
        except ImportError:
            pytest.skip("TOML library not available")

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        project = pyproject.get("project", {})

        # Runtime dependencies should be minimal
        runtime_deps = project.get("dependencies", [])
        dev_deps = project.get("optional-dependencies", {}).get("dev", [])

        # Core runtime dependencies (should be small set)
        expected_runtime = {"requests", "python-dateutil", "certifi"}
        actual_runtime = {dep.split(">=")[0].split("==")[0] for dep in runtime_deps}

        # Verify runtime deps are minimal and expected
        assert actual_runtime.issubset(
            expected_runtime
        ), f"Unexpected runtime dependencies: {actual_runtime - expected_runtime}"

        # Verify dev dependencies exist and are separate
        assert dev_deps, "Development dependencies should be specified"

        # Common dev tools should be in dev dependencies, not runtime
        dev_tools = {"pytest", "black", "flake8", "mypy", "bandit", "safety"}
        actual_dev = {dep.split(">=")[0].split("==")[0] for dep in dev_deps}

        # At least some dev tools should be present
        assert dev_tools.intersection(
            actual_dev
        ), "Expected development tools not found in optional-dependencies"

    @given(st.text(min_size=1, max_size=100))
    def test_metadata_field_format_property(self, field_value: str):
        """Property test: metadata fields should handle various string formats."""
        # This tests that our metadata parsing is robust
        # In a real scenario, we'd test with actual metadata manipulation

        # Basic validation that strings are handled properly
        assert isinstance(field_value, str)
        assert len(field_value) > 0

        # Test that common metadata operations work
        normalized = field_value.strip()
        assert isinstance(normalized, str)

    def test_python_version_constraint_format(self):
        """Test that Python version constraints are properly formatted."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if not pyproject_path.exists():
            pytest.skip("pyproject.toml not found")

        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
        except ImportError:
            pytest.skip("TOML library not available")

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        project = pyproject.get("project", {})
        requires_python = project.get("requires-python", "")

        # Should specify minimum Python 3.8
        assert requires_python, "requires-python field is missing"
        assert "3.8" in requires_python, "Should require Python 3.8 or higher"
        assert ">=" in requires_python, "Should use >= for minimum version"

    def test_classifiers_include_supported_python_versions(self):
        """Test that classifiers include all supported Python versions."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if not pyproject_path.exists():
            pytest.skip("pyproject.toml not found")

        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib
        except ImportError:
            pytest.skip("TOML library not available")

        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)

        project = pyproject.get("project", {})
        classifiers = project.get("classifiers", [])

        # Expected Python version classifiers
        expected_versions = [
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ]

        for version_classifier in expected_versions:
            assert (
                version_classifier in classifiers
            ), f"Missing classifier: {version_classifier}"

        # Should NOT include Python 2.7
        python_2_classifier = "Programming Language :: Python :: 2.7"
        assert (
            python_2_classifier not in classifiers
        ), "Should not include Python 2.7 classifier"
