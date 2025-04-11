#include <iostream>

#include "version.h"

int main() {
  std::cout << "Basic Example Application" << std::endl;
  std::cout << "------------------------" << std::endl;
  std::cout << "Version: " << PROJECT_VERSION << std::endl;
  std::cout << "Major: " << PROJECT_VERSION_MAJOR << std::endl;
  std::cout << "Minor: " << PROJECT_VERSION_MINOR << std::endl;
  std::cout << "Patch: " << PROJECT_VERSION_PATCH << std::endl;

  return 0;
}
