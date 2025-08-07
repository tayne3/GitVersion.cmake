# GitVersion.cmake Test Suite

Comprehensive test suite for GitVersion.cmake using pytest framework.

## 📋 Prerequisites

- Python 3.8+
- CMake 3.12+
- Git
- pytest

## 🚀 Quick Start

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v
```

## 🧪 Test Structure

```
tests/
├── basic/                  # Core functionality tests
│   ├── version_tag_test.py     # Tests for exact version tags
│   ├── development_version_test.py  # Tests for development versions
│   └── no_tag_test.py          # Tests for repositories without tags
├── advanced/               # Advanced feature tests
│   ├── dirty_state_test.py     # Dirty state detection tests
│   ├── multiple_tags_test.py   # Multiple tags handling
│   └── custom_source_dir_test.py  # Custom source directory tests
├── edge_cases/            # Edge cases and error handling
│   ├── branching_test.py       # Branch-specific scenarios
│   ├── fail_on_mismatch_test.py  # FAIL_ON_MISMATCH option tests
│   └── malformed_tags_test.py  # Invalid tag format handling
└── utils/                 # Test utilities
    ├── cmake_project.py        # CMake project helper
    └── git_environment.py      # Git repository helper
```

## 🎯 Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Category
```bash
# Basic tests only
pytest tests/basic/

# Advanced tests only
pytest tests/advanced/

# Edge cases only
pytest tests/edge_cases/
```

### Run Specific Test File
```bash
pytest tests/basic/version_tag_test.py
```

### Run Specific Test Function
```bash
pytest tests/basic/version_tag_test.py::test_exact_tag_version
```

### Run with Markers
```bash
# Run only basic tests
pytest tests/ -m basic

# Run only advanced tests
pytest tests/ -m advanced

# Run only edge case tests
pytest tests/ -m edge_cases
```

## 🔍 Test Options

### Verbose Output
```bash
pytest tests/ -v
```

### Show Test Output
```bash
pytest tests/ -s
```

### Stop on First Failure
```bash
pytest tests/ -x
```

### Run Failed Tests Only
```bash
# After a test run with failures
pytest tests/ --lf
```

### Parallel Execution
```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run tests in parallel with 4 workers
pytest tests/ -n 4
```

## 📊 Test Coverage

```bash
# Install coverage plugin
pip install pytest-cov

# Run with coverage report
pytest tests/ --cov=cmake --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=cmake --cov-report=html
# Open htmlcov/index.html in browser
```

## 🏷️ Test Markers

Tests are organized with markers for easy filtering:

- `@pytest.mark.basic` - Core functionality tests
- `@pytest.mark.advanced` - Advanced feature tests
- `@pytest.mark.edge_cases` - Edge case and error handling tests

## ✍️ Writing Tests

### Test File Naming
- Test files should be named `test_*.py` or `*_test.py`
- Place tests in appropriate category directory

### Test Function Naming
- Test functions must start with `test_`
- Use descriptive names that explain what is being tested

### Basic Test Example
```python
import pytest

@pytest.mark.basic
def test_exact_tag_version(git_env, cmake_project):
    """Test version extraction with an exact tag."""
    # Setup
    git_env.create_file("README.md", "# Test Project")
    git_env.commit("Initial commit")
    git_env.tag("1.2.3")
    
    # Execute
    cmake_project.create_cmakelists()
    version_info = cmake_project.configure()
    
    # Verify
    assert version_info.get("PROJECT_VERSION") == "1.2.3"
    assert version_info.get("MAJOR_MACRO") == "1"
    assert version_info.get("MINOR_MACRO") == "2"
    assert version_info.get("PATCH_MACRO") == "3"
```

### Using Fixtures

The test suite provides several fixtures:

- `git_env` - Creates a temporary Git repository
- `cmake_project` - Creates a CMake project with GitVersion.cmake
- `gitversion_cmake_path` - Path to the GitVersion.cmake file
- `project_root` - Path to the project root directory

## 🐛 Debugging Tests

### Run with Python Debugger
```bash
pytest tests/ --pdb
```

### Show Local Variables on Failure
```bash
pytest tests/ -l
```

### Detailed Traceback
```bash
pytest tests/ --tb=long
```

### Short Traceback
```bash
pytest tests/ --tb=short
```

## 🔧 Test Environment

Tests run in isolated temporary directories to ensure:
- No interference between tests
- No modification of the actual project
- Automatic cleanup after test completion

Each test creates its own:
- Temporary Git repository
- CMake project structure
- Build directory

## 📈 Test Statistics

Current test suite coverage:

| Category | Tests | Description |
|----------|-------|-------------|
| Basic | 6 | Core version extraction functionality |
| Advanced | 11 | Complex scenarios and features |
| Edge Cases | 18 | Error handling and special cases |
| **Total** | **35** | **Comprehensive test coverage** |

## 🔄 Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branch
- Release tags

Supported platforms:
- Ubuntu (latest)
- Windows (latest)
- macOS (latest)

## 🆘 Troubleshooting

### CMake Not Found
```bash
# Ensure CMake is installed and in PATH
cmake --version
```

### Git Not Found
```bash
# Ensure Git is installed and in PATH
git --version
```

### Permission Errors
- Tests create temporary files and directories
- Ensure write permissions in system temp directory

### Test Failures on Windows
- Line ending differences may cause issues
- Tests handle both LF and CRLF appropriately

## 📝 Contributing

When adding new tests:

1. Choose the appropriate category (basic/advanced/edge_cases)
2. Follow existing naming conventions
3. Add docstrings to test functions
4. Use descriptive assertion messages
5. Ensure tests are independent and isolated
6. Clean up resources using fixtures

Example PR checklist:
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Test docstrings are clear
- [ ] No hardcoded paths
- [ ] Works on all platforms

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [CMake testing guide](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [Git documentation](https://git-scm.com/doc)

## 📄 License

Tests are part of the GitVersion.cmake project and follow the same MIT license.
