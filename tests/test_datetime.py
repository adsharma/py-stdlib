import pytest

from stdlib.datetime import datetime


def test_datetime_now():
    dt = datetime.now()
    assert isinstance(dt, datetime)
    assert 2020 <= dt.year <= 2030  # Adjust this range as needed
    assert 1 <= dt.month <= 12
    assert 1 <= dt.day <= 31
    assert 0 <= dt.hour <= 23
    assert 0 <= dt.minute <= 59
    assert 0 <= dt.second <= 59
    assert 0 <= dt.microsecond <= 999999


def test_datetime_init():
    dt = datetime(2022, 12, 25, 12, 30, 45, 123456)
    assert dt.year == 2022
    assert dt.month == 12
    assert dt.day == 25
    assert dt.hour == 12
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456


def test_datetime_str():
    dt = datetime(2022, 12, 25, 12, 30, 45, 123456)
    expected_str = "2022-12-25 12:30:45.123456"
    assert str(dt) == expected_str


def disabled_test_datetime_invalid_input():
    with pytest.raises(TypeError):
        datetime("2022", 12, 25, 12, 30, 45, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 13, 25, 12, 30, 45, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 12, 32, 12, 30, 45, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 12, 25, 24, 30, 45, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 12, 25, 12, 60, 45, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 12, 25, 12, 30, 60, 123456)

    with pytest.raises(ValueError):
        datetime(2022, 12, 25, 12, 30, 45, 1000000)
