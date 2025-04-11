cmake_minimum_required(VERSION 3.12)

# Include GitVersion.cmake
include(../../GitVersion.cmake)

# Extract version from Git
git_version(
  OUTPUT_VERSION PROJECT_VERSION
  MAJOR PROJECT_VERSION_MAJOR
  MINOR PROJECT_VERSION_MINOR
  PATCH PROJECT_VERSION_PATCH
)

# Create a project with the extracted version
project(BasicExample VERSION ${PROJECT_VERSION})

# Print version information
message(STATUS "Project version: ${PROJECT_VERSION}")
message(STATUS "Major version: ${PROJECT_VERSION_MAJOR}")
message(STATUS "Minor version: ${PROJECT_VERSION_MINOR}")
message(STATUS "Patch version: ${PROJECT_VERSION_PATCH}")

# Output version information to a file
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/version.h.in"
  "${CMAKE_CURRENT_BINARY_DIR}/version.h"
)

# Create a simple executable
add_executable(basic_example main.cpp)
target_include_directories(basic_example PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
