#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake FAIL_ON_MISMATCH option.
"""

import pytest
import subprocess
from pathlib import Path


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
    
    # Version might include hash suffix, so check if it starts with the expected version
    assert version_info.get("PROJECT_VERSION").startswith("1.2.3"), f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
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
    
    # Check if the error message contains relevant information about the mismatch
    assert "CMake Error" in excinfo.value.stderr or "FAIL_ON_MISMATCH" in excinfo.value.stderr


@pytest.mark.edge_cases
def test_fail_on_mismatch_with_prefix(git_env, cmake_project, gitversion_cmake_path):
    """Test FAIL_ON_MISMATCH option with a tag prefix."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.2.3")  # Tag with prefix
    
    # Create a CMake project with FAIL_ON_MISMATCH, prefix, and matching DEFAULT_VERSION
    cmake_project.create_cmakelists({
        "PREFIX": "v",
        "DEFAULT_VERSION": "1.2.3",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed because DEFAULT_VERSION matches the tag version (without prefix)
    version_info = cmake_project.configure()
    
    # Version might include hash suffix, so check if it starts with the expected version
    assert version_info.get("PROJECT_VERSION").startswith("1.2.3"), f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version"


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
    
    # Create a CMake project with FAIL_ON_MISMATCH
    # The DEFAULT_VERSION matches the tag but we're in a development version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.3",
        "PREFIX": "v",
        "FAIL_ON_MISMATCH": True
    })
    
    # Should succeed but the version will include development info (commit count, hash)
    version_info = cmake_project.configure()
    
    # The PROJECT_VERSION will still be 1.2.3 due to regex in the CMakeLists.txt
    assert version_info.get("PROJECT_VERSION").startswith("1.2.3"), f"Wrong project version: {version_info.get('PROJECT_VERSION')}"


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
    
    # Version might contain a hash suffix when there are no tags
    assert version_info.get("PROJECT_VERSION").startswith("1.0.0"), f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "0", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "0", "Wrong patch version" 
