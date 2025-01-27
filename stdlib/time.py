import ctypes
import ctypes.util
from typing import NamedTuple, Optional

from stdlib._os_types import libc


# Define time.struct_time manually
class struct_time(NamedTuple):
    tm_year: int  # Year, e.g., 2023
    tm_mon: int  # Month, 1-12
    tm_mday: int  # Day of the month, 1-31
    tm_hour: int  # Hour, 0-23
    tm_min: int  # Minute, 0-59
    tm_sec: int  # Second, 0-61 (60 and 61 are leap seconds)
    tm_wday: int  # Day of the week, 0-6 (0 is Monday)
    tm_yday: int  # Day of the year, 1-366
    tm_isdst: int  # Daylight savings flag, -1, 0, or 1


# Define tm structure for C
class tm(ctypes.Structure):
    _fields_ = [
        ("tm_sec", ctypes.c_int),
        ("tm_min", ctypes.c_int),
        ("tm_hour", ctypes.c_int),
        ("tm_mday", ctypes.c_int),
        ("tm_mon", ctypes.c_int),
        ("tm_year", ctypes.c_int),
        ("tm_wday", ctypes.c_int),
        ("tm_yday", ctypes.c_int),
        ("tm_isdst", ctypes.c_int),
    ]


# Define necessary types and structures
class timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long)]


class timespec(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]


libc.gmtime.restype = ctypes.POINTER(tm)
libc.localtime.restype = ctypes.POINTER(tm)


# Pure Python implementation of gmtime and localtime using libc
def gmtime(seconds: Optional[float] = None) -> struct_time:
    """
    Equivalent to time.gmtime() in Python.
    """
    if seconds is None:
        seconds = time()
    time_t = int(seconds)
    tm_ptr = libc.gmtime(ctypes.byref(ctypes.c_long(time_t)))
    tm_struct = tm_ptr.contents
    return struct_time(
        tm_year=tm_struct.tm_year + 1900,  # Years since 1900
        tm_mon=tm_struct.tm_mon + 1,  # Months are 0-11 in C
        tm_mday=tm_struct.tm_mday,
        tm_hour=tm_struct.tm_hour,
        tm_min=tm_struct.tm_min,
        tm_sec=tm_struct.tm_sec,
        tm_wday=tm_struct.tm_wday,
        tm_yday=tm_struct.tm_yday + 1,  # Days are 0-365 in C
        tm_isdst=tm_struct.tm_isdst,
    )


def localtime(seconds: Optional[float] = None) -> struct_time:
    """
    Equivalent to time.localtime() in Python.
    """
    if seconds is None:
        seconds = time()
    time_t = int(seconds)
    tm_ptr = libc.localtime(ctypes.byref(ctypes.c_long(time_t)))
    tm_struct = tm_ptr.contents
    return struct_time(
        tm_year=tm_struct.tm_year + 1900,  # Years since 1900
        tm_mon=tm_struct.tm_mon + 1,  # Months are 0-11 in C
        tm_mday=tm_struct.tm_mday,
        tm_hour=tm_struct.tm_hour,
        tm_min=tm_struct.tm_min,
        tm_sec=tm_struct.tm_sec,
        tm_wday=tm_struct.tm_wday,
        tm_yday=tm_struct.tm_yday + 1,  # Days are 0-365 in C
        tm_isdst=tm_struct.tm_isdst,
    )


# Define functions using ctypes
def gettimeofday(tv: timeval, tz: Optional[ctypes.c_void_p]) -> None:
    """
    Equivalent to gettimeofday() in C.
    """
    libc.gettimeofday(ctypes.byref(tv), tz)


def clock_gettime(clk_id: int, tp: timespec) -> None:
    """
    Equivalent to clock_gettime() in C.
    """
    libc.clock_gettime(clk_id, ctypes.byref(tp))


def clock_settime(clk_id: int, tp: timespec) -> None:
    """
    Equivalent to clock_settime() in C.
    """
    libc.clock_settime(clk_id, ctypes.byref(tp))


# Define constants for clock_gettime and clock_settime
CLOCK_REALTIME: int = 0


# Implement Python time functions using FFI
def time() -> float:
    """
    Equivalent to time.time() in Python.
    """
    tv = timeval()
    gettimeofday(tv, None)
    return tv.tv_sec + tv.tv_usec / 1_000_000


def sleep(seconds: float) -> None:
    """
    Equivalent to time.sleep() in Python.
    """
    libc.usleep(int(seconds * 1_000_000))
