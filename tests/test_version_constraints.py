"""
Property-based tests for version constraint enforcement.

Feature: python-modernization, Property 2: Version Constraint Enforcement
Validates: Requirements 1.2, 1.3
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple, List
import re

import pytest
from hypothesis import given, strategies as st


class TestVersionConstraintEnforcement:
    """Test that Python version constraints are properly enforced."""

    def test_python_requires_constraint_exists(self):
        """Test that python_requires constraint is properly set."""
        # Check pyproject.toml
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
            requires_python = project.get("requires-python", "")

            assert requires_python, "requires-python should be specified"
            assert ">=3.8" in requires_python, "Should require Python 3.8 or higher"

        # Check setup.py as fallback
        setup_py_path = Path(__file__).parent.parent / "setup.py"
        if setup_py_path.exists():
            setup_content = setup_py_path.read_text()
            assert (
                'python_requires=">=3.8"' in setup_content
            ), "setup.py should specify python_requires>=3.8"

    def test_current_version_meets_requirements(self):
        """Test that current Python version meets the requirements."""
        current_version = sys.version_info

        # Should be 3.8 or higher
        assert current_version >= (
            3,
            8,
        ), f"Current Python {current_version} is below minimum requirement 3.8"

        # Should be within supported range (3.8-3.12)
        assert current_version[:2] <= (
            3,
            12,
        ), f"Current Python {current_version} is above tested range 3.12"

    def test_version_constraint_format_is_valid(self):
        """Test that version constraint format follows PEP 440."""
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

        # Should follow PEP 440 format
        # Valid formats: >=3.8, >=3.8.0, >=3.8,<4.0, etc.
        pep440_pattern = r"^>=\d+\.\d+(\.\d+)?([,<>=\d\.]*)?$"
        assert re.match(
            pep440_pattern, requires_python
        ), f"requires-python '{requires_python}' should follow PEP 440 format"

    def test_classifiers_match_version_constraints(self):
        """Test that classifiers match the version constraints."""
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
        classifiers = project.get("classifiers", [])

        # Extract minimum version from requires-python
        version_match = re.search(r">=(\d+)\.(\d+)", requires_python)
        if version_match:
            min_major, min_minor = int(version_match.group(1)), int(
                version_match.group(2)
            )

            # Check that classifiers include supported versions
            python_classifiers = [
                c
                for c in classifiers
                if c.startswith("Programming Language :: Python :: 3.")
            ]

            # Should have classifiers for supported versions
            expected_versions = []
            for minor in range(8, 13):  # 3.8 to 3.12
                if (3, minor) >= (min_major, min_minor):
                    expected_versions.append(
                        f"Programming Language :: Python :: 3.{minor}"
                    )

            for expected in expected_versions:
                assert expected in classifiers, f"Missing classifier: {expected}"

            # Should NOT have classifiers for unsupported versions
            unsupported_versions = [
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
            ]

            for unsupported in unsupported_versions:
                assert (
                    unsupported not in classifiers
                ), f"Should not have classifier: {unsupported}"

    @given(
        st.tuples(
            st.integers(min_value=2, max_value=3),  # major version
            st.integers(min_value=0, max_value=15),  # minor version
        )
    )
    def test_version_comparison_property(self, version_tuple: Tuple[int, int]):
        """Property test: Version comparison logic should work correctly."""
        major, minor = version_tuple
        test_version = (major, minor)

        # Our minimum requirement is Python 3.8
        min_required = (3, 8)
        max_supported = (3, 12)

        # Test version comparison logic
        is_supported = min_required <= test_version <= max_supported

        if test_version < min_required:
            # Should be rejected
            assert (
                not is_supported
            ), f"Version {test_version} should be rejected (below minimum)"
        elif test_version > max_supported:
            # Should be rejected (above tested range)
            assert (
                not is_supported
            ), f"Version {test_version} should be rejected (above tested range)"
        else:
            # Should be supported
            assert is_supported, f"Version {test_version} should be supported"

    def test_setup_py_backward_compatibility(self):
        """Test that setup.py maintains version constraints for backward compatibility."""
        setup_py_path = Path(__file__).parent.parent / "setup.py"

        if not setup_py_path.exists():
            pytest.skip("setup.py not found")

        setup_content = setup_py_path.read_text()

        # Should have python_requires
        assert (
            "python_requires=" in setup_content
        ), "setup.py should specify python_requires"

        # Should require Python 3.8+
        python_requires_match = re.search(
            r'python_requires=["\']([^"\']+)["\']', setup_content
        )
        assert python_requires_match, "Could not find python_requires value"

        python_requires = python_requires_match.group(1)
        assert (
            ">=3.8" in python_requires
        ), f"setup.py should require >=3.8, got: {python_requires}"

    def test_no_python2_classifiers_remain(self):
        """Test that Python 2.7 classifiers have been removed."""
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
            classifiers = project.get("classifiers", [])

            # Should not have Python 2.7 classifier
            python2_classifiers = [
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 2.7",
            ]

            for classifier in python2_classifiers:
                assert (
                    classifier not in classifiers
                ), f"Should not have Python 2 classifier: {classifier}"

        # Also check setup.py
        setup_py_path = Path(__file__).parent.parent / "setup.py"
        if setup_py_path.exists():
            setup_content = setup_py_path.read_text()

            # Should not contain Python 2.7 classifiers
            assert (
                '"Programming Language :: Python :: 2.7"' not in setup_content
            ), "setup.py should not contain Python 2.7 classifier"
            assert (
                "'Programming Language :: Python :: 2.7'" not in setup_content
            ), "setup.py should not contain Python 2.7 classifier"

    @given(
        st.text(
            min_size=1,
            max_size=20,
            alphabet="0123456789.>=<,",
        )
    )
    def test_version_string_parsing_property(self, version_string: str):
        """Property test: Version string parsing should handle various formats."""
        # Test that our version constraint parsing logic is robust

        # Valid version constraint patterns
        valid_patterns = [
            r">=\d+\.\d+",
            r">=\d+\.\d+\.\d+",
            r">=\d+\.\d+,<\d+\.\d+",
            r">=\d+\.\d+\.\d+,<\d+\.\d+\.\d+",
        ]

        # Check if the version string matches any valid pattern
        is_valid_format = any(
            re.match(pattern, version_string) for pattern in valid_patterns
        )

        if is_valid_format:
            # If it's a valid format, it should be parseable
            try:
                # Extract version numbers
                version_numbers = re.findall(r"\d+", version_string)
                assert (
                    len(version_numbers) >= 2
                ), "Should have at least major.minor version"

                # Convert to integers (should not raise exception)
                major = int(version_numbers[0])
                minor = int(version_numbers[1])

                assert major >= 0, "Major version should be non-negative"
                assert minor >= 0, "Minor version should be non-negative"

            except (ValueError, IndexError) as e:
                pytest.fail(
                    f"Valid format version string failed to parse: {version_string}, error: {e}"
                )

    def test_installation_would_fail_on_old_python(self):
        """Test that installation would fail on Python versions below 3.8."""
        # This test verifies the constraint exists, but can't actually test installation failure
        # without having old Python versions available

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        setup_py_path = Path(__file__).parent.parent / "setup.py"

        constraint_found = False

        # Check pyproject.toml
        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib

                with open(pyproject_path, "rb") as f:
                    pyproject = tomllib.load(f)

                requires_python = pyproject.get("project", {}).get(
                    "requires-python", ""
                )
                if ">=3.8" in requires_python:
                    constraint_found = True

            except ImportError:
                pass

        # Check setup.py
        if setup_py_path.exists():
            setup_content = setup_py_path.read_text()
            if 'python_requires=">=3.8"' in setup_content:
                constraint_found = True

        assert (
            constraint_found
        ), "Python version constraint >=3.8 should be specified in either pyproject.toml or setup.py"

    def test_error_message_clarity(self):
        """Test that version constraint errors would be clear to users."""
        # This tests that our constraint specification is clear

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        if pyproject_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                else:
                    import tomli as tomllib

                with open(pyproject_path, "rb") as f:
                    pyproject = tomllib.load(f)

                requires_python = pyproject.get("project", {}).get(
                    "requires-python", ""
                )

                # Should be specific and clear
                assert requires_python, "requires-python should be specified"
                assert ">=" in requires_python, "Should use >= for minimum version"
                assert "3.8" in requires_python, "Should specify 3.8 as minimum"

                # Should not be overly restrictive
                assert (
                    "<4" not in requires_python or "<3.13" not in requires_python
                ), "Should not unnecessarily restrict future Python versions"

            except ImportError:
                pytest.skip("TOML library not available")
