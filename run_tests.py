#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test runner for GitVersion.cmake tests.

A streamlined wrapper around pytest that provides project-specific options.
"""

import sys
import argparse
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if the required dependencies are installed."""
    required_packages = ['pytest']
    return [pkg for pkg in required_packages if importlib.util.find_spec(pkg) is None]

def install_dependencies():
    """Install dependencies from requirements-dev.txt."""
    print("Installing development dependencies...")
    
    req_file = Path(__file__).parent / "requirements-dev.txt"
    if req_file.exists():
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
            print("Dependencies installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install them manually.")
            return False
    else:
        print("requirements-dev.txt not found. Please create this file or install dependencies manually.")
        return False

def list_project_markers():
    """List only the project-specific markers defined in pyproject.toml."""
    print("Available project-specific markers:")
    print("  @pytest.mark.basic: basic functionality tests")
    print("  @pytest.mark.advanced: advanced functionality tests")
    print("  @pytest.mark.edge_cases: edge case tests")
    return 0

def main():
    """Run the GitVersion.cmake tests using pytest."""
    
    parser = argparse.ArgumentParser(description="Run GitVersion.cmake tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output")
    parser.add_argument("--markers", "-m", help="Only run tests with specific markers (e.g. 'basic')")
    parser.add_argument("--list-markers", action="store_true", help="List available project-specific markers")
    parser.add_argument("--check-deps", action="store_true", help="Check for required dependencies")
    parser.add_argument("--install-deps", action="store_true", help="Install development dependencies")
    parser.add_argument("tests", nargs="*", help="Specific test files or directories to run")
    
    args = parser.parse_args()
    
    # List markers if requested
    if args.list_markers:
        return list_project_markers()
    
    # Check for dependencies if requested
    if args.check_deps or args.install_deps:
        missing_packages = check_dependencies()
        if missing_packages:
            print(f"Missing dependencies: {', '.join(missing_packages)}")
            
            if args.install_deps:
                if not install_dependencies():
                    return 1
            else:
                print("Run with --install-deps to install dependencies.")
                return 1
        else:
            print("All required dependencies are installed.")
            if args.check_deps and not args.install_deps:
                return 0
    
    # Build the pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add verbose flag if requested
    if args.verbose:
        cmd.append("-v")
    
    # Add marker if specified
    if args.markers:
        cmd.append(f"-m {args.markers}")
    
    # Add specific tests if provided
    if args.tests:
        cmd.extend(args.tests)
    
    # Print the command being run
    if args.verbose:
        print(f"Running: {' '.join(cmd)}")
    
    # Run the tests
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main()) 
