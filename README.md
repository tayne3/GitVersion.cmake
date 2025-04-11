[English](README.md) | [中文](README_zh.md)

<p align="center">
  <img src="./docs/images/logo.svg" height="100" />
</p>
<p align="center" style="font-size: 24px; font-weight: bold; color: #797979;">GitVersion.cmake</p>

[![Ubuntu](https://github.com/tayne3/GitVersion.cmake/workflows/ubuntu/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Aubuntu)
[![Windows](https://github.com/tayne3/GitVersion.cmake/workflows/windows/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Awindows)
[![macOS](https://github.com/tayne3/GitVersion.cmake/workflows/macos/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Amacos)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![CMake](https://img.shields.io/badge/CMake-3.12%2B-brightgreen)
![GitHub Release](https://img.shields.io/github/v/release/tayne3/GitVersion.cmake?include_prereleases&label=release)

A lightweight CMake module that extracts version information from Git tags following the [Semantic Versioning 2.0.0](https://semver.org/) specification. This module provides a straightforward way to integrate Git-based versioning into your CMake build process.


## ✨ Features

- **Version Extraction** - Reliably extract version information from Git tags with SemVer 2.0.0 format support
- **Flexible Prefixes** - Support for customizable tag prefixes (default is "v" prefix, like "v1.0.0")
- **Fallback Mechanism** - Graceful handling when Git is unavailable with customizable default versions
- **Auto Reconfiguration** - CMake automatically reconfigures when Git HEAD changes
- **Cross-Platform** - Works reliably on Windows, macOS, and Linux

## 🎯 Use Cases

GitVersion.cmake is useful for:

- Automating version management in CMake projects
- Maintaining consistent version information across build artifacts
- Generating version-specific resource files and headers
- Integrating with package systems that require semantic versioning

## 🚀 Getting Started

### 📋 Requirements

- CMake 3.12+
- Git
- Git repository with at least one commit

### 📥 Installation

Add GitVersion.cmake to your project with a single command:

```bash
# Create cmake directory if it doesn't exist
mkdir -p cmake
# Download the latest version
curl -o cmake/GitVersion.cmake https://raw.githubusercontent.com/tayne3/GitVersion.cmake/master/GitVersion.cmake
```

### 📝 Basic Usage

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)
extract_version_from_git(VERSION PROJECT_VERSION PREFIX "v")
project(MyProject VERSION ${PROJECT_VERSION})
```

### 🔧 Using Custom Variables

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)

# Use only the parameters you need
extract_version_from_git(
  VERSION MY_VERSION
  MAJOR MY_VERSION_MAJOR
  PREFIX ""  # Use empty prefix for git tags like "1.0.0"
)

message(STATUS "Version: ${MY_VERSION}")
message(STATUS "Major version: ${MY_VERSION_MAJOR}")
```

### ⚙️ Advanced Options

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)

extract_version_from_git(
  VERSION PROJECT_VERSION               # Short version output like "1.2.3"
  FULL_VERSION PROJECT_FULL_VERSION     # Full version output like "1.2.3-dev.5+abc1234"
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
  DEFAULT_VERSION "1.0.0"               # Custom default version
  PREFIX "rel-"                         # Custom tag prefix (like rel-1.0.0)
  SOURCE_DIR "${CMAKE_SOURCE_DIR}/lib"  # Custom Git repository directory
  FAIL_ON_MISMATCH                      # Fail if versions don't match
)
```

### 📁 Header File Generation Example

version.h.in:
```c
#ifndef VERSION_H
#define VERSION_H

#define PROJECT_VERSION "@PROJECT_VERSION@"
#define PROJECT_FULL_VERSION "@PROJECT_FULL_VERSION@"
#define PROJECT_VERSION_MAJOR @PROJECT_VERSION_MAJOR@
#define PROJECT_VERSION_MINOR @PROJECT_VERSION_MINOR@
#define PROJECT_VERSION_PATCH @PROJECT_VERSION_PATCH@

#endif // VERSION_H
```

CMakeLists.txt:
```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)
extract_version_from_git(
  VERSION PROJECT_VERSION
  FULL_VERSION PROJECT_FULL_VERSION
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
)
project(MyProject VERSION ${PROJECT_VERSION})

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/include/version.h.in
  ${CMAKE_CURRENT_BINARY_DIR}/include/version.h
)

add_executable(my_app src/main.cpp)
target_include_directories(my_app PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/include)
```

## ⚙️ How It Works

GitVersion.cmake operates through a simple workflow:

1. Check if Git is available
2. If Git is available, run `git describe` to get tag information
3. Parse the output according to SemVer 2.0.0 format
4. Extract major, minor, and patch version components
5. Fall back to default version if Git is unavailable
6. Set up dependency on `.git/HEAD` for automatic reconfiguration

## 📝 Conventional Commits Integration

For optimal use with GitVersion.cmake, we recommend adopting [Conventional Commits](https://www.conventionalcommits.org/) for your commit messages. This structured commit format enhances your versioning workflow by:

- **Clear Version Bumping**: Commits with `fix:` prefix trigger patch versions, `feat:` trigger minor versions, and `BREAKING CHANGE:` trigger major versions
- **Automated Changelogs**: Generate comprehensive changelogs automatically based on structured commit messages
- **Better Collaboration**: Make your repository history more readable and organized for team members
- **CI/CD Integration**: Simplify automated release pipelines with predictable version increments

Example commit messages:
```
feat: add new authentication feature
fix: resolve memory leak in file processing
feat!: redesign API with breaking changes
docs: update README with Conventional Commits information
```

Using Conventional Commits alongside GitVersion.cmake creates a powerful, automated versioning system that follows semantic versioning principles consistently.

## 🏷️ Version Format

GitVersion.cmake produces the following types of version strings:

- **Exact Tag**: `1.2.3` (when HEAD is exactly at a tag)
- **Development Version**: `1.2.3-dev.5+abc1234` (5 commits after tag 1.2.3, at commit abc1234)
- **No Tag**: `0.0.0+abc1234` (only commit hash is available)

## 📋 Function Parameters

| Parameter | Type | Description | Required | Default |
|-----------|------|-------------|----------|---------|
| VERSION | Variable | Output variable for short version string (like v1.2.3) | No | - |
| FULL_VERSION | Variable | Output variable for full semantic version string (like 1.2.3-dev.5+abc1234) | No | - |
| MAJOR | Variable | Output variable for major version number | No | - |
| MINOR | Variable | Output variable for minor version number | No | - |
| PATCH | Variable | Output variable for patch version number | No | - |
| DEFAULT_VERSION | String | Default version used when Git is unavailable | No | "0.0.0" |
| PREFIX | String | Tag prefix (e.g., "v" for v1.0.0) | No | "v" |
| SOURCE_DIR | Path | Git repository directory | No | CMAKE_CURRENT_SOURCE_DIR |
| FAIL_ON_MISMATCH | Boolean | Fail if Git tag doesn't match default version | No | False |

**Note**:
- At least one output parameter (VERSION, FULL_VERSION, MAJOR, MINOR, or PATCH) must be specified.
- PREFIX now defaults to "v", which means the module will look for tags starting with "v" (like v1.2.3).

## 🔍 Troubleshooting

- **Git information not detected**: Make sure the repository has at least one commit and the `.git` directory is accessible.
- **Version not updating**: Check that the `.git/HEAD` file is accessible and that your build system reruns CMake.
- **Unexpected version format**: Ensure your tag format follows SemVer and use the `PREFIX` parameter if needed.

## ❓ FAQ

**Q: Can I use this without Git?**  
A: Yes, the module falls back to the specified DEFAULT_VERSION when Git is unavailable.

**Q: Does this work with CI/CD pipelines?**  
A: Yes, it works in most CI/CD environments that have Git installed.

**Q: Is there a performance impact?**  
A: The module only runs during CMake configuration, so it has minimal impact on build performance.

**Q: How does this work with Conventional Commits?**  
A: GitVersion.cmake extracts version information from Git tags, which can be created based on Conventional Commits. While it doesn't directly parse commit messages, it integrates perfectly with CI/CD systems that use Conventional Commits to create semantic version tags automatically.

**Q: Can I use this for non-SemVer versioning?**  
A: This module is specifically designed for SemVer 2.0.0 compatibility. Customization would be needed for other schemes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Please update tests as appropriate for any changes.
