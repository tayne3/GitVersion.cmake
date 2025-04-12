# 🧪 GitVersion.cmake 测试框架

本文档详细介绍了 GitVersion.cmake 项目的测试框架架构、执行方法和最佳实践。该测试框架旨在确保模块在各种环境和用例下都能可靠运行。

## 🛠️ 测试环境设置

在开始运行测试之前，需要确保您的环境配置正确并已安装所有依赖项。

### 📦 依赖安装

您可以通过以下命令轻松安装所有必要的测试依赖：

```bash
python run_tests.py --check-deps --install-deps
```

系统将自动检查依赖项状态并安装缺失的包。该命令使用项目根目录下的 `requirements-dev.txt` 文件进行依赖管理，确保测试环境的一致性和可重现性。

## 🏗️ 测试架构

我们的测试框架采用分层架构，按功能复杂度和使用场景组织测试用例，确保全面覆盖所有功能点。

### 📁 目录结构

测试框架按以下层次结构组织：

- `tests/`: 测试框架的入口目录
  - `utils/`: 核心测试工具和辅助函数
  - `basic/`: 基础功能测试集
  - `advanced/`: 高级功能测试集
  - `edge_cases/`: 边缘情况和特殊场景测试

## ▶️ 运行测试

GitVersion.cmake 提供了灵活便捷的测试执行方式，适应不同的开发和调试需求。

### 🚀 使用测试运行器

您可以使用项目根目录的 `run_tests.py` 脚本执行测试，该脚本提供多种选项：

```bash
# 运行所有测试
python run_tests.py

# 运行测试并显示详细输出（包括测试执行过程和覆盖率信息）
python run_tests.py --verbose

# 检查测试环境依赖是否完整
python run_tests.py --check-deps

# 安装所有开发和测试依赖项
python run_tests.py --install-deps

# 仅运行特定标记的测试组
python run_tests.py --markers basic

# 查看所有可用的测试标记及其描述
python run_tests.py --list-markers

# 运行特定的测试文件或测试目录
python run_tests.py tests/basic/version_tag_test.py
```

### 🚄 并行测试执行

为提高测试执行性能，测试框架支持并行执行模式。您可以使用以下选项：

```bash
# 使用并行模式执行测试
python run_tests.py --parallel

# 指定工作进程数量（默认为 CPU 核心数）
python run_tests.py --parallel --workers 4

# 与其他选项组合使用（例如标记和详细输出）
python run_tests.py --parallel --markers basic --verbose
```

我们的内部并行实现按文件划分测试，在单独的进程中运行每个文件，然后收集并汇总结果，提供清晰的测试执行摘要。这种方法最适合我们的 CMake 测试需求，使测试过程简单而高效。

### 🏷️ 测试标记系统

为便于组织和选择性执行测试，GitVersion.cmake 项目定义了以下测试标记：

- `basic`: 核心功能测试，验证基本版本提取和解析功能
- `advanced`: 高级功能测试，覆盖复杂场景和配置选项
- `edge_cases`: 边缘情况测试，确保在特殊和异常情况下系统行为符合预期

这些标记在 `pyproject.toml` 文件中定义，并通过 pytest 的标记系统实现测试分类与筛选。

## ✏️ 添加新测试

随着项目功能的扩展，您可能需要添加新的测试用例。请按照以下步骤操作：

1. 在适当的测试目录下创建新的测试文件（文件名应以 `_test.py` 结尾，表示其测试文件身份）
2. 导入必要的模块、工具类和测试框架组件
3. 使用适当的 pytest marker 装饰器（如 `@pytest.mark.basic`）标记测试类型
4. 实现测试函数（建议使用 `test_` 前缀命名，提高可发现性）

### 📝 测试文件模板

以下是一个典型测试文件的结构示例：

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
        "DEFAULT_VERSION": "1.2.3",
        "PREFIX": "v"
    })
    
    # Perform test operations
    version_info = cmake_project.configure()
    
    # Verify test results
    assert version_info.get("PROJECT_VERSION") == "1.2.3", f"Version should be 1.2.3, actual: {version_info.get('PROJECT_VERSION')}"
    assert version_info.get("MAJOR_MACRO") == "1", "Major version doesn't match"
    assert version_info.get("MINOR_MACRO") == "2", "Minor version doesn't match"
    assert version_info.get("PATCH_MACRO") == "3", "Patch version doesn't match"
```

## 💯 测试最佳实践

遵循以下最佳实践可以提高测试质量和可维护性：

1. **测试夹具使用**: 充分利用 `conftest.py` 中定义的 fixtures (`git_env`, `cmake_project` 等)，减少重复代码并确保测试环境一致性

2. **分类与标记**: 使用适当的 pytest markers 对测试进行分类，便于有选择性地运行相关测试组

3. **测试隔离**: 确保每个测试函数是完全独立的，不依赖于其他测试的执行结果或状态

4. **明确的断言消息**: 为每个断言提供清晰详细的失败消息，使调试过程更高效

5. **参数化测试**: 使用 `@pytest.mark.parametrize` 装饰器测试多种输入组合，提高测试覆盖率

6. **详细文档**: 为每个测试函数编写清晰的文档字符串，说明测试目的、步骤和预期结果

7. **测试粒度**: 每个测试函数应专注于验证一个特定功能点，避免过于复杂的测试逻辑

8. **边缘情况**: 不仅测试正常路径，还应考虑异常情况、错误处理和边界条件
