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
            
        # Add source_dir if specified
        source_dir = ""
        if "SOURCE_DIR" in config:
            source_dir = f"SOURCE_DIR {config['SOURCE_DIR']}"
        
        # Add FAIL_ON_MISMATCH if specified
        fail_on_mismatch = ""
        if config.get("FAIL_ON_MISMATCH", False):
            fail_on_mismatch = "FAIL_ON_MISMATCH"
            
        # Add PREFIX if specified
        prefix = ""
        if "PREFIX" in config:
            prefix = f'PREFIX "{config["PREFIX"]}"'
            
        # Add DEFAULT_VERSION if specified
        default_version = ""
        if "DEFAULT_VERSION" in config:
            default_version = f'DEFAULT_VERSION {config["DEFAULT_VERSION"]}'
            
        # Create CMakeLists.txt content
        content = f"""
cmake_minimum_required(VERSION 3.12)

# Include GitVersion.cmake
include(${{CMAKE_CURRENT_SOURCE_DIR}}/cmake/GitVersion.cmake)

# Extract version from Git
extract_version_from_git(
  VERSION PROJECT_VERSION
  FULL_VERSION PROJECT_FULL_VERSION
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
  {default_version}
  {prefix}
  {source_dir}
  {fail_on_mismatch}
)

# Create a project with the extracted version (only using X.Y.Z part)
project(TestProject VERSION "${{PROJECT_VERSION}}")

# Output version information to a file
configure_file(
  "${{CMAKE_CURRENT_SOURCE_DIR}}/version.h.in"
  "${{CMAKE_CURRENT_BINARY_DIR}}/version.h"
)

# Create a simple executable
add_executable(test_app main.cpp)
"""
        
        # Create version.h.in template
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
        with open(self.root_dir / "CMakeLists.txt", "w") as f:
            f.write(content)
            
        with open(self.root_dir / "version.h.in", "w") as f:
            f.write(version_template)
            
        with open(self.root_dir / "main.cpp", "w") as f:
            f.write(main_cpp)
    
    def configure(self) -> Dict[str, str]:
        """Configure the CMake project.
        
        Returns:
            A dictionary with version information
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
            
            return version_info
        except subprocess.CalledProcessError as e:
            print(f"CMake Error Output:\n{e.stderr}")
            raise 
