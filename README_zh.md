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
- **回退机制** - 当 Git 不可用时，优雅地回退到自定义默认版本
- **自动重配置** - 当 Git HEAD 变更时，CMake 自动重新配置
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

只需一步即可将 GitVersion.cmake 添加到您的项目中：

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
gitversion_extract(VERSION PROJECT_VERSION)
project(MyProject VERSION ${PROJECT_VERSION})
```

### 🔧 使用自定义变量

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)

# 只使用需要的输出参数
gitversion_extract(
  VERSION MY_VERSION
  MAJOR MY_VERSION_MAJOR
)

message(STATUS "版本号: ${MY_VERSION}")
message(STATUS "主版本号: ${MY_VERSION_MAJOR}")
```

### ⚙️ 高级选项

```cmake
cmake_minimum_required(VERSION 3.12)

include(cmake/GitVersion.cmake)

gitversion_extract(
  VERSION PROJECT_VERSION               # 输出简短版本，如 "1.2.3"
  FULL_VERSION PROJECT_FULL_VERSION     # 输出完整版本如 "1.2.3-dev.5+abc1234"
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
  DEFAULT_VERSION "1.0.0"               # 自定义默认版本
  SOURCE_DIR "${CMAKE_SOURCE_DIR}/lib"  # 自定义 Git 仓库目录
  HASH_LENGTH 7                         # 将提交哈希截断为 7 个字符
  FAIL_ON_MISMATCH                      # 如果版本不匹配则失败
)
```

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
gitversion_extract(
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

GitVersion.cmake 通过以下简单流程运行：

1. 检查 Git 是否可用
2. 如果 Git 可用，运行 `git describe` 获取标签信息
3. 根据 SemVer 2.0.0 格式解析输出
4. 提取主版本号、次版本号和补丁版本号
5. 如果 Git 不可用，回退到默认版本
6. 设置对 `.git/HEAD` 的依赖，以便自动重新配置

## 📝 约定式提交集成

为了与 GitVersion.cmake 配合使用，我们推荐采用[约定式提交](https://www.conventionalcommits.org/)规范来编写提交信息。这种结构化的提交格式通过以下方式增强您的版本控制工作流：

- **清晰的版本递增**：带有 `fix:` 前缀的提交触发补丁版本更新，`feat:` 触发次版本更新，而 `BREAKING CHANGE:` 触发主版本更新
- **自动化更新日志**：基于结构化提交信息自动生成全面的更新日志
- **更好的协作**：使您的代码库历史对团队成员更具可读性和条理性
- **CI/CD 集成**：通过可预测的版本增量简化自动化发布流程

提交信息示例：
```
feat: 添加新的身份验证功能
fix: 解决文件处理中的内存泄漏
feat!: 重新设计 API，包含破坏性变更
docs: 更新 README，添加约定式提交信息
```

将约定式提交与 GitVersion.cmake 结合使用，可以创建一个强大的、自动化的版本控制系统，该系统始终遵循语义化版本原则。

## 🏷️ 版本格式

GitVersion.cmake 生成以下几种类型的版本字符串 (FULL_VERSION)：

- **精确标签**：`1.2.3`（当 HEAD 正好位于标签处）
- **开发版本**：`1.2.3-dev.5+abc1234`（标签 1.2.3 之后的 5 个提交，位于提交 abc1234）
- **无标签**：`0.0.0+abc1234`（仅有提交哈希可用）

## 📋 函数参数

| 参数 | 类型 | 描述 | 必需 | 默认值 |
|-----------|------|-------------|----------|---------|
| VERSION | 变量 | 普通的版本字符串输出变量（如 1.2.3） | 否 | - |
| FULL_VERSION | 变量 | 符合语义化版本的完整版本字符串（如 1.2.3-dev.5+abc1234）输出变量 | 否 | - |
| MAJOR | 变量 | 主版本号的输出变量 | 否 | - |
| MINOR | 变量 | 次版本号的输出变量 | 否 | - |
| PATCH | 变量 | 补丁版本号的输出变量 | 否 | - |
| DEFAULT_VERSION | 字符串 | Git 不可用时使用的默认版本 | 否 | "0.0.0" |
| SOURCE_DIR | 路径 | Git 仓库目录 | 否 | CMAKE_CURRENT_SOURCE_DIR |
| HASH_LENGTH | 整数 | 在完整版本中包含的 Git 提交哈希的长度（有效范围：1-40） | 否 | 7 |
| FAIL_ON_MISMATCH | 布尔值 | 如果 Git 标签与默认版本不匹配则失败 | 否 | False |

**注意**：
- 至少需要指定其中一个输出参数（VERSION、FULL_VERSION、MAJOR、MINOR 或 PATCH）。
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
