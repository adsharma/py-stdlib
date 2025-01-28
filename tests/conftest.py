# tests/conftest.py
import pytest

from stdlib import re


@pytest.fixture
def regex_matcher():
    """Fixture to provide the match function."""
    return re.match
