#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for GitVersion.cmake when no tag is present.
"""

import os
import unittest
from pathlib import Path

from tests.utils.git_environment import GitEnvironment
from tests.utils.cmake_project import CMakeProject


class NoTagTest(unittest.TestCase):
    """Test version extraction when no tag is present."""
    
    def setUp(self):
        """Set up the test environment."""
        # Find the path to GitVersion.cmake
        script_dir = Path(__file__).parent.parent.parent
        self.gitversion_path = script_dir / "GitVersion.cmake"
        
        # Create a temporary directory for the test
        self.git_env = GitEnvironment()
        self.test_dir = self.git_env.root_dir
    
    def tearDown(self):
        """Clean up the test environment."""
        # The GitEnvironment class will clean up the temporary directory
        pass
    
    def test_no_tag(self):
        """Test version extraction when no tag is present."""
        # Create files and commits
        self.git_env.create_file("README.md", "# Test Project")
        self.git_env.commit("Initial commit")
        
        # Create a CMake project with a default version
        cmake_project = CMakeProject(self.test_dir, self.gitversion_path)
        cmake_project.create_cmakelists({
            "DEFAULT_VERSION": "1.0.0"
        })
        
        # Configure the project and get version info
        version_info = cmake_project.configure()
        
        # Verify version information
        version = version_info.get("PROJECT_VERSION")
        self.assertTrue(version.startswith("1.0.0"), f"Version should start with 1.0.0, got {version}")
        self.assertEqual(version_info.get("MAJOR_MACRO"), "1")
        self.assertEqual(version_info.get("MINOR_MACRO"), "0")
        self.assertEqual(version_info.get("PATCH_MACRO"), "0")
    
    def test_no_tag_custom_default_version(self):
        """Test version extraction when no tag is present with a custom default version."""
        # Create files and commits
        self.git_env.create_file("README.md", "# Test Project")
        self.git_env.commit("Initial commit")
        
        # Create a CMake project with a custom default version
        cmake_project = CMakeProject(self.test_dir, self.gitversion_path)
        cmake_project.create_cmakelists({
            "DEFAULT_VERSION": "2.3.4"
        })
        
        # Configure the project and get version info
        version_info = cmake_project.configure()
        
        # Verify version information
        version = version_info.get("PROJECT_VERSION")
        self.assertTrue(version.startswith("2.3.4"), f"Version should start with 2.3.4, got {version}")
        self.assertEqual(version_info.get("MAJOR_MACRO"), "2")
        self.assertEqual(version_info.get("MINOR_MACRO"), "3")
        self.assertEqual(version_info.get("PATCH_MACRO"), "4")


if __name__ == "__main__":
    unittest.main() 
