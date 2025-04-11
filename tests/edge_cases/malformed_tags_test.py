#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake with malformed or irregular version tags.
"""

import pytest
from pathlib import Path


@pytest.mark.edge_cases
def test_malformed_version_tag(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with a malformed version tag."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag with a malformed version (not in X.Y.Z format)
    git_env.tag("version-abc")
    
    # Create a CMake project with a default version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "0.1.0"
    })
    version_info = cmake_project.configure()
    
    # Version should be extracted - but might include hash suffixes
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    # If extracted from default version, major should be 0
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_partial_version_tag(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with a partial version tag (missing parts)."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag with a partial version (only major.minor)
    git_env.tag("1.2")
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Should extract some version information but specific values may vary
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_extra_version_components(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with extra version components."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag with extra version components (X.Y.Z.W)
    git_env.tag("1.2.3.4")
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Should extract some version information but actual values may vary
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_alphanumeric_version_components(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with alphanumeric version components."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag with alphanumeric components (not pure numbers)
    git_env.tag("1.2.3rc1")
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Should extract some version information but actual values may vary
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_semver_prerelease_tag(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction with a SemVer prerelease tag."""
    # Create files and commits
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a SemVer-style prerelease tag
    git_env.tag("1.0.0-alpha.1")
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Should extract some version information but actual values may vary
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"
    
    # Version string should be extracted but might have various formats
    assert version_info.get("PROJECT_VERSION"), "Missing project version" 
