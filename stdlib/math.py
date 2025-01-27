import ctypes
import sys

# Load the C math library
if sys.platform == "win32":
    # On Windows, the math library is part of the standard C library (msvcrt)
    libm = ctypes.CDLL("msvcrt")
elif sys.platform == "darwin":  # macOS
    libm = ctypes.CDLL("libSystem.dylib")
else:
    # On Unix-like systems, load libm
    libm = ctypes.CDLL("libm.so.6")

# Define the C functions with their argument and return types
libm.sin.argtypes = [ctypes.c_double]
libm.sin.restype = ctypes.c_double

libm.cos.argtypes = [ctypes.c_double]
libm.cos.restype = ctypes.c_double

libm.tan.argtypes = [ctypes.c_double]
libm.tan.restype = ctypes.c_double

libm.sqrt.argtypes = [ctypes.c_double]
libm.sqrt.restype = ctypes.c_double

libm.pow.argtypes = [ctypes.c_double, ctypes.c_double]
libm.pow.restype = ctypes.c_double

pi = 3.14159265358979323846


# Define Python functions to call the C functions
def sin(x: float) -> float:
    return libm.sin(x)


def cos(x: float) -> float:
    return libm.cos(x)


def tan(x: float) -> float:
    return libm.tan(x)


def sqrt(x: float) -> float:
    return libm.sqrt(x)


def pow(x: float, y: float) -> float:
    return libm.pow(x, y)


# Example usage
if __name__ == "__main__":
    import math

    x = 1.0
    y = 2.0

    print(f"sin({x}) = {sin(x)} (Python math.sin: {math.sin(x)})")
    print(f"cos({x}) = {cos(x)} (Python math.cos: {math.cos(x)})")
