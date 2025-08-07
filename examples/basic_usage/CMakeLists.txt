cmake_minimum_required(VERSION 3.12)

include(../../cmake/GitVersion.cmake)
git_version_info(VERSION PROJECT_VERSION)
project(BasicExample VERSION ${PROJECT_VERSION})

message(STATUS "Project version: ${PROJECT_VERSION}")
message(STATUS "Major version: ${PROJECT_VERSION_MAJOR}")
message(STATUS "Minor version: ${PROJECT_VERSION_MINOR}")
message(STATUS "Patch version: ${PROJECT_VERSION_PATCH}")

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/version.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/version.h"
)

add_executable(basic_example main.cpp)
target_include_directories(basic_example PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
