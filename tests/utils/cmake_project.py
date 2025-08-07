#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CMake project utilities for testing GitVersion.cmake.
"""

import os
import shutil
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional


class CMakeProject:
    """Class to manage a CMake project for testing."""
    
    def __init__(self, root_dir: Path, gitversion_path: Path):
        """Initialize a CMake project.
        
        Args:
            root_dir: The project root directory
            gitversion_path: Path to GitVersion.cmake
        """
        self.root_dir = root_dir
        
        # Copy GitVersion.cmake to the project
        cmake_dir = root_dir / "cmake"
        os.makedirs(cmake_dir, exist_ok=True)
        shutil.copy(gitversion_path, cmake_dir / "GitVersion.cmake")
    
    def create_cmakelists(self, config: Optional[Dict[str, str]] = None) -> None:
        """Create a CMakeLists.txt file.
        
        Args:
            config: Configuration parameters for GitVersion.cmake
        """
        if config is None:
            config = {}
            
        # Build parameter list for git_version_info
        params = []
        
        # Always include basic version parameters
        params.extend([
            "VERSION PROJECT_VERSION",
            "FULL_VERSION PROJECT_FULL_VERSION",
            "MAJOR PROJECT_VERSION_MAJOR",
            "MINOR PROJECT_VERSION_MINOR",
            "PATCH PROJECT_VERSION_PATCH"
        ])
        
        # Add optional extended parameters
        if config.get("INCLUDE_EXTENDED", False):
            params.extend([
                "COMMIT_HASH PROJECT_COMMIT_HASH",
                "COMMIT_COUNT PROJECT_COMMIT_COUNT",
                "IS_DIRTY PROJECT_IS_DIRTY",
                "IS_TAGGED PROJECT_IS_TAGGED",
                "IS_DEVELOPMENT PROJECT_IS_DEVELOPMENT",
                "TAG_NAME PROJECT_TAG_NAME",
                "BRANCH_NAME PROJECT_BRANCH_NAME"
            ])
        
        # Add source_dir if specified
        if "SOURCE_DIR" in config:
            params.append(f"SOURCE_DIR {config['SOURCE_DIR']}")
        
        # Add FAIL_ON_MISMATCH if specified
        if config.get("FAIL_ON_MISMATCH", False):
            params.append("FAIL_ON_MISMATCH")
            
        # Add DEFAULT_VERSION if specified
        if "DEFAULT_VERSION" in config:
            params.append(f'DEFAULT_VERSION {config["DEFAULT_VERSION"]}')
        
        # Add HASH_LENGTH if specified
        if "HASH_LENGTH" in config:
            params.append(f'HASH_LENGTH {config["HASH_LENGTH"]}')
        
        # Create parameter string
        params_str = '\n  '.join(params)
        
        # Create CMakeLists.txt content
        content = f"""
cmake_minimum_required(VERSION 3.12)

# Include GitVersion.cmake
include(${{CMAKE_CURRENT_SOURCE_DIR}}/cmake/GitVersion.cmake)

# Extract version information
git_version_info(
  {params_str}
)

# Create a project with the version (VERSION is always clean semantic version)
project(TestProject VERSION "${{PROJECT_VERSION}}")

# Output version information to a file
configure_file(
  "${{CMAKE_CURRENT_SOURCE_DIR}}/version.h.in"
  "${{CMAKE_CURRENT_BINARY_DIR}}/version.h"
)

# Create a simple executable
add_executable(test_app main.cpp)
"""
        
        # Create version.h.in template (extended if requested)
        if config.get("INCLUDE_EXTENDED", False):
            version_template = """
#pragma once

#define PROJECT_VERSION "${PROJECT_VERSION}"
#define PROJECT_FULL_VERSION "${PROJECT_FULL_VERSION}"
#define PROJECT_VERSION_MAJOR ${PROJECT_VERSION_MAJOR}
#define PROJECT_VERSION_MINOR ${PROJECT_VERSION_MINOR}
#define PROJECT_VERSION_PATCH ${PROJECT_VERSION_PATCH}
#define PROJECT_COMMIT_HASH "${PROJECT_COMMIT_HASH}"
#define PROJECT_COMMIT_COUNT ${PROJECT_COMMIT_COUNT}
#cmakedefine01 PROJECT_IS_DIRTY
#cmakedefine01 PROJECT_IS_TAGGED
#cmakedefine01 PROJECT_IS_DEVELOPMENT
#define PROJECT_TAG_NAME "${PROJECT_TAG_NAME}"
#define PROJECT_BRANCH_NAME "${PROJECT_BRANCH_NAME}"
"""
        else:
            version_template = """
#pragma once

#define PROJECT_VERSION "${PROJECT_VERSION}"
#define PROJECT_FULL_VERSION "${PROJECT_FULL_VERSION}"
#define PROJECT_VERSION_MAJOR ${PROJECT_VERSION_MAJOR}
#define PROJECT_VERSION_MINOR ${PROJECT_VERSION_MINOR}
#define PROJECT_VERSION_PATCH ${PROJECT_VERSION_PATCH}
"""
        
        # Create main.cpp
        main_cpp = """
