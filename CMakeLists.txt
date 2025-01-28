cmake_minimum_required(VERSION 3.10)
project(RegexWrapper LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add the native/src directory
add_subdirectory(native)

# Install the library (optional)
install(TARGETS regex_wrapper DESTINATION lib)
#install(FILES DESTINATION include)
