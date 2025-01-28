# native/CMakeLists.txt
add_library(regex_wrapper SHARED src/libregex_wrapper.cpp)

# Include directories (if needed)
target_include_directories(regex_wrapper PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
