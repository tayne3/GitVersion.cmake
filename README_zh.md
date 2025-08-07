[English](README.md) | 中文

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

一个轻量级的 CMake 模块，用于从遵循[语义化版本 2.0.0 规范](https://semver.org/)的 Git 标签中提取版本信息。该模块提供了一种简单直接的方法，将基于 Git 的版本控制集成到 CMake 构建过程中。

---

## ✨ 功能特点

- **版本提取** - 可靠地从 Git 标签中提取符合 SemVer 2.0.0 格式的版本信息
- **脏状态检测** - 自动检测未提交的更改并在版本字符串中包含 `-dirty` 后缀
- **综合信息** - 获取提交哈希、分支名称、标签信息和仓库状态
- **回退机制** - 当 Git 不可用时优雅回退，支持自定义默认版本
- **自动重配置** - 当 Git HEAD 变更时 CMake 自动重新配置
- **跨平台兼容** - 在 Windows、macOS 和 Linux 上可靠运行

## 🎯 使用场景

GitVersion.cmake 适用于：

- 在 CMake 项目中自动化版本管理
- 在构建产物中维护一致的版本信息
- 生成与版本相关的资源文件和头文件
- 与需要语义化版本的包管理系统集成

## 🚀 快速入门

### 📋 系统要求

- CMake 3.12+
- Git

### 📥 安装方法

只需一行命令即可将 GitVersion.cmake 添加到您的项目中：

```bash
# 如果目录不存在，创建 cmake 目录
mkdir -p cmake
# 下载最新版本
curl -o cmake/GitVersion.cmake https://github.com/tayne3/GitVersion.cmake/releases/latest/download/GitVersion.cmake
```

### 📝 基本用法

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)
git_version_info(VERSION PROJECT_VERSION)
project(MyProject VERSION ${PROJECT_VERSION})
```

### 🔧 使用多个变量

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
message(STATUS "版本: ${PROJECT_VERSION}")
message(STATUS "完整版本: ${PROJECT_FULL_VERSION}")
```

### ⚙️ 高级选项

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

查看[函数参数](#-函数参数)了解所有可用选项。

### 📁 头文件生成示例

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

## ⚙️ 工作原理

GitVersion.cmake 使用 `git describe` 从 Git 标签中提取版本信息，按照 SemVer 2.0.0 规范进行解析，在 Git 不可用时回退到默认版本。当 Git HEAD 变更时模块会自动重新配置

## 📝 约定式提交集成

GitVersion.cmake 与[约定式提交](https://www.conventionalcommits.org/)完美配合，实现自动化版本管理。使用 `fix:` 触发补丁版本，`feat:` 触发次版本，`BREAKING CHANGE:` 触发主版本，保持语义化版本的一致性。

## 🏷️ 版本格式

GitVersion.cmake 生成以下几种类型的版本字符串 (FULL_VERSION)：

- **标签发布版 (clean)**：`1.2.3`（当 HEAD 正好位于标签且无更改）
- **标签发布版 (dirty)**：`1.2.3-dirty`（当 HEAD 位于标签但有未提交更改）
- **开发版 (clean)**：`1.2.3-dev.5+abc1234`（标签 1.2.3 后的 5 个提交，位于提交 abc1234）
- **开发版 (dirty)**：`1.2.3-dev.5+abc1234.dirty`（有未提交更改的开发版本）
- **无标签 (clean)**：`0.0.0+abc1234`（仅有提交哈希可用）
- **无标签 (dirty)**：`0.0.0+abc1234.dirty`（无标签且有未提交更改）

## 📋 函数参数

| 参数 | 类型 | 描述 | 必需 | 默认值 |
|-----------|------|-------------|----------|---------|
| VERSION | 变量 | 清洁版本字符串输出变量（如 1.2.3） | 否 | - |
| FULL_VERSION | 变量 | 带元数据的完整版本输出变量（如 1.2.3-dev.5+abc1234.dirty） | 否 | - |
| MAJOR | 变量 | 主版本号输出变量 | 否 | - |
| MINOR | 变量 | 次版本号输出变量 | 否 | - |
| PATCH | 变量 | 补丁版本号输出变量 | 否 | - |
| COMMIT_HASH | 变量 | 当前提交哈希输出变量 | 否 | - |
| COMMIT_COUNT | 变量 | 自上次标签以来提交数输出变量 | 否 | - |
| IS_DIRTY | 变量 | 脏状态输出变量（布尔值） | 否 | - |
| IS_TAGGED | 变量 | 指示 HEAD 是否位于标签提交的输出变量 | 否 | - |
| IS_DEVELOPMENT | 变量 | 指示开发版本的输出变量 | 否 | - |
| TAG_NAME | 变量 | 当前/最近标签名输出变量 | 否 | - |
| BRANCH_NAME | 变量 | 当前分支名输出变量 | 否 | - |
| DEFAULT_VERSION | 字符串 | Git 不可用时使用的默认版本 | 否 | "0.0.0" |
| SOURCE_DIR | 路径 | Git 仓库目录 | 否 | CMAKE_CURRENT_SOURCE_DIR |
| HASH_LENGTH | 整数 | Git 提交哈希长度（有效范围：1-40） | 否 | 7 |
| FAIL_ON_MISMATCH | 布尔值 | 如果 Git 标签与默认版本不匹配则失败 | 否 | False |

**注意**：

- 至少需要指定一个输出参数（VERSION、FULL_VERSION、MAJOR、MINOR 或 PATCH）。
- 如果 HASH_LENGTH 小于 0 或大于 40，将被限制为 40 个字符。

## 🔍 故障排除

- **未检测到 Git 信息**：确保仓库至少有一个提交，并且 `.git` 目录可访问。
- **版本未更新**：检查 `.git/HEAD` 文件是否可访问，以及构建系统是否重新运行 CMake。
- **版本格式异常**：确保标签格式遵循 SemVer。

## ❓ 常见问题

**问：我可以在没有 Git 的情况下使用吗？**  
答：可以，当 Git 不可用时，模块会回退到指定的 DEFAULT_VERSION。

**问：这可以在 CI/CD 管道中工作吗？**  
答：是的，它可以在大多数安装了 Git 的 CI/CD 环境中工作。

**问：对性能有影响吗？**  
答：该模块仅在 CMake 配置阶段运行，对构建性能影响很小。

**问：这如何与约定式提交协同工作？**  
答：GitVersion.cmake 从 Git 标签中提取版本信息，这些标签可以基于约定式提交创建。虽然它不直接解析提交信息，但它与使用约定式提交自动创建语义化版本标签的 CI/CD 系统完美集成。

**问：可以用于非 SemVer 版本控制吗？**  
答：此模块专为 SemVer 2.0.0 兼容性设计。其他方案需要定制。

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 👥 贡献

欢迎贡献！请随时提交拉取请求。

1. Fork 仓库
2. 创建功能分支
3. 提交拉取请求

请为任何更改适当地更新测试。
