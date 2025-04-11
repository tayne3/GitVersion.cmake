# GitVersion Examples

This directory contains example projects demonstrating how to use the GitVersion.cmake module.

## Basic Usage

The `basic_usage` directory contains a minimal example showing how to use GitVersion.cmake to extract version information from Git tags.

### Building the Basic Example

```sh
mkdir build
cd build
cmake ..
cmake --build .
```

### Running the Basic Example

```sh
./basic_example
```

This will display the version information extracted from Git tags or the default version if no tags are available.

## Version Formats

GitVersion.cmake supports various version formats:

1. Exact Tag: When the HEAD is exactly at a tag (e.g., `1.2.3`)
2. Development Version: When commits exist after a tag (e.g., `1.2.3-dev.5+abc1234`)
3. No Tag: When no tag exists (e.g., `0.0.0+abc1234`)

## Configuration Options

See the main README.md in the project root for a full list of configuration options. 
