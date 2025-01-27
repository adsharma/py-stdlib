import time as py_time

import pytest

from stdlib.time import gmtime, localtime, sleep, time


def test_time():
    """
    Test that the custom time() function is close to Python's time().
    """
    custom_time = time()
    py_time_time = py_time.time()
    assert custom_time == pytest.approx(
        py_time_time, abs=0.1
    )  # Allow small delta for timing differences


def test_sleep():
    """
    Test that the custom sleep() function sleeps for the correct duration.
    """
    start = time()
    sleep(1)  # Sleep for 1 second
    end = time()
    assert end - start == pytest.approx(
        1.0, abs=0.1
    )  # Allow small delta for timing differences


def test_gmtime():
    """
    Test that the custom gmtime() matches Python's gmtime().
    """
    now = time()
    custom_gmtime = gmtime(now)
    py_gmtime = py_time.gmtime(now)

    # Compare all fields of struct_time
    assert custom_gmtime.tm_year == py_gmtime.tm_year
    assert custom_gmtime.tm_mon == py_gmtime.tm_mon
    assert custom_gmtime.tm_mday == py_gmtime.tm_mday
    assert custom_gmtime.tm_hour == py_gmtime.tm_hour
    assert custom_gmtime.tm_min == py_gmtime.tm_min
    assert custom_gmtime.tm_sec == py_gmtime.tm_sec
    assert custom_gmtime.tm_wday == py_gmtime.tm_wday
    assert custom_gmtime.tm_yday == py_gmtime.tm_yday
    assert custom_gmtime.tm_isdst == py_gmtime.tm_isdst


def test_localtime():
    """
    Test that the custom localtime() matches Python's localtime().
    """
    now = time()
    custom_localtime = localtime(now)
    py_localtime = py_time.localtime(now)

    # Compare all fields of struct_time
    assert custom_localtime.tm_year == py_localtime.tm_year
    assert custom_localtime.tm_mon == py_localtime.tm_mon
    assert custom_localtime.tm_mday == py_localtime.tm_mday
    assert custom_localtime.tm_hour == py_localtime.tm_hour
    assert custom_localtime.tm_min == py_localtime.tm_min
    assert custom_localtime.tm_sec == py_localtime.tm_sec
    assert custom_localtime.tm_wday == py_localtime.tm_wday
    assert custom_localtime.tm_yday == py_localtime.tm_yday
    assert custom_localtime.tm_isdst == py_localtime.tm_isdst


def test_gmtime_default():
    """
    Test that the custom gmtime() without arguments matches Python's gmtime().
    """
    custom_gmtime = gmtime()
    py_gmtime = py_time.gmtime()

    # Compare all fields of struct_time
    assert custom_gmtime.tm_year == py_gmtime.tm_year
    assert custom_gmtime.tm_mon == py_gmtime.tm_mon
    assert custom_gmtime.tm_mday == py_gmtime.tm_mday
    assert custom_gmtime.tm_hour == py_gmtime.tm_hour
    assert custom_gmtime.tm_min == py_gmtime.tm_min
    assert custom_gmtime.tm_sec == py_gmtime.tm_sec
    assert custom_gmtime.tm_wday == py_gmtime.tm_wday
    assert custom_gmtime.tm_yday == py_gmtime.tm_yday
    assert custom_gmtime.tm_isdst == py_gmtime.tm_isdst


def test_localtime_default():
    """
    Test that the custom localtime() without arguments matches Python's localtime().
    """
    custom_localtime = localtime()
    py_localtime = py_time.localtime()

    # Compare all fields of struct_time
    assert custom_localtime.tm_year == py_localtime.tm_year
    assert custom_localtime.tm_mon == py_localtime.tm_mon
    assert custom_localtime.tm_mday == py_localtime.tm_mday
    assert custom_localtime.tm_hour == py_localtime.tm_hour
    assert custom_localtime.tm_min == py_localtime.tm_min
    assert custom_localtime.tm_sec == py_localtime.tm_sec
    assert custom_localtime.tm_wday == py_localtime.tm_wday
    assert custom_localtime.tm_yday == py_localtime.tm_yday
    assert custom_localtime.tm_isdst == py_localtime.tm_isdst
