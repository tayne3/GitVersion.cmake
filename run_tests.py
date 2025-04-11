#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test runner for GitVersion.cmake tests.

A streamlined wrapper around pytest that provides project-specific options.
With support for parallel test execution to improve performance.
"""

import sys
import os
import argparse
import subprocess
import importlib.util
import concurrent.futures
import tempfile
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

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

def discover_tests(markers: str = None) -> List[str]:
    """
    Discover test files based on markers or return all tests if no marker specified.
    
    Args:
        markers: Optional markers to filter tests
    
    Returns:
        List of test file paths
    """
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    if markers:
        cmd.append(f"-m {markers}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Parse the output to get the test file paths
        lines = result.stdout.strip().split('\n')
        test_files = []
        
        # Find test modules from the collected test list
        for line in lines:
            if "::" in line:
                module_path = line.split("::")[0]
                if module_path not in test_files:
                    test_files.append(module_path)
        
        return test_files
    except subprocess.CalledProcessError:
        print("Failed to discover tests. Make sure pytest is properly installed.")
        return []

def run_test_file(test_file: str, verbose: bool = False) -> Tuple[str, int, str, str]:
    """
    Run a single test file and return its results.
    
    Args:
        test_file: Path to the test file
        verbose: Whether to run with verbose output
    
    Returns:
        Tuple of (test_file, return_code, stdout, stderr)
    """
    cmd = [sys.executable, "-m", "pytest", test_file]
    if verbose:
        cmd.append("-v")
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    return (test_file, process.returncode, process.stdout, process.stderr)

def run_tests_in_parallel(test_files: List[str], workers: int, verbose: bool = False) -> Dict[str, Any]:
    """
    Run tests in parallel using a process pool.
    
    Args:
        test_files: List of test files to run
        workers: Number of worker processes
        verbose: Whether to run with verbose output
    
    Returns:
        Dictionary with test results
    """
    print(f"Running {len(test_files)} test files with {workers} workers...")
    
    results = {
        'passed': 0, 
        'failed': 0, 
        'total': len(test_files), 
        'failures': [],
        'successes': []
    }
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_file = {
            executor.submit(run_test_file, test_file, verbose): test_file 
            for test_file in test_files
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            test_file = future_to_file[future]
            try:
                file_path, return_code, stdout, stderr = future.result()
                # Always print at least a status message for each test
                if return_code == 0:
                    results['passed'] += 1
                    results['successes'].append({
                        'file': file_path,
                        'output': stdout
                    })
                    print(f"[PASS] {file_path} - PASSED")
                    # If verbose, also show the output for passed tests
                    if verbose and stdout.strip():
                        print("--- Test Output ---")
                        print(stdout)
                        print("-" * 40)
                else:
                    results['failed'] += 1
                    results['failures'].append({
                        'file': file_path,
                        'output': stdout,
                        'stderr': stderr
                    })
                    print(f"[FAIL] {file_path} - FAILED")
                    # Always show output for failed tests
                    print("--- Test Output ---")
                    print(stdout)
                    if stderr.strip():
                        print("--- Error Output ---")
                        print(stderr)
                    print("-" * 40)
            except Exception as e:
                results['failed'] += 1
                results['failures'].append({
                    'file': test_file,
                    'output': f"Error executing test: {str(e)}",
                    'stderr': f"Error executing test: {str(e)}"
                })
                print(f"[FAIL] {test_file} - ERROR: {str(e)}")
    
    return results

def display_results(results: Dict[str, Any], verbose: bool = False):
    """
    Display test execution results.
    
    Args:
        results: Dictionary with test results
        verbose: Whether to show detailed output for all tests
    """
    print("\n" + "="*80)
    print(f"Test Execution Summary:")
    print(f"  Total:  {results['total']}")
    print(f"  Passed: {results['passed']} [PASS]")
    print(f"  Failed: {results['failed']} [FAIL]")
    print("="*80)
    
    # In verbose mode, show details for both successes and failures
    if verbose:
        # First check if we have successes to show
        if results['passed'] > 0 and 'successes' in results:
            print("\nSuccessful Tests Summary:")
            for i, success in enumerate(results['successes'], 1):
                print(f"  [PASS] {i}. {success['file']}")
        
        # Then show details for failures
        if results['failed'] > 0:
            print("\nFailed Tests Details:")
            for i, failure in enumerate(results['failures'], 1):
                print(f"\n--- Failure {i}: {failure['file']} ---")
                print(failure['output'])
                if 'stderr' in failure and failure['stderr'].strip():
                    print("\nError Output:")
                    print(failure['stderr'])
                print("-"*80)

def main():
    """Run the GitVersion.cmake tests using pytest with parallel execution."""
    
    parser = argparse.ArgumentParser(description="Run GitVersion.cmake tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output")
    parser.add_argument("--markers", "-m", help="Only run tests with specific markers (e.g. 'basic')")
    parser.add_argument("--list-markers", action="store_true", help="List available project-specific markers")
    parser.add_argument("--check-deps", action="store_true", help="Check for required dependencies")
    parser.add_argument("--install-deps", action="store_true", help="Install development dependencies")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel mode")
    parser.add_argument("--workers", "-w", type=int, default=os.cpu_count(), 
                      help="Number of worker processes for parallel execution (default: number of CPU cores)")
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
        return 0
    
    # If parallel mode is enabled with internal implementation
    if args.parallel:
        # If specific tests are provided, use them
        if args.tests:
            test_files = args.tests
        else:
            # Otherwise discover tests based on markers
            test_files = discover_tests(args.markers)
        
        if not test_files:
            print("No tests found to run.")
            return 1
        
        # Run tests in parallel
        results = run_tests_in_parallel(test_files, args.workers, args.verbose)
        
        # Display results
        display_results(results, args.verbose)
        
        # Return non-zero exit code if any tests failed
        return 1 if results['failed'] > 0 else 0
    
    # Standard mode (non-parallel)
    else:
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
