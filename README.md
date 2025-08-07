English | [中文](README_zh.md)

<p align="center">
  <img src="./docs/images/logo.svg" height="100" />
</p>
<p align="center" style="font-size: 24px; font-weight: bold; color: #797979;">GitVersion.cmake</p>

![CMake](https://img.shields.io/badge/CMake-3.12%2B-brightgreen?logo=cmake&logoColor=white)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/tayne3/GitVersion.cmake)
[![Release](https://img.shields.io/github/v/release/tayne3/GitVersion.cmake?include_prereleases&label=release&logo=github&logoColor=white)](https://github.com/tayne3/GitVersion.cmake/releases)
[![Tag](https://img.shields.io/github/v/tag/tayne3/GitVersion.cmake?color=%23ff8936&style=flat-square&logo=git&logoColor=white)](https://github.com/tayne3/GitVersion.cmake/tags)
[![Ubuntu](https://github.com/tayne3/GitVersion.cmake/workflows/ubuntu/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Aubuntu)
[![Windows](https://github.com/tayne3/GitVersion.cmake/workflows/windows/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Awindows)
[![macOS](https://github.com/tayne3/GitVersion.cmake/workflows/macos/badge.svg)](https://github.com/tayne3/GitVersion.cmake/actions?query=workflow%3Amacos)

A lightweight CMake module that extracts version information from Git tags following the [Semantic Versioning 2.0.0](https://semver.org/) specification. This module provides a straightforward way to integrate Git-based versioning into your CMake build process.

---

## ✨ Features

- **Version Extraction** - Reliably extract version information from Git tags with SemVer 2.0.0 format support
- **Dirty State Detection** - Automatically detect uncommitted changes and include `-dirty` suffix in version strings
- **Comprehensive Information** - Get commit hash, branch name, tag information, and repository state
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

### 📥 Installation

Add GitVersion.cmake to your project with a single command:

```bash
# Create cmake directory if it doesn't exist
mkdir -p cmake
# Download the latest version
curl -o cmake/GitVersion.cmake https://github.com/tayne3/GitVersion.cmake/releases/latest/download/GitVersion.cmake
```

### 📝 Basic Usage

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)
git_version_info(VERSION PROJECT_VERSION)
project(MyProject VERSION ${PROJECT_VERSION})
```

### 🔧 Using Multiple Variables

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)

# Extract comprehensive version information
git_version_info(
  VERSION PROJECT_VERSION
  FULL_VERSION PROJECT_FULL_VERSION
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
)

project(MyProject VERSION ${PROJECT_VERSION})
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "Full version: ${PROJECT_FULL_VERSION}")
```

### ⚙️ Advanced Options

```cmake
git_version_info(
  VERSION PROJECT_VERSION
  FULL_VERSION PROJECT_FULL_VERSION  
  IS_DIRTY PROJECT_IS_DIRTY
  COMMIT_HASH PROJECT_COMMIT_HASH
  DEFAULT_VERSION "1.0.0"
  FAIL_ON_MISMATCH
)

project(MyProject VERSION ${PROJECT_VERSION})

if(PROJECT_IS_DIRTY)
  message(WARNING "Working directory has uncommitted changes")
endif()
```

See [Function Parameters](#-function-parameters) for all available options.

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
git_version_info(
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

GitVersion.cmake extracts version information from Git tags using `git describe`, parses them according to SemVer 2.0.0, and falls back to a default version when Git is unavailable. The module automatically reconfigures when Git HEAD changes

## 📝 Conventional Commits Integration

GitVersion.cmake works seamlessly with [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning. Use `fix:` for patches, `feat:` for minor versions, and `BREAKING CHANGE:` for major versions to maintain consistent semantic versioning.

## 🏷️ Version Format

GitVersion.cmake produces the following types of version strings (FULL_VERSION):

- **Tagged Release (clean)**: `1.2.3` (when HEAD is exactly at a tag with no changes)
- **Tagged Release (dirty)**: `1.2.3-dirty` (when HEAD is at a tag but has uncommitted changes)
- **Development (clean)**: `1.2.3-dev.5+abc1234` (5 commits after tag 1.2.3, at commit abc1234)
- **Development (dirty)**: `1.2.3-dev.5+abc1234.dirty` (development version with uncommitted changes)
- **No Tags (clean)**: `0.0.0+abc1234` (only commit hash available)
- **No Tags (dirty)**: `0.0.0+abc1234.dirty` (no tags with uncommitted changes)

## 📋 Function Parameters

| Parameter | Type | Description | Required | Default |
|-----------|------|-------------|----------|---------|
| VERSION | Variable | Output variable for clean version string (like 1.2.3) | No | - |
| FULL_VERSION | Variable | Output variable for full version with metadata (like 1.2.3-dev.5+abc1234.dirty) | No | - |
| MAJOR | Variable | Output variable for major version number | No | - |
| MINOR | Variable | Output variable for minor version number | No | - |
| PATCH | Variable | Output variable for patch version number | No | - |
| COMMIT_HASH | Variable | Output variable for current commit hash | No | - |
| COMMIT_COUNT | Variable | Output variable for commits since last tag | No | - |
| IS_DIRTY | Variable | Output variable for dirty state (boolean) | No | - |
| IS_TAGGED | Variable | Output variable indicating if HEAD is at a tagged commit | No | - |
| IS_DEVELOPMENT | Variable | Output variable indicating development version | No | - |
| TAG_NAME | Variable | Output variable for current/nearest tag name | No | - |
| BRANCH_NAME | Variable | Output variable for current branch name | No | - |
| DEFAULT_VERSION | String | Default version used when Git is unavailable | No | "0.0.0" |
| SOURCE_DIR | Path | Git repository directory | No | CMAKE_CURRENT_SOURCE_DIR |
| HASH_LENGTH | Integer | Git commit hash length (valid range: 1-40) | No | 7 |
| FAIL_ON_MISMATCH | Boolean | Fail if Git tag doesn't match default version | No | False |

**Note**:

- At least one output parameter (VERSION, FULL_VERSION, MAJOR, MINOR, or PATCH) must be specified.
- If HASH_LENGTH is less than 0 or greater than 40, it will be capped at 40 characters.

## 🔍 Troubleshooting

- **Git information not detected**: Make sure the repository has at least one commit and the `.git` directory is accessible.
- **Version not updating**: Check that the `.git/HEAD` file is accessible and that your build system reruns CMake.
- **Unexpected version format**: Ensure your tag format follows SemVer.

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
