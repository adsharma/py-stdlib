import sys

import cffi


def load_library(lib_name):
    """
    Load a shared library based on the operating system.

    Args:
        lib_name (str): The base name of the library (without extension or 'lib' prefix).

    Returns:
        ctypes.CDLL: The loaded shared library.
    """
    # Determine the library extension based on the OS
    if sys.platform == "linux":
        lib_ext = ".so"
    elif sys.platform == "darwin":  # macOS
        lib_ext = ".dylib"
    elif sys.platform == "win32":  # Windows
        lib_ext = ".dll"
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")

    # Construct the full library name
    lib_filename = (
        f"lib{lib_name}{lib_ext}" if sys.platform != "win32" else f"{lib_name}{lib_ext}"
    )

    ffi = cffi.FFI()
    ffi.cdef(
        """
             bool match(const char* pattern, const char* text);
             """
    )
    return ffi.dlopen(lib_filename)


# Load the shared library
lib = load_library("regex_wrapper")


def match(pattern, text):
    return lib.match(pattern.encode("utf-8"), text.encode("utf-8"))


# Example usage
if __name__ == "__main__":
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    text = "123-45-6789"

    if match(pattern, text):
        print("Match found!")
    else:
        print("No match.")
