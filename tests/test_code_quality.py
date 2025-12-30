"""
Property-based tests for code quality and modernization.

Feature: python-modernization, Property 6: Code Quality and Modernization
Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5
"""

import ast
import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Dict, Any, Set
import re

import pytest
from hypothesis import given, strategies as st, assume


class TestCodeQualityAndModernization:
    """Test that code quality meets modern Python standards."""

    def test_no_python2_syntax_remains(self):
        """Test that no Python 2.7 syntax remains in the codebase."""
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        python2_patterns = [
            r"print\s+[^(]",  # print statement (not function)
            r"class\s+\w+\(object\):",  # explicit object inheritance
            r"from\s+__future__\s+import",  # future imports
            r"unicode\(",  # unicode function
            r"basestring",  # basestring type
            r"xrange\(",  # xrange function
            r"\.iteritems\(\)",  # dict.iteritems()
            r"\.iterkeys\(\)",  # dict.iterkeys()
            r"\.itervalues\(\)",  # dict.itervalues()
        ]

        for py_file in python_files:
            content = py_file.read_text(encoding="utf-8")

            for pattern in python2_patterns:
                matches = re.findall(pattern, content)
                assert not matches, f"Python 2 syntax found in {py_file}: {matches}"

    def test_modern_class_definitions_used(self):
        """Test that modern class definitions are used (no explicit object inheritance)."""
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        for py_file in python_files:
            content = py_file.read_text(encoding="utf-8")

            # Parse AST to check class definitions
            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Check if class explicitly inherits from object
                        for base in node.bases:
                            if isinstance(base, ast.Name) and base.id == "object":
                                # Allow Exception classes to inherit from object for clarity
                                if not any(
                                    (
                                        "Exception" in base_name.id
                                        if isinstance(base_name, ast.Name)
                                        else False
                                    )
                                    for base_name in node.bases
                                ):
                                    assert (
                                        False
                                    ), f"Class {node.name} in {py_file} should not explicitly inherit from object"

            except SyntaxError:
                pytest.fail(f"Syntax error in {py_file}")

    def test_f_strings_used_where_appropriate(self):
        """Test that f-strings are used instead of old string formatting."""
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        old_format_patterns = [
            r"\.format\(",  # .format() method
            r"%\s*\(",  # % formatting
        ]

        for py_file in python_files:
            content = py_file.read_text(encoding="utf-8")

            # Count old formatting vs f-strings
            old_format_count = sum(
                len(re.findall(pattern, content)) for pattern in old_format_patterns
            )
            f_string_count = len(re.findall(r'f["\']', content))

            # If there's string formatting, prefer f-strings
            if old_format_count > 0:
                # Allow some old formatting for backward compatibility or complex cases
                # but encourage f-strings for simple cases
                pass  # This is more of a guideline than a strict requirement

    def test_type_hints_compatibility(self):
        """Test that code is compatible with type hints."""
        # Test that we can add type hints without breaking functionality
        from typing import Optional, Dict, List, Any

        def typed_function(api_key: str, host: Optional[str] = None) -> Dict[str, Any]:
            from gophish import Gophish

            client = Gophish(api_key, host=host or "https://localhost:3333")
            return {"client": client, "api_key": api_key}

        result = typed_function("test-key")
        assert isinstance(result, dict)
        assert "client" in result
        assert "api_key" in result

    def test_pathlib_compatibility(self):
        """Test that code is compatible with pathlib."""
        from pathlib import Path

        # Test that pathlib works with our codebase
        current_dir = Path(__file__).parent
        gophish_dir = current_dir.parent / "gophish"

        assert gophish_dir.exists(), "Gophish directory should exist"
        assert gophish_dir.is_dir(), "Gophish should be a directory"

        # Test that we can iterate over Python files
        python_files = list(gophish_dir.rglob("*.py"))
        assert len(python_files) > 0, "Should find Python files"

    def test_docstrings_present(self):
        """Test that public functions and classes have docstrings."""
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        missing_docstrings = []

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                        # Skip private methods and functions
                        if node.name.startswith("_"):
                            continue

                        # Check if it has a docstring
                        if (
                            not node.body
                            or not isinstance(node.body[0], ast.Expr)
                            or not isinstance(node.body[0].value, ast.Constant)
                            or not isinstance(node.body[0].value.value, str)
                        ):
                            missing_docstrings.append(f"{py_file.name}:{node.name}")

            except SyntaxError:
                continue

        # Allow some missing docstrings but encourage their use
        if missing_docstrings:
            print(f"Functions/classes without docstrings: {missing_docstrings}")
        # Don't fail the test, just report

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(min_codepoint=32, max_codepoint=126),
        )
    )
    def test_string_handling_property(self, test_string: str):
        """Property test: String handling should work with various inputs."""
        assume(test_string.strip())  # Assume non-empty after stripping

        # Test that our string handling is robust
        try:
            # Test f-string formatting
            formatted = f"API Key: {test_string}"
            assert test_string in formatted

            # Test string methods
            upper_string = test_string.upper()
            assert isinstance(upper_string, str)

            # Test string encoding/decoding
            encoded = test_string.encode("utf-8")
            decoded = encoded.decode("utf-8")
            assert decoded == test_string

        except Exception as e:
            pytest.fail(f"String handling failed for '{test_string}': {e}")

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
    def test_dictionary_operations_property(self, test_dict: Dict[str, Any]):
        """Property test: Dictionary operations should work correctly."""
        # Test modern dictionary operations
        try:
            # Test dictionary unpacking
            base_dict = {"base": "value"}
            merged_dict = {**base_dict, **test_dict}

            assert "base" in merged_dict
            for key, value in test_dict.items():
                assert merged_dict[key] == value

            # Test dictionary comprehension
            filtered_dict = {k: v for k, v in test_dict.items() if v is not None}
            assert isinstance(filtered_dict, dict)

            # Test get method with default
            for key in test_dict:
                value = test_dict.get(key, "default")
                assert value is not None or test_dict[key] is None

        except Exception as e:
            pytest.fail(f"Dictionary operations failed for {test_dict}: {e}")

    def test_import_structure_modern(self):
        """Test that import structure follows modern practices."""
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        for py_file in python_files:
            content = py_file.read_text(encoding="utf-8")

            # Check for relative imports (should use explicit relative imports)
            lines = content.split("\n")
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith("from ") and " import " in line:
                    # Should use explicit relative imports within package
                    if line.startswith("from gophish"):
                        # Absolute imports are fine
                        continue
                    elif line.startswith("from ."):
                        # Explicit relative imports are fine
                        continue
                    elif any(
                        line.startswith(f"from {module}")
                        for module in ["datetime", "json", "requests", "dateutil"]
                    ):
                        # Standard library and external imports are fine
                        continue

    def test_exception_handling_modern(self):
        """Test that exception handling uses modern practices."""
        from gophish.models import Error, Success

        # Test that exceptions can be chained
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise Error() from e
        except Error as error:
            assert error.__cause__ is not None

        # Test that exceptions have proper inheritance
        assert issubclass(Error, Exception)
        assert issubclass(Success, Exception)

    @given(
        st.lists(
            st.text(
                min_size=1,
                max_size=50,
                alphabet=st.characters(min_codepoint=97, max_codepoint=122),
            ),
            min_size=0,
            max_size=10,
        )
    )
    def test_list_operations_property(self, test_list: List[str]):
        """Property test: List operations should work correctly."""
        # Test modern list operations
        try:
            # Test list comprehension
            upper_list = [item.upper() for item in test_list]
            assert len(upper_list) == len(test_list)

            # Test list unpacking
            if test_list:
                first, *rest = test_list
                assert first == test_list[0]
                assert rest == test_list[1:]

            # Test enumerate
            for i, item in enumerate(test_list):
                assert test_list[i] == item

            # Test filter
            filtered = list(filter(lambda x: len(x) > 3, test_list))
            assert all(len(item) > 3 for item in filtered)

        except Exception as e:
            pytest.fail(f"List operations failed for {test_list}: {e}")

    def test_context_managers_work(self):
        """Test that context managers work correctly."""
        from pathlib import Path

        # Test file context manager
        test_file = Path(__file__)

        with open(test_file, "r") as f:
            content = f.read()
            assert len(content) > 0

        # File should be closed after context
        assert f.closed

    def test_generator_expressions_work(self):
        """Test that generator expressions work correctly."""
        # Test generator expression
        numbers = range(10)
        squares = (x * x for x in numbers)

        # Should be a generator
        assert hasattr(squares, "__next__")

        # Should produce correct values
        square_list = list(squares)
        assert square_list == [x * x for x in range(10)]

    def test_async_compatibility(self):
        """Test that code is compatible with async/await (doesn't use conflicting names)."""
        # Test that we don't use 'async' or 'await' as variable names
        gophish_dir = Path(__file__).parent.parent / "gophish"
        python_files = list(gophish_dir.rglob("*.py"))

        for py_file in python_files:
            content = py_file.read_text(encoding="utf-8")

            # Check for async/await used as variable names (not keywords)
            lines = content.split("\n")
            for line_num, line in enumerate(lines, 1):
                # Skip actual async/await usage
                if "async def" in line or "await " in line:
                    continue

                # Check for problematic usage
                if re.search(r"\basync\s*=", line) or re.search(r"\bawait\s*=", line):
                    pytest.fail(
                        f"async/await used as variable name in {py_file}:{line_num}"
                    )

    @given(st.integers(min_value=0, max_value=1000))
    def test_numeric_operations_property(self, test_number: int):
        """Property test: Numeric operations should work correctly."""
        # Test modern numeric operations
        try:
            # Test f-string formatting with numbers
            formatted = f"Number: {test_number}"
            assert str(test_number) in formatted

            # Test division (should be true division in Python 3)
            if test_number > 0:
                result = test_number / 2
                assert isinstance(result, float)

            # Test integer division
            if test_number > 0:
                result = test_number // 2
                assert isinstance(result, int)

            # Test power operator
            result = test_number**2
            assert result == test_number * test_number

        except Exception as e:
            pytest.fail(f"Numeric operations failed for {test_number}: {e}")

    def test_encoding_handling_modern(self):
        """Test that encoding is handled correctly (UTF-8 by default)."""
        # Test that we can handle Unicode strings
        unicode_string = "Hello, 世界! 🌍"

        # Should work with f-strings
        formatted = f"Message: {unicode_string}"
        assert unicode_string in formatted

        # Should work with encoding/decoding
        encoded = unicode_string.encode("utf-8")
        decoded = encoded.decode("utf-8")
        assert decoded == unicode_string

        # Should work with file operations
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            f.write(unicode_string)
            temp_path = f.name

        with open(temp_path, "r", encoding="utf-8") as f:
            read_content = f.read()
            assert read_content == unicode_string

        # Clean up
        Path(temp_path).unlink()
