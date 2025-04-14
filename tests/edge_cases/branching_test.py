#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake with complex branching scenarios.
"""

import pytest

@pytest.mark.edge_cases
def test_feature_branch_version(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction on a feature branch with no tags."""
    # Create main branch with a tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")
    
    # Create a feature branch
    git_env.checkout("feature/new-feature", create=True)
    git_env.create_file("feature.txt", "New feature")
    git_env.commit("Add feature")
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Check that a version was extracted - specific values might vary
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_multiple_branches_with_tags(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction when multiple branches have different tags."""
    # Create main branch with a tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")
    
    # Create a release branch with different version
    git_env.checkout("release/2.0", create=True)
    git_env.create_file("CHANGELOG.md", "# Changelog")
    git_env.commit("Add changelog")
    git_env.tag("2.0.0-rc.1")  # RC tag on release branch
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Check that a version was extracted - specific values might vary
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"
    
    # Switch back to main branch
    git_env.checkout("master")
    
    # Create a new CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Check that a version was extracted
    assert version_info.get("PROJECT_VERSION"), "Missing project version"


@pytest.mark.edge_cases
def test_branch_with_no_tags(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction on a branch with no tags."""
    # Create main branch with a tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")
    
    # Create an orphan branch with no tags
    git_env.checkout("orphan", create=True)
    git_env.create_file("orphan.txt", "Orphan branch")
    git_env.commit("Initial commit on orphan branch")
    
    # Create a CMake project with a default version
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "0.0.0"
    })
    version_info = cmake_project.configure()
    
    # Check that version info was extracted - values may include development info
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version"


@pytest.mark.edge_cases
def test_detached_head_state(git_env, cmake_project, gitversion_cmake_path):
    """Test version extraction in a detached HEAD state."""
    # Create main branch with commits and tags
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.0.0")
    
    # Add more commits and tag
    git_env.create_file("file.txt", "Content")
    first_commit = git_env.commit("Add file")
    
    git_env.create_file("another.txt", "More content")
    git_env.commit("Add another file")
    git_env.tag("1.1.0")
    
    # Checkout a specific commit (detached HEAD)
    git_env.checkout(first_commit)
    
    # Create a CMake project
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Check that version info was extracted
    assert version_info.get("PROJECT_VERSION"), "Missing project version"
    assert version_info.get("MAJOR_MACRO"), "Missing major version"
    assert version_info.get("MINOR_MACRO"), "Missing minor version"
    assert version_info.get("PATCH_MACRO"), "Missing patch version" 
