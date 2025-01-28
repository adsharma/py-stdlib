cmake_minimum_required(VERSION 3.10)
project(RegexWrapper LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Create a shared library
add_library(regex_wrapper SHARED src/regex_wrapper.cpp)

# Set output directory for the shared library
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Install the library (optional)
install(TARGETS regex_wrapper DESTINATION lib)
#install(FILES DESTINATION include)
