#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake with exact version tags (pytest version).
"""

import pytest
from pathlib import Path

# Use pytest marker to mark this is a basic test
@pytest.mark.basic
def test_exact_tag_version(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with an exact tag."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag
    git_env.tag("1.2.3")
    
    # Create a CMake project and configure
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Verify version information
    assert version_info.get("PROJECT_VERSION") == "1.2.3", "Wrong project version"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version"

@pytest.mark.basic
def test_custom_prefix(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with a custom prefix."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag with a prefix
    git_env.tag("v1.2.3")
    
    # Create a CMake project with a prefix
    cmake_project.create_cmakelists()
    
    # Configure the project and get version info
    version_info = cmake_project.configure()
    
    # Verify version information
    assert version_info.get("PROJECT_VERSION") == "1.2.3", "Wrong project version"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version" 
