# 🧪 GitVersion.cmake Testing Framework

This document provides a detailed overview of the testing framework architecture, execution methods, and best practices for the GitVersion.cmake project. The testing framework is designed to ensure the module works reliably across various environments and use cases.

## 🛠️ Testing Environment Setup

Before running tests, ensure your environment is properly configured and all dependencies are installed.

### 📦 Dependency Installation

You can easily install all necessary test dependencies with the following command:

```bash
python run_tests.py --check-deps --install-deps
```

The system will automatically check the dependency status and install missing packages. This command uses the `requirements-dev.txt` file in the project root directory for dependency management, ensuring consistency and reproducibility of the testing environment.

## 🏗️ Testing Architecture

Our testing framework employs a layered architecture, organizing test cases by functional complexity and usage scenarios to ensure comprehensive coverage of all features.

### 📁 Directory Structure

The testing framework is organized according to the following hierarchical structure:

- `tests/`: Entry directory for the test framework
  - `utils/`: Core testing tools and helper functions
  - `basic/`: Basic functionality test suite
  - `advanced/`: Advanced functionality test suite
  - `edge_cases/`: Edge cases and special scenario tests

## ▶️ Running Tests

GitVersion.cmake provides flexible and convenient test execution methods, adapting to different development and debugging needs.

### 🚀 Using the Test Runner

You can use the `run_tests.py` script in the project root directory to execute tests, which provides multiple options:

```bash
# Run all tests
python run_tests.py

# Run tests with detailed output (including test execution process and coverage information)
python run_tests.py --verbose

# Check if test environment dependencies are complete
python run_tests.py --check-deps

# Install all development and test dependencies
python run_tests.py --install-deps

# Run only tests with specific markers
python run_tests.py --markers basic

# View all available test markers and their descriptions
python run_tests.py --list-markers

# Run specific test files or test directories
python run_tests.py tests/basic/version_tag_test.py
```

### 🚄 Parallel Test Execution

To improve test execution performance, the testing framework supports parallel execution. You can use the following options:

```bash
# Run tests in parallel 
python run_tests.py --parallel

# Specify number of worker processes (default is number of CPU cores)
python run_tests.py --parallel --workers 4

# Combine with other options (e.g., markers and verbose)
python run_tests.py --parallel --markers basic --verbose
```

Our internal parallel implementation divides tests by file and runs each file in a separate process, then collects and aggregates results to provide a clear summary of test execution. This approach is ideal for our CMake testing needs, keeping the testing process simple yet efficient.

### 🏷️ Test Marking System

To facilitate organization and selective execution of tests, the GitVersion.cmake project defines the following test markers:

- `basic`: Core functionality tests, verifying basic version extraction and parsing functions
- `advanced`: Advanced functionality tests, covering complex scenarios and configuration options
- `edge_cases`: Edge case tests, ensuring system behavior meets expectations in special and exceptional situations

These markers are defined in the `pyproject.toml` file and implemented through pytest's marking system for test classification and filtering.

## ✏️ Adding New Tests

As project functionality expands, you may need to add new test cases. Please follow these steps:

1. Create a new test file in the appropriate test directory (filename should end with `_test.py` to indicate its test file identity)
2. Import necessary modules, utility classes, and testing framework components
3. Use appropriate pytest marker decorators (such as `@pytest.mark.basic`) to mark the test type
4. Implement test functions (recommended to use `test_` prefix naming for better discoverability)

### 📝 Test File Template

Here's an example structure of a typical test file:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for [Feature Name] in GitVersion.cmake.

This test module verifies [Specific Functionality] behavior under [Specific Scenario].
"""

import pytest
import os
from pathlib import Path

# Use pytest marker to mark test type
@pytest.mark.basic  # or advanced, edge_cases, etc.
def test_my_feature(git_env, cmake_project, gitversion_cmake_path):
    """
    Test whether [Feature] correctly [Expected Behavior] under [Conditions].
    
    Test steps:
    1. Set up test environment
    2. Perform test operations
    3. Verify results match expectations
    """
    # Set up test environment
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")  # Create version tag
    
    # Configure CMake project
    cmake_project.create_cmakelists({
        "DEFAULT_VERSION": "1.2.3"
    })
    
    # Perform test operations
    version_info = cmake_project.configure()
    
    # Verify test results
    assert version_info.get("PROJECT_VERSION") == "1.2.3", f"Version should be 1.2.3, actual: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Major version doesn't match"
    assert version_info.get("MINOR_MACRO") == "2", "Minor version doesn't match"
    assert version_info.get("PATCH_MACRO") == "3", "Patch version doesn't match"
```

## 💯 Testing Best Practices

Following these best practices can improve test quality and maintainability:

1. **Fixture Usage**: Fully utilize fixtures defined in `conftest.py` (`git_env`, `cmake_project`, etc.) to reduce redundant code and ensure testing environment consistency

2. **Classification and Marking**: Use appropriate pytest markers to categorize tests, making it easier to selectively run related test groups

3. **Test Isolation**: Ensure each test function is completely independent, not relying on the execution results or state of other tests

4. **Clear Assertion Messages**: Provide clear and detailed failure messages for each assertion, making the debugging process more efficient

5. **Parameterized Testing**: Use the `@pytest.mark.parametrize` decorator to test multiple input combinations, improving test coverage

6. **Detailed Documentation**: Write clear docstrings for each test function, explaining the test purpose, steps, and expected results

7. **Test Granularity**: Each test function should focus on verifying a specific functionality point, avoiding overly complex test logic

8. **Edge Cases**: Test not only normal paths but also consider exception handling, error handling, and boundary conditions
