#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake dirty state detection functionality.
"""

import pytest

# Use pytest marker to mark this as an advanced test
@pytest.mark.advanced
def test_clean_tagged_version(git_env, cmake_project):
    """Test version extraction from a clean tagged commit."""
    # Create initial commit
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create CMake project files and commit them first
    cmake_project.create_cmakelists({"INCLUDE_EXTENDED": True})
    cmake_project.commit_project_files(git_env)  # Commit cmake files
    
    # Create a tag AFTER committing cmake files
    git_env.tag("v1.2.3")
    
    version_info = cmake_project.configure()
    
    # Verify basic version information
    assert version_info.get("PROJECT_VERSION") == "1.2.3", "Wrong project version"
    assert version_info.get("PROJECT_FULL_VERSION") == "1.2.3", "Wrong full version"
    assert version_info.get("MAJOR_MACRO") == "1", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "2", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "3", "Wrong patch version"
    
    # Verify extended information
    assert version_info.get("PROJECT_IS_DIRTY") == False, "Should not be dirty"
    assert version_info.get("PROJECT_IS_TAGGED") == True, "Should be tagged"
    assert version_info.get("PROJECT_IS_DEVELOPMENT") == False, "Should not be development"
    assert version_info.get("PROJECT_TAG_NAME") == "v1.2.3", "Wrong tag name"

@pytest.mark.advanced
def test_dirty_tagged_version(git_env, cmake_project):
    """Test version extraction from a dirty tagged commit."""
    # Create initial commit
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Create a tag
    git_env.tag("v2.1.0")
    
    # Modify a file without committing (make it dirty)
    git_env.modify_file("README.md", "\n# Modified content")
    
    # Verify repository is dirty
    assert git_env.is_dirty() == True, "Repository should be dirty"
    
    # Create CMake project with extended parameters
    cmake_project.create_cmakelists({"INCLUDE_EXTENDED": True})
    version_info = cmake_project.configure()
    
    # Verify basic version information
    assert version_info.get("PROJECT_VERSION") == "2.1.0", "Wrong project version"
    assert version_info.get("PROJECT_FULL_VERSION") == "2.1.0-dirty", "Full version should include -dirty"
    assert version_info.get("MAJOR_MACRO") == "2", "Wrong major version"
    assert version_info.get("MINOR_MACRO") == "1", "Wrong minor version"
    assert version_info.get("PATCH_MACRO") == "0", "Wrong patch version"
    
    # Verify extended information
    assert version_info.get("PROJECT_IS_DIRTY") == True, "Should be dirty"
    assert version_info.get("PROJECT_IS_TAGGED") == True, "Should be tagged"
    assert version_info.get("PROJECT_IS_DEVELOPMENT") == False, "Should not be development"

@pytest.mark.advanced
def test_clean_development_version(git_env, cmake_project):
    """Test version extraction from a clean development commit."""
    # Create initial commit and tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v1.5.2")
    
    # Add another commit (development version)
    git_env.create_file("feature.txt", "New feature")
    git_env.commit("Add new feature")
    
    # Create CMake project with extended parameters and commit to keep repo clean
    cmake_project.create_cmakelists({"INCLUDE_EXTENDED": True})
    cmake_project.commit_project_files(git_env)
    version_info = cmake_project.configure()
    
    # Verify basic version information
    assert version_info.get("PROJECT_VERSION") == "1.5.2", "Wrong project version"
    
    # Full version should be development format (2 commits after tag: feature + cmake files)
    full_version = version_info.get("PROJECT_FULL_VERSION")
    assert full_version.startswith("1.5.2-dev.2+"), f"Expected development version, got: {full_version}"
    assert "-dirty" not in full_version, f"Clean version should not have -dirty: {full_version}"
    
    # Verify extended information
    assert version_info.get("PROJECT_IS_DIRTY") == False, "Should not be dirty"
    assert version_info.get("PROJECT_IS_TAGGED") == False, "Should not be tagged"
    assert version_info.get("PROJECT_IS_DEVELOPMENT") == True, "Should be development"

@pytest.mark.advanced
def test_dirty_development_version(git_env, cmake_project):
    """Test version extraction from a dirty development commit."""
    # Create initial commit and tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("v3.0.1")
    
    # Add another commit (development version)
    git_env.create_file("feature.txt", "New feature")
    git_env.commit("Add new feature")
    
    # Modify a file without committing (make it dirty)
    git_env.modify_file("feature.txt", "\n# Work in progress")
    
    # Verify repository is dirty
    assert git_env.is_dirty() == True, "Repository should be dirty"
    
    # Create CMake project with extended parameters
    cmake_project.create_cmakelists({"INCLUDE_EXTENDED": True})
    version_info = cmake_project.configure()
    
    # Verify basic version information
    assert version_info.get("PROJECT_VERSION") == "3.0.1", "Wrong project version"
    
    # Full version should be dirty development format
    full_version = version_info.get("PROJECT_FULL_VERSION")
    assert full_version.startswith("3.0.1-dev.1+"), f"Expected development version, got: {full_version}"
    assert full_version.endswith(".dirty"), f"Dirty development version should end with .dirty: {full_version}"
    
    # Verify extended information
    assert version_info.get("PROJECT_IS_DIRTY") == True, "Should be dirty"
    assert version_info.get("PROJECT_IS_TAGGED") == False, "Should not be tagged"
    assert version_info.get("PROJECT_IS_DEVELOPMENT") == True, "Should be development"

@pytest.mark.advanced
def test_no_tags_dirty_version(git_env, cmake_project):
    """Test version extraction from a repository with no tags but dirty state."""
    # Create initial commit but no tag
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    
    # Modify file to make it dirty
    git_env.modify_file("README.md", "\n# Modified")
    assert git_env.is_dirty() == True, "Repository should be dirty"
    
    # Create CMake project with extended parameters
    cmake_project.create_cmakelists({"INCLUDE_EXTENDED": True})
    version_info = cmake_project.configure()
    
    # Should use default version with commit hash and dirty suffix
    assert version_info.get("PROJECT_VERSION") == "0.0.0", "Wrong project version"
    
    full_version = version_info.get("PROJECT_FULL_VERSION")
    assert full_version.startswith("0.0.0+"), f"Expected version with commit hash, got: {full_version}"
    assert full_version.endswith(".dirty"), f"Dirty version should end with .dirty: {full_version}"
    
    # Verify extended information
    assert version_info.get("PROJECT_IS_DIRTY") == True, "Should be dirty"
    assert version_info.get("PROJECT_IS_TAGGED") == False, "Should not be tagged"
    assert version_info.get("PROJECT_IS_DEVELOPMENT") == False, "Should not be development (no tags)"
