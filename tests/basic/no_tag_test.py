#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake when no tag is present.
"""

import pytest

# Use pytest marker to mark this as a basic test
@pytest.mark.basic
def test_no_tag(git_env, cmake_project):
    """Test version extraction when no tag is present."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a CMake project with a default version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.0.0"
    })
    
    # Configure the project and get version info
    version_info = cmake_project.configure()
    
    # Verify version information
    version = version_info.get("PROJECT_VERSION")
    assert version.startswith("1.0.0"), f"Version should start with 1.0.0, got {version}"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "0", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "0", "Wrong patch version"

@pytest.mark.basic
def test_no_tag_custom_default_version(git_env, cmake_project):
    """Test version extraction when no tag is present with a custom default version."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a CMake project with a custom default version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "2.3.4"
    })
    
    # Configure the project and get version info
    version_info = cmake_project.configure()
    
    # Verify version information
    version = version_info.get("PROJECT_VERSION")
    assert version.startswith("2.3.4"), f"Version should start with 2.3.4, got {version}"
    assert version_info.get("MAJOR_MACRO") == "2", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "3", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "4", "Wrong patch version" 
