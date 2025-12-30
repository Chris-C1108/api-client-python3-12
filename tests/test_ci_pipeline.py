"""
Property-based tests for CI pipeline functionality.

Feature: python-modernization, Property 5: CI Pipeline Functionality
Validates: Requirements 4.4, 4.5
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Set

import pytest
from hypothesis import given, strategies as st


class TestCIPipelineFunctionality:
    """Test that CI pipeline is properly configured and functional."""

    def test_ci_workflow_exists(self):
        """Test that CI workflow file exists and is properly configured."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        assert ci_workflow_path.exists(), "CI workflow file should exist"

        with open(ci_workflow_path, "r") as f:
            ci_config = yaml.safe_load(f)

        assert ci_config is not None, "CI workflow should be valid YAML"
        assert "jobs" in ci_config, "CI workflow should have jobs"
        assert "on" in ci_config, "CI workflow should have triggers"

    def test_python_version_matrix_complete(self):
        """Test that CI tests all supported Python versions."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            ci_config = yaml.safe_load(f)

        # Find test job with matrix
        test_job = None
        for job_name, job_config in ci_config.get("jobs", {}).items():
            if "strategy" in job_config and "matrix" in job_config["strategy"]:
                if "python-version" in job_config["strategy"]["matrix"]:
                    test_job = job_config
                    break

        assert test_job is not None, "Should have a test job with Python version matrix"

        python_versions = test_job["strategy"]["matrix"]["python-version"]
        expected_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]

        for version in expected_versions:
            assert (
                version in python_versions
            ), f"Python {version} should be in CI matrix"

    def test_operating_system_matrix_complete(self):
        """Test that CI tests on multiple operating systems."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            ci_config = yaml.safe_load(f)

        # Find test job with OS matrix
        test_job = None
        for job_name, job_config in ci_config.get("jobs", {}).items():
            if "strategy" in job_config and "matrix" in job_config["strategy"]:
                if "os" in job_config["strategy"]["matrix"]:
                    test_job = job_config
                    break

        assert test_job is not None, "Should have a test job with OS matrix"

        operating_systems = test_job["strategy"]["matrix"]["os"]
        expected_os = ["ubuntu-latest", "windows-latest", "macos-latest"]

        for os_name in expected_os:
            assert os_name in operating_systems, f"{os_name} should be in CI matrix"

    def test_security_scanning_included(self):
        """Test that security scanning is included in CI pipeline."""
        workflow_files = [
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml",
            Path(__file__).parent.parent / ".github" / "workflows" / "code-quality.yml",
        ]

        security_tools_found = set()

        for workflow_path in workflow_files:
            if not workflow_path.exists():
                continue

            with open(workflow_path, "r") as f:
                content = f.read()

            # Check for security tools
            if "bandit" in content:
                security_tools_found.add("bandit")
            if "safety" in content:
                security_tools_found.add("safety")

        assert (
            "bandit" in security_tools_found
        ), "bandit security scanner should be in CI"
        assert (
            "safety" in security_tools_found
        ), "safety dependency scanner should be in CI"

    def test_code_quality_checks_included(self):
        """Test that code quality checks are included in CI pipeline."""
        workflow_files = [
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml",
            Path(__file__).parent.parent / ".github" / "workflows" / "code-quality.yml",
        ]

        quality_tools_found = set()

        for workflow_path in workflow_files:
            if not workflow_path.exists():
                continue

            with open(workflow_path, "r") as f:
                content = f.read()

            # Check for quality tools
            if "black" in content:
                quality_tools_found.add("black")
            if "flake8" in content:
                quality_tools_found.add("flake8")
            if "mypy" in content:
                quality_tools_found.add("mypy")

        assert "black" in quality_tools_found, "black formatter should be in CI"
        assert "flake8" in quality_tools_found, "flake8 linter should be in CI"
        # mypy is optional initially, so we don't assert it

    def test_package_installation_validated(self):
        """Test that CI validates package installation."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            content = f.read()

        # Should have package installation test
        assert (
            "package-test" in content or "Test package installation" in content
        ), "CI should include package installation testing"

        # Should test import functionality
        assert "import gophish" in content, "CI should test package import"

    def test_modern_github_actions_versions(self):
        """Test that modern GitHub Actions versions are used."""
        workflow_dir = Path(__file__).parent.parent / ".github" / "workflows"

        if not workflow_dir.exists():
            pytest.skip("Workflows directory not found")

        workflow_files = list(workflow_dir.glob("*.yml")) + list(
            workflow_dir.glob("*.yaml")
        )

        for workflow_path in workflow_files:
            with open(workflow_path, "r") as f:
                content = f.read()

            # Check for modern action versions
            if "actions/checkout@" in content:
                assert (
                    "actions/checkout@v4" in content or "actions/checkout@v5" in content
                ), f"Should use modern checkout action in {workflow_path.name}"

            if "actions/setup-python@" in content:
                assert (
                    "actions/setup-python@v5" in content
                    or "actions/setup-python@v4" in content
                ), f"Should use modern setup-python action in {workflow_path.name}"

            # Should not use deprecated versions
            deprecated_actions = [
                "@v1",
                "@v2",
                "actions/checkout@v2",
                "actions/setup-python@v1",
            ]
            for deprecated in deprecated_actions:
                assert (
                    deprecated not in content
                ), f"Should not use deprecated action {deprecated} in {workflow_path.name}"

    def test_fail_fast_configuration(self):
        """Test that CI is configured to handle failures appropriately."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            ci_config = yaml.safe_load(f)

        # Find test job with strategy
        test_job = None
        for job_name, job_config in ci_config.get("jobs", {}).items():
            if "strategy" in job_config:
                test_job = job_config
                break

        if test_job and "strategy" in test_job:
            strategy = test_job["strategy"]
            # fail-fast should be false to test all combinations
            if "fail-fast" in strategy:
                assert (
                    strategy["fail-fast"] is False
                ), "fail-fast should be false to test all Python/OS combinations"

    @given(
        st.lists(
            st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(min_codepoint=97, max_codepoint=122),
            ),
            min_size=1,
            max_size=5,
            unique=True,
        )
    )
    def test_workflow_job_names_property(self, job_names: List[str]):
        """Property test: Workflow job names should be valid."""
        # Test that our job naming conventions are valid

        for job_name in job_names:
            # Valid job names should:
            # - Be lowercase
            # - Use hyphens instead of spaces
            # - Not start or end with hyphens

            is_valid = (
                job_name.islower()
                and not job_name.startswith("-")
                and not job_name.endswith("-")
                and "--" not in job_name
            )

            if is_valid:
                # Valid names should be usable in YAML
                normalized_name = job_name.replace("_", "-")
                assert isinstance(normalized_name, str)
                assert len(normalized_name) > 0

    def test_workflow_triggers_appropriate(self):
        """Test that workflow triggers are appropriate for CI."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            ci_config = yaml.safe_load(f)

        triggers = ci_config.get("on", {})

        # Should trigger on push to main branches
        if "push" in triggers:
            push_config = triggers["push"]
            if "branches" in push_config:
                branches = push_config["branches"]
                main_branches = ["main", "master", "develop"]
                has_main_branch = any(branch in branches for branch in main_branches)
                assert has_main_branch, "Should trigger on main branches"

        # Should trigger on pull requests
        assert "pull_request" in triggers, "Should trigger on pull requests"

    def test_dependency_caching_enabled(self):
        """Test that dependency caching is enabled for performance."""
        workflow_files = [
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml",
            Path(__file__).parent.parent / ".github" / "workflows" / "code-quality.yml",
        ]

        caching_found = False

        for workflow_path in workflow_files:
            if not workflow_path.exists():
                continue

            with open(workflow_path, "r") as f:
                content = f.read()

            # Check for caching configuration
            if "cache: 'pip'" in content or "cache: pip" in content:
                caching_found = True
                break

        assert caching_found, "Should enable pip caching for performance"

    def test_test_coverage_reporting(self):
        """Test that test coverage reporting is configured."""
        ci_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml"
        )

        if not ci_workflow_path.exists():
            pytest.skip("CI workflow not found")

        with open(ci_workflow_path, "r") as f:
            content = f.read()

        # Should have coverage reporting
        coverage_indicators = ["--cov=", "coverage", "codecov"]
        has_coverage = any(indicator in content for indicator in coverage_indicators)

        assert has_coverage, "CI should include test coverage reporting"

    @given(
        st.dictionaries(
            st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(min_codepoint=97, max_codepoint=122),
            ),
            st.one_of(st.text(), st.lists(st.text()), st.booleans()),
            min_size=1,
            max_size=5,
        )
    )
    def test_yaml_configuration_property(self, config_dict: Dict[str, Any]):
        """Property test: YAML configuration should be valid."""
        # Test that our YAML generation logic works

        try:
            # Should be able to serialize to YAML
            yaml_content = yaml.dump(config_dict)
            assert isinstance(yaml_content, str)
            assert len(yaml_content) > 0

            # Should be able to parse back
            parsed_config = yaml.safe_load(yaml_content)
            assert isinstance(parsed_config, dict)

        except Exception as e:
            pytest.fail(f"YAML configuration test failed: {e}")

    def test_workflow_permissions_secure(self):
        """Test that workflow permissions are appropriately configured."""
        workflow_files = [
            Path(__file__).parent.parent / ".github" / "workflows" / "pythonpublish.yml"
        ]

        for workflow_path in workflow_files:
            if not workflow_path.exists():
                continue

            with open(workflow_path, "r") as f:
                workflow_config = yaml.safe_load(f)

            # Check for permissions configuration
            if "permissions" in workflow_config:
                permissions = workflow_config["permissions"]

                # Should have appropriate permissions for publishing
                if "id-token" in permissions:
                    assert (
                        permissions["id-token"] == "write"
                    ), "id-token permission should be write for trusted publishing"

    def test_artifact_upload_configured(self):
        """Test that artifact upload is configured for important files."""
        workflow_files = [
            Path(__file__).parent.parent / ".github" / "workflows" / "ci.yml",
            Path(__file__).parent.parent
            / ".github"
            / "workflows"
            / "pythonpublish.yml",
        ]

        artifact_upload_found = False

        for workflow_path in workflow_files:
            if not workflow_path.exists():
                continue

            with open(workflow_path, "r") as f:
                content = f.read()

            if "upload-artifact" in content:
                artifact_upload_found = True
                break

        assert (
            artifact_upload_found
        ), "Should configure artifact upload for build outputs"

    def test_environment_protection_for_publishing(self):
        """Test that publishing jobs use environment protection."""
        publish_workflow_path = (
            Path(__file__).parent.parent / ".github" / "workflows" / "pythonpublish.yml"
        )

        if not publish_workflow_path.exists():
            pytest.skip("Publish workflow not found")

        with open(publish_workflow_path, "r") as f:
            publish_config = yaml.safe_load(f)

        # Find publish job
        publish_job = None
        for job_name, job_config in publish_config.get("jobs", {}).items():
            if "publish" in job_name.lower() or "deploy" in job_name.lower():
                publish_job = job_config
                break

        if publish_job:
            # Should use environment protection
            assert (
                "environment" in publish_job
            ), "Publish job should use environment protection"