#include <iostream>
#include "version.h"

int main() {
    std::cout << "Version: " << PROJECT_VERSION << std::endl;
    return 0;
}
"""
        
        # Write files
        with open(self.root_dir / "CMakeLists.txt", "w", newline='\n') as f:
            f.write(content)
            
        with open(self.root_dir / "version.h.in", "w", newline='\n') as f:
            f.write(version_template)
            
        with open(self.root_dir / "main.cpp", "w", newline='\n') as f:
            f.write(main_cpp)
    
    def commit_project_files(self, git_env) -> None:
        """Commit the project files to Git to avoid dirty state.
        
        Args:
            git_env: The GitEnvironment instance to use for committing
        """
        # Add and commit the project files to avoid dirty state
        import subprocess
        subprocess.run(["git", "add", "CMakeLists.txt", "version.h.in", "main.cpp", "cmake/"], 
                      cwd=self.root_dir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Add CMake project files"], 
                      cwd=self.root_dir, check=True, capture_output=True)
    
    def configure(self) -> Dict[str, str]:
        """Configure the CMake project.
        
        Returns:
            A dictionary with version information
            
        Raises:
            subprocess.CalledProcessError: If CMake configuration fails
        """
        # Create a build directory
        build_dir = self.root_dir / "build"
        os.makedirs(build_dir, exist_ok=True)
        
        # Run CMake
        try:
            result = subprocess.run(
                ["cmake", ".."],
                cwd=build_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Extract version information from the output file
            version_file = build_dir / "version.h"
            with open(version_file, "r") as f:
                version_h = f.read()
            
            # Extract version strings using regex
            version_match = re.search(r'#define PROJECT_VERSION "([^"]+)"', version_h)
            full_version_match = re.search(r'#define PROJECT_FULL_VERSION "([^"]+)"', version_h)
            major_match = re.search(r'#define PROJECT_VERSION_MAJOR (\d+)', version_h)
            minor_match = re.search(r'#define PROJECT_VERSION_MINOR (\d+)', version_h)
            patch_match = re.search(r'#define PROJECT_VERSION_PATCH (\d+)', version_h)
            
            # Extract extended parameters if present
            commit_hash_match = re.search(r'#define PROJECT_COMMIT_HASH "([^"]+)"', version_h)
            commit_count_match = re.search(r'#define PROJECT_COMMIT_COUNT (\d+)', version_h)
            is_dirty_match = re.search(r'#define PROJECT_IS_DIRTY ([01])', version_h)
            is_tagged_match = re.search(r'#define PROJECT_IS_TAGGED ([01])', version_h)
            is_development_match = re.search(r'#define PROJECT_IS_DEVELOPMENT ([01])', version_h)
            tag_name_match = re.search(r'#define PROJECT_TAG_NAME "([^"]+)"', version_h)
            branch_name_match = re.search(r'#define PROJECT_BRANCH_NAME "([^"]+)"', version_h)
            
            # Return the extracted values
            version_info = {}
            
            if version_match:
                version_info["PROJECT_VERSION"] = version_match.group(1)
            if full_version_match:
                version_info["PROJECT_FULL_VERSION"] = full_version_match.group(1)
            if major_match:
                version_info["MAJOR_MACRO"] = major_match.group(1)
            if minor_match:
                version_info["MINOR_MACRO"] = minor_match.group(1)
            if patch_match:
                version_info["PATCH_MACRO"] = patch_match.group(1)
            
            # Add extended information if available
            if commit_hash_match:
                version_info["PROJECT_COMMIT_HASH"] = commit_hash_match.group(1)
            if commit_count_match:
                version_info["PROJECT_COMMIT_COUNT"] = commit_count_match.group(1)
            if is_dirty_match:
                version_info["PROJECT_IS_DIRTY"] = is_dirty_match.group(1) == "1"
            if is_tagged_match:
                version_info["PROJECT_IS_TAGGED"] = is_tagged_match.group(1) == "1"
            if is_development_match:
                version_info["PROJECT_IS_DEVELOPMENT"] = is_development_match.group(1) == "1"
            if tag_name_match:
                version_info["PROJECT_TAG_NAME"] = tag_name_match.group(1)
            if branch_name_match:
                version_info["PROJECT_BRANCH_NAME"] = branch_name_match.group(1)
            
            return version_info
        except subprocess.CalledProcessError as e:
            # Enhance exception with details from stderr and stdout
            print(f"CMake Error Output:\n{e.stderr}")
            
            # Make sure the exception contains the error information for the test to access
            # This modifies the exception object to ensure stderr information is preserved
            e.stderr = e.stderr if e.stderr else "No error output"
            e.stdout = e.stdout if e.stdout else "No standard output"
            
            # Raise the exception for the test to catch
            raise 
