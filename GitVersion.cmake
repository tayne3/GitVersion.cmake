# GitVersion.cmake - CMake module for Git-based version management
# ===========================================
# See https://github.com/tayne3/GitVersion.cmake.git for usage and update instructions.
#
# MIT License
# -----------
#[[
  Copyright (c) 2025 tayne3 and contributors

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
]]

cmake_minimum_required(VERSION 3.12)

# Find Git executable / 查找 Git 可执行程序
find_package(Git QUIET)

# Main function that handles version extraction from Git
# 处理从 Git 提取版本的主函数
function(extract_version_from_git)
  # Parse arguments / 解析参数
  set(options FAIL_ON_MISMATCH)
  set(oneValueArgs OUTPUT_VERSION MAJOR MINOR PATCH DEFAULT_VERSION PREFIX SOURCE_DIR)
  cmake_parse_arguments(VERSION "${options}" "${oneValueArgs}" "" ${ARGN})
  
  # Validate required parameters / 验证必需参数
  if(NOT VERSION_OUTPUT_VERSION)
    message(FATAL_ERROR "GitVersion: Missing required parameter OUTPUT_VERSION.")
  endif()
  
  if(NOT VERSION_MAJOR)
    message(FATAL_ERROR "GitVersion: Missing required parameter MAJOR.")
  endif()
  
  if(NOT VERSION_MINOR)
    message(FATAL_ERROR "GitVersion: Missing required parameter MINOR.")
  endif()
  
  if(NOT VERSION_PATCH)
    message(FATAL_ERROR "GitVersion: Missing required parameter PATCH.")
  endif()
  
  # Set default values for optional parameters / 为可选参数设置默认值
  if(NOT VERSION_SOURCE_DIR)
    set(VERSION_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
  endif()
  
  if(NOT DEFINED VERSION_PREFIX)
    set(VERSION_PREFIX "")
  endif()
  
  if(NOT DEFINED VERSION_DEFAULT_VERSION)
    set(VERSION_DEFAULT_VERSION "0.0.0")
  endif()

  # Initialize with default values / 使用默认值初始化
  set(VERSION_MAJOR_VAL 0)
  set(VERSION_MINOR_VAL 0)
  set(VERSION_PATCH_VAL 0)
  
  # Parse default version / 解析默认版本
  set(RESOLVED_VERSION "${VERSION_DEFAULT_VERSION}")
  
  if(RESOLVED_VERSION MATCHES "^([0-9]+)\\.([0-9]+)\\.([0-9]+)(.*)$")
    set(VERSION_MAJOR_VAL "${CMAKE_MATCH_1}")
    set(VERSION_MINOR_VAL "${CMAKE_MATCH_2}")
    set(VERSION_PATCH_VAL "${CMAKE_MATCH_3}")
  else()
    message(WARNING "GitVersion: Default version '${RESOLVED_VERSION}' does not follow semver format.")
  endif()

  # Initialize version string / 初始化版本字符串
  set(VERSION_STRING "${RESOLVED_VERSION}")

  # Try to get version from Git / 尝试从 Git 获取版本
  if(GIT_FOUND AND EXISTS "${VERSION_SOURCE_DIR}/.git")
    # Set configuration dependency on Git HEAD / 设置配置依赖于 Git HEAD
    set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${VERSION_SOURCE_DIR}/.git/HEAD")
    
    # Execute git describe command / 执行 git describe 命令
    execute_process(
      COMMAND ${GIT_EXECUTABLE} -C "${VERSION_SOURCE_DIR}" describe --match "${VERSION_PREFIX}*.*.*" --tags --abbrev=9
      RESULT_VARIABLE GIT_RESULT
      OUTPUT_VARIABLE GIT_DESCRIBE
      OUTPUT_STRIP_TRAILING_WHITESPACE
      ERROR_QUIET
    )
    
    if(GIT_RESULT EQUAL "0")
      # Tag format: v1.2.3 or 1.2.3 / 标签格式: v1.2.3 或 1.2.3
      if(GIT_DESCRIBE MATCHES "^${VERSION_PREFIX}([0-9]+\\.[0-9]+\\.[0-9]+)$")
        # Exact tagged version / 精确的标签版本
        set(GIT_TAG ${CMAKE_MATCH_1})
        
        # Parse version numbers in one step using string operations / 使用字符串操作一步解析版本号
        if(GIT_TAG MATCHES "^([0-9]+)\\.([0-9]+)\\.([0-9]+)$")
          set(VERSION_MAJOR_VAL "${CMAKE_MATCH_1}")
          set(VERSION_MINOR_VAL "${CMAKE_MATCH_2}")
          set(VERSION_PATCH_VAL "${CMAKE_MATCH_3}")
        endif()
        
        set(VERSION_STRING "${GIT_TAG}")
        
        # Check if version matches default / 检查版本是否与默认值匹配
        if(VERSION_FAIL_ON_MISMATCH AND NOT GIT_TAG VERSION_EQUAL RESOLVED_VERSION)
          message(SEND_ERROR "GitVersion: Project version (${RESOLVED_VERSION}) does not match Git tag (${GIT_TAG}).")
        endif()
      
      # Format: v1.2.3-5-gabcdef123 or 1.2.3-5-gabcdef123 / 格式: v1.2.3-5-gabcdef123 或 1.2.3-5-gabcdef123
      elseif(GIT_DESCRIBE MATCHES "^${VERSION_PREFIX}([0-9]+\\.[0-9]+\\.[0-9]+)-([0-9]+)-g(.+)$")
        # Untagged pre-release version / 未标记的预发布版本
        set(GIT_TAG ${CMAKE_MATCH_1})
        set(GIT_COMMITS_AFTER_TAG ${CMAKE_MATCH_2})
        set(GIT_COMMIT ${CMAKE_MATCH_3})
        
        # Parse version numbers in one step / 一步解析版本号
        if(GIT_TAG MATCHES "^([0-9]+)\\.([0-9]+)\\.([0-9]+)$")
          set(VERSION_MAJOR_VAL "${CMAKE_MATCH_1}")
          set(VERSION_MINOR_VAL "${CMAKE_MATCH_2}")
          set(VERSION_PATCH_VAL "${CMAKE_MATCH_3}")
        endif()
        
        # Follow Semantic Versioning specification / 遵循语义化版本规范
        # Check if version is greater than the tagged version / 检查版本是否大于标记的版本
        if(VERSION_FAIL_ON_MISMATCH AND NOT RESOLVED_VERSION VERSION_GREATER GIT_TAG)
          message(SEND_ERROR "GitVersion: Project version (${RESOLVED_VERSION}) must be greater than tagged ancestor (${GIT_TAG}).")
        endif()
        
        # Use the format: version-dev.commits+commit / 使用格式: version-dev.commits+commit
        set(VERSION_STRING "${RESOLVED_VERSION}-dev.${GIT_COMMITS_AFTER_TAG}+${GIT_COMMIT}")
      else()
        message(WARNING "GitVersion: Failed to parse version from output of 'git describe': ${GIT_DESCRIBE}")
      endif()
    else()
      # Get latest commit hash / 获取最新的提交哈希
      execute_process(
        COMMAND ${GIT_EXECUTABLE} -C "${VERSION_SOURCE_DIR}" rev-parse --short=9 HEAD
        RESULT_VARIABLE GIT_RESULT
        OUTPUT_VARIABLE GIT_COMMIT
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
      )
      
      if(GIT_RESULT EQUAL "0")
        # Use commit hash when no tag is available / 在没有标签的情况下使用提交哈希
        set(VERSION_STRING "${RESOLVED_VERSION}+${GIT_COMMIT}")
      else()
        message(WARNING "GitVersion: Failed to get commit hash from Git.")
      endif()
    endif()
  else()
    if(NOT GIT_FOUND)
      message(STATUS "GitVersion: Git not found, using default version ${RESOLVED_VERSION}.")
    else()
      message(STATUS "GitVersion: Not a git repository, using default version ${RESOLVED_VERSION}.")
    endif()
  endif()

  # Set output variables in parent scope / 在父作用域中设置输出变量
  set(${VERSION_OUTPUT_VERSION} "${VERSION_STRING}" PARENT_SCOPE)
  set(${VERSION_MAJOR} "${VERSION_MAJOR_VAL}" PARENT_SCOPE)
  set(${VERSION_MINOR} "${VERSION_MINOR_VAL}" PARENT_SCOPE)
  set(${VERSION_PATCH} "${VERSION_PATCH_VAL}" PARENT_SCOPE)
  
  message(STATUS "GitVersion: Configured ${VERSION_OUTPUT_VERSION}=${VERSION_STRING}")
endfunction()

# Simplified version that works with named parameters / 使用命名参数的简化版本
function(git_version)
  extract_version_from_git(${ARGN})
endfunction() 
