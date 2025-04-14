#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration and fixtures for GitVersion.cmake test suite.
"""

import os
import sys
import pytest
from pathlib import Path

# Get the path to the project root directory
@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory as a Path object."""
    return Path(__file__).parent.parent.absolute()

# Get the path to the GitVersion.cmake file
@pytest.fixture(scope="session")
def gitversion_cmake_path(project_root):
    """Return the path to the GitVersion.cmake file."""
    return project_root / "cmake/GitVersion.cmake"

# Import git_environment fixture for creating temporary Git repos
@pytest.fixture
def git_env():
    """Create a temporary Git environment for testing."""
    from tests.utils.git_environment import GitEnvironment
    env = GitEnvironment()
    yield env
    # Cleanup happens automatically in GitEnvironment's __del__ method

# Import cmake_project fixture for creating temporary CMake projects
@pytest.fixture
def cmake_project(git_env, gitversion_cmake_path):
    """Create a temporary CMake project for testing."""
    from tests.utils.cmake_project import CMakeProject
    project = CMakeProject(git_env.root_dir, gitversion_cmake_path)
    return project 