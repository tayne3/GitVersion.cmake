#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake FAIL_ON_MISMATCH option.
"""

import pytest
import subprocess
import re

@pytest.mark.edge_cases
def test_fail_on_mismatch_exact_match(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with an exact tag match."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")  # Exact version tag
    
    # Create a CMake project with FAIL_ON_MISMATCH and same DEFAULT_VERSION
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.3",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed because DEFAULT_VERSION matches the tag version
    version_info = cmake_project.configure()
    
    # Verify exact version match
    assert version_info.get("PROJECT_VERSION") == "1.2.3", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version"


@pytest.mark.edge_cases
def test_fail_on_mismatch_version_mismatch(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with a version mismatch."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")  # Exact version tag
    
    # Create a CMake project with FAIL_ON_MISMATCH and different DEFAULT_VERSION
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "2.0.0",  # Different from the actual tag
        "FAIL_ON_MISMATCH": True
    })
    
    # Should fail because DEFAULT_VERSION doesn't match the tag version
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        cmake_project.configure()
    
    # Check for the specific error message about version mismatch
    error_output = excinfo.value.stderr
    assert "CMake Error" in error_output, f"Missing CMake Error in output: {error_output}"
    assert "does not match Git tag" in error_output, f"Missing specific error message about version mismatch: {error_output}"
    assert "2.0.0" in error_output and "1.2.3" in error_output, f"Missing version numbers in error message: {error_output}"


@pytest.mark.edge_cases
def test_fail_on_mismatch_with_prefix(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with a tag prefix."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.2.3")  # Tag with prefix
    
    # Create a CMake project with FAIL_ON_MISMATCH, prefix, and matching DEFAULT_VERSION
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.3",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed because DEFAULT_VERSION matches the tag version (without prefix)
    version_info = cmake_project.configure()
    
    # Verify exact version match
    assert version_info.get("PROJECT_VERSION") == "1.2.3", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version"


@pytest.mark.edge_cases
def test_fail_on_mismatch_with_prefix_mismatch(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with a tag prefix but mismatched version."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.2.3")  # Tag with prefix
    
    # Create a CMake project with mismatched version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "2.0.0",  # Different from tag version
        "FAIL_ON_MISMATCH": True
    })
    
    # Should fail because of version mismatch
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        cmake_project.configure()
    
    # Check for the specific error message
    error_output = excinfo.value.stderr
    assert "CMake Error" in error_output, f"Missing CMake Error in output: {error_output}"
    assert "does not match Git tag" in error_output, f"Missing specific error message about version mismatch: {error_output}"
    assert "2.0.0" in error_output and "1.2.3" in error_output, f"Missing version numbers in error message: {error_output}"


@pytest.mark.edge_cases
def test_fail_on_mismatch_with_development_version(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with a development version (commits after tag)."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")  # Tag
    
    # Add another commit to create a development version
    git_env.create_file("file.txt", "content")
    git_env.commit("Another commit")
    
    # Create a CMake project where DEFAULT_VERSION equals the tag version
    # This should fail because with FAIL_ON_MISMATCH, DEFAULT_VERSION should be equal to the tag version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.1",  # Same as tag, but we're in dev version
        "FAIL_ON_MISMATCH": True
    })
    
    # Should fail since we're in development version but the DEFAULT_VERSION equals the tag
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        cmake_project.configure()
    
    # Check for the specific error message
    error_output = excinfo.value.stderr
    assert "CMake Error" in error_output, f"Missing CMake Error in output: {error_output}"
    assert "must be >= tagged ancestor" in error_output, f"Missing specific error about version needing to be equal: {error_output}"


@pytest.mark.edge_cases
def test_fail_on_mismatch_with_development_version_success(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH with development version and correct higher DEFAULT_VERSION."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")  # Tag
    
    # Add another commit to create a development version
    git_env.create_file("file.txt", "content")
    git_env.commit("Another commit")
    
    # Create a CMake project with DEFAULT_VERSION equal to the tag version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.3",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed as DEFAULT_VERSION is equal to the tag version
    version_info = cmake_project.configure()
    
    # The full version will include development info
    full_version = version_info.get("PROJECT_FULL_VERSION", "")
    assert full_version.startswith("1.2.3-dev."), f"Expected development version format not found: {full_version}"
    assert "+" in full_version, f"Missing commit hash in full version: {full_version}"


@pytest.mark.edge_cases
def test_no_tag_with_fail_on_mismatch(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with no tags present."""
    # Create files and commits but no tags
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a CMake project with FAIL_ON_MISMATCH
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.0.0",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed and use the DEFAULT_VERSION since there's no tag to mismatch with
    version_info = cmake_project.configure()
    
    # Check the full version format - new implementation adds commit hash even without tags
    full_version = version_info.get("PROJECT_FULL_VERSION", "")
    # Should have commit hash since there are commits but no tags
    assert full_version.startswith("1.0.0+"), f"Expected version with commit hash: {full_version}"
    
    # Check version components
    assert version_info.get("PROJECT_VERSION") == "1.0.0", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "0", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "0", "Wrong patch version"


@pytest.mark.edge_cases
def test_mixed_prefix_tags(git_env, cmake_project, gitversion_cmake_path):
    """Test with mixed prefix tags (both with and without prefix)."""
    # Create repo with two tags: one with prefix, one without
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")  # No prefix
    
    git_env.create_file("file.txt", "content")
    git_env.commit("Second commit")
    git_env.tag("v2.0.0")  # With prefix
    
    # Test with prefix matching
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "2.0.0",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should match v2.0.0 tag and succeed
    version_info = cmake_project.configure()
    assert version_info.get("PROJECT_VERSION") == "2.0.0", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"


@pytest.mark.edge_cases
def test_error_message_format(git_env, cmake_project, gitversion_cmake_path):
    """Test that the error message is properly formatted and contains key information."""
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")
    
    # Create a CMake project with mismatched version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "9.9.9",  # Very different from tag
        "FAIL_ON_MISMATCH": True
    })
    
    # Should fail with specific error message
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        cmake_project.configure()
    
    error_output = excinfo.value.stderr
    
    # Define regex pattern for expected error message
    error_pattern = r"CMake Error at.*GitVersion\.cmake.*message.*Project version \(9\.9\.9\).*does not match Git tag \(1\.2\.3\)"
    
    # Check with regex for a more structured error message validation
    assert re.search(error_pattern, error_output, re.DOTALL), f"Error message doesn't match expected format: {error_output}" 
