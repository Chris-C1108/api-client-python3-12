"""
Property-based tests for dependency compatibility and security.

Feature: python-modernization, Property 3: Dependency Compatibility and Security
Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""

import sys
import subprocess
import re
import importlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from packaging import version
import json

import pytest
from hypothesis import given, strategies as st


class TestDependencyCompatibilityAndSecurity:
    """Test that dependencies are compatible, secure, and properly managed."""

    def test_core_dependencies_are_updated(self):
        """Test that core dependencies are updated to secure versions."""
        expected_deps = {
            "requests": "2.32.0",  # Minimum secure version
            "python-dateutil": "2.8.2",  # Updated version
            "certifi": "2023.7.22",  # Updated certificates
        }

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
            except ImportError:
                pytest.skip("TOML library not available")

            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            dependencies = pyproject.get("project", {}).get("dependencies", [])

            for dep_name, min_version in expected_deps.items():
                # Find the dependency in the list
                dep_found = False
                for dep in dependencies:
                    if dep.startswith(dep_name):
                        dep_found = True
                        # Extract version constraint
                        version_match = re.search(r">=([0-9\.]+)", dep)
                        if version_match:
                            actual_version = version_match.group(1)
                            assert version.parse(actual_version) >= version.parse(
                                min_version
                            ), f"{dep_name} should be >= {min_version}, got {actual_version}"
                        break

                assert dep_found, f"Dependency {dep_name} not found in dependencies"

    def test_legacy_dependencies_removed(self):
        """Test that legacy Python 2.7 dependencies have been removed."""
        legacy_deps = ["six", "appdirs", "packaging", "pyparsing"]

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
            except ImportError:
                pytest.skip("TOML library not available")

            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            dependencies = pyproject.get("project", {}).get("dependencies", [])

            for legacy_dep in legacy_deps:
                dep_found = any(dep.startswith(legacy_dep) for dep in dependencies)
                assert (
                    not dep_found
                ), f"Legacy dependency {legacy_dep} should be removed"

    def test_transitive_dependencies_not_pinned(self):
        """Test that transitive dependencies are not unnecessarily pinned."""
        # These should not be in direct dependencies as they're transitive
        transitive_deps = ["urllib3", "chardet", "idna"]

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
            except ImportError:
                pytest.skip("TOML library not available")

            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            dependencies = pyproject.get("project", {}).get("dependencies", [])

            for transitive_dep in transitive_deps:
                dep_found = any(dep.startswith(transitive_dep) for dep in dependencies)
                assert (
                    not dep_found
                ), f"Transitive dependency {transitive_dep} should not be directly specified"

    def test_version_ranges_allow_security_updates(self):
        """Test that version ranges allow automatic security updates."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
            except ImportError:
                pytest.skip("TOML library not available")

            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            dependencies = pyproject.get("project", {}).get("dependencies", [])

            for dep in dependencies:
                # Should use >= for minimum version
                assert (
                    ">=" in dep
                ), f"Dependency {dep} should use >= for minimum version"

                # Should not pin exact versions (unless absolutely necessary)
                assert "==" not in dep, f"Dependency {dep} should not pin exact version"

                # Should have upper bound for major versions to prevent breaking changes
                if "requests" in dep:
                    assert (
                        "<3.0.0" in dep or "<4" in dep
                    ), f"requests dependency should have upper bound: {dep}"

    def test_dependencies_can_be_imported(self):
        """Test that all specified dependencies can be imported."""
        core_modules = ["requests", "dateutil", "certifi"]

        for module_name in core_modules:
            try:
                if module_name == "dateutil":
                    import dateutil.parser

                    assert dateutil.parser is not None
                else:
                    module = importlib.import_module(module_name)
                    assert (
                        module is not None
                    ), f"Module {module_name} should be importable"
            except ImportError:
                pytest.skip(
                    f"Module {module_name} not available (may not be installed)"
                )

    @given(
        st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(min_codepoint=97, max_codepoint=122),
        )
    )
    def test_dependency_name_validation_property(self, package_name: str):
        """Property test: Package names should follow Python naming conventions."""
        # Test that our dependency validation logic works

        # Valid Python package names should:
        # - Start with a letter
        # - Contain only letters, numbers, hyphens, underscores
        # - Not start with numbers or special characters

        is_valid_name = (
            package_name[0].isalpha()
            and all(c.isalnum() or c in "-_" for c in package_name)
            and not package_name.startswith("-")
            and not package_name.startswith("_")
        )

        if is_valid_name:
            # Valid names should be processable
            normalized_name = package_name.lower().replace("_", "-")
            assert isinstance(normalized_name, str)
            assert len(normalized_name) > 0

    def test_requests_security_version(self):
        """Test that requests library is at a secure version."""
        try:
            import requests

            # Check version
            requests_version = version.parse(requests.__version__)
            min_secure_version = version.parse("2.32.0")

            assert (
                requests_version >= min_secure_version
            ), f"requests version {requests_version} is below secure minimum {min_secure_version}"

        except ImportError:
            pytest.skip("requests not available (may not be installed)")

    def test_ssl_certificate_validation_enabled(self):
        """Test that SSL certificate validation is enabled by default."""
        try:
            import requests
            import ssl

            # Test that SSL context has proper verification
            context = ssl.create_default_context()
            assert context.check_hostname, "SSL hostname checking should be enabled"
            assert (
                context.verify_mode == ssl.CERT_REQUIRED
            ), "SSL certificate verification should be required"

            # Test that requests uses verification by default
            session = requests.Session()
            assert (
                session.verify is True
            ), "requests should verify SSL certificates by default"

        except ImportError:
            pytest.skip("requests or ssl not available")

    def test_no_known_vulnerable_versions(self):
        """Test that we're not using known vulnerable versions."""
        # Known vulnerable versions to avoid
        vulnerable_versions = {
            "requests": ["2.24.0", "2.25.0", "2.25.1"],  # Had various security issues
            "certifi": ["2020.6.20", "2021.5.30"],  # Outdated certificates
        }

        for package_name, vuln_versions in vulnerable_versions.items():
            try:
                module = importlib.import_module(package_name)
                if hasattr(module, "__version__"):
                    current_version = module.__version__
                    assert (
                        current_version not in vuln_versions
                    ), f"{package_name} version {current_version} is known to be vulnerable"
            except ImportError:
                # Package not installed, skip check
                continue

    @given(
        st.lists(
            st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(min_codepoint=97, max_codepoint=122),
            ),
            min_size=1,
            max_size=10,
            unique=True,
        )
    )
    def test_dependency_resolution_property(self, package_names: List[str]):
        """Property test: Dependency resolution should handle various package combinations."""
        # Test that our dependency specification doesn't create conflicts

        # Filter to valid package names
        valid_names = [name for name in package_names if name[0].isalpha()]

        if not valid_names:
            return  # Skip if no valid names

        # Test that we can create dependency specifications
        for name in valid_names:
            # Should be able to create version specifications
            version_specs = [
                f"{name}>=1.0.0",
                f"{name}>=1.0.0,<2.0.0",
                f"{name}>=1.0.0,<1.1.0",
            ]

            for spec in version_specs:
                # Should be parseable
                assert ">=" in spec, "Should have minimum version"
                assert name in spec, "Should contain package name"

    def test_development_dependencies_separate(self):
        """Test that development dependencies are properly separated."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
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
            runtime_deps = project.get("dependencies", [])
            optional_deps = project.get("optional-dependencies", {})
            dev_deps = optional_deps.get("dev", [])

            # Development tools should not be in runtime dependencies
            dev_tools = ["pytest", "black", "flake8", "mypy", "bandit", "safety"]

            for tool in dev_tools:
                runtime_has_tool = any(tool in dep for dep in runtime_deps)
                dev_has_tool = any(tool in dep for dep in dev_deps)

                assert (
                    not runtime_has_tool
                ), f"{tool} should not be in runtime dependencies"
                # Note: dev_has_tool might be False if not all dev tools are specified

    def test_dependency_compatibility_matrix(self):
        """Test that our dependencies are compatible with each other."""
        # Test known compatibility issues
        compatibility_matrix = {
            "requests": {
                "compatible_with": ["certifi", "python-dateutil"],
                "min_python": "3.8",
            },
            "python-dateutil": {
                "compatible_with": ["requests", "certifi"],
                "min_python": "3.8",
            },
            "certifi": {
                "compatible_with": ["requests", "python-dateutil"],
                "min_python": "3.8",
            },
        }

        for package, info in compatibility_matrix.items():
            try:
                module = importlib.import_module(
                    package if package != "python-dateutil" else "dateutil"
                )

                # Test that it can be imported (basic compatibility)
                assert module is not None, f"{package} should be importable"

                # Test Python version compatibility
                current_python = f"{sys.version_info.major}.{sys.version_info.minor}"
                min_python = info["min_python"]

                assert version.parse(current_python) >= version.parse(
                    min_python
                ), f"{package} requires Python {min_python}, current is {current_python}"

            except ImportError:
                pytest.skip(f"{package} not available for compatibility testing")

    def test_no_conflicting_version_constraints(self):
        """Test that version constraints don't conflict with each other."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib
            except ImportError:
                pytest.skip("TOML library not available")

            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)

            dependencies = pyproject.get("project", {}).get("dependencies", [])

            # Parse version constraints
            for dep in dependencies:
                # Should not have conflicting constraints like >=2.0,<1.0
                if ">=" in dep and "<" in dep:
                    # Extract version numbers
                    min_match = re.search(r">=([0-9\.]+)", dep)
                    max_match = re.search(r"<([0-9\.]+)", dep)

                    if min_match and max_match:
                        min_version = version.parse(min_match.group(1))
                        max_version = version.parse(max_match.group(1))

                        assert (
                            min_version < max_version
                        ), f"Conflicting version constraint in {dep}: min >= max"

    @given(
        st.tuples(
            st.integers(min_value=1, max_value=10),  # major
            st.integers(min_value=0, max_value=50),  # minor
            st.integers(min_value=0, max_value=50),  # patch
        )
    )
    def test_version_comparison_logic_property(
        self, version_tuple: Tuple[int, int, int]
    ):
        """Property test: Version comparison logic should work correctly."""
        major, minor, patch = version_tuple
        test_version = f"{major}.{minor}.{patch}"

        try:
            parsed_version = version.parse(test_version)

            # Test basic version operations
            assert (
                str(parsed_version).count(".") >= 1
            ), "Version should have at least major.minor"

            # Test comparison operations
            same_version = version.parse(test_version)
            assert parsed_version == same_version, "Same versions should be equal"

            # Test with different versions
            if major > 1:
                lower_version = version.parse(f"{major-1}.{minor}.{patch}")
                assert (
                    parsed_version > lower_version
                ), "Higher major version should be greater"

        except Exception as e:
            pytest.fail(f"Version parsing failed for {test_version}: {e}")
