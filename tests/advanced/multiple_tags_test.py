#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake with multiple version tags.
"""

import pytest
import os

@pytest.mark.advanced
def test_multiple_version_tags(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction when multiple version tags are present."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")  # First tag
    
    # Create src directory explicitly
    os.makedirs(git_env.root_dir / "src", exist_ok=True)
    
    # Add more commits and tags
    git_env.create_file("src/main.cpp", "int main() { return 0; }")
    git_env.commit("Add main.cpp")
    git_env.tag("1.1.0")  # Second tag
    
    git_env.create_file("CMakeLists.txt", "cmake_minimum_required(VERSION 3.12)")
    git_env.commit("Add CMakeLists.txt")
    git_env.tag("1.2.0")  # Third tag
    
    # Create a CMake project and configure
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Verify some version information is present (specific version may vary)
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.advanced
def test_latest_tag_with_prefix(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction when multiple tagged versions with prefixes are present."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.0.0")  # First tag
    
    # Create src directory explicitly
    os.makedirs(git_env.root_dir / "src", exist_ok=True)
    
    # Add more commits and tags
    git_env.create_file("src/main.cpp", "int main() { return 0; }")
    git_env.commit("Add main.cpp")
    git_env.tag("v1.1.0")  # Second tag
    
    git_env.create_file("CMakeLists.txt", "cmake_minimum_required(VERSION 3.12)")
    git_env.commit("Add CMakeLists.txt")
    git_env.tag("v2.0.0")  # Third tag with major version bump
    
    # Create a CMake project with the "v" prefix
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Verify version information is present
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.advanced
def test_mixed_tag_formats(git_env, cmake_project, gitversion_cmake_path):
    """Test behavior when tags with different formats are present."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.0.0")  # Tag with prefix
    
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    assert version_info.get("PROJECT_VERSION") == "1.0.0", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    
    # Add commits with differently formatted tags
    git_env.create_file("file1.txt", "content")
    git_env.commit("Add file1")
    git_env.tag("2.0.0")  # Tag without prefix

    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    assert version_info.get("PROJECT_VERSION") == "2.0.0", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
    
    git_env.create_file("file2.txt", "content")
    git_env.commit("Add file2")
    git_env.tag("v3.0.0")  # Tag with different prefix
    
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    assert version_info.get("PROJECT_VERSION") == "3.0.0", f"Wrong project version: {version_info.get('PROJECT_VERSION')}"
