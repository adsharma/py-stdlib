import pytest

from stdlib.re import CompiledRegex


def test_match_simple_pattern(regex_matcher):
    """Test matching a simple pattern."""
    assert regex_matcher(r"^\d{3}-\d{2}-\d{4}$", "123-45-6789") == True
    assert regex_matcher(r"^\d{3}-\d{2}-\d{4}$", "123-456-789") == False


def test_match_email(regex_matcher):
    """Test matching an email address."""
    assert (
        regex_matcher(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "test@example.com"
        )
        == True
    )
    assert (
        regex_matcher(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "invalid-email"
        )
        == False
    )


def test_match_empty_string(regex_matcher):
    """Test matching an empty string."""
    assert regex_matcher(r"^$", "") == True
    assert regex_matcher(r"^$", "not empty") == False


def test_match_invalid_pattern(regex_matcher):
    """Test matching with an invalid regex pattern."""
    assert (
        regex_matcher(r"invalid[", "text") == False
    )  # Invalid pattern should return False


def test_match_case_sensitive(regex_matcher):
    """Test case-sensitive matching."""
    assert regex_matcher(r"hello", "hello") == True
    assert regex_matcher(r"hello", "HELLO") == False


def test_match_with_anchors(regex_matcher):
    """Test matching with start (^) and end ($) anchors."""
    # These tests should pass because std::regex_match enforces full-string matching
    assert (
        regex_matcher(r"start", "start of the text") == False
    )  # "start" is not the full string
    assert (
        regex_matcher(r"end", "text ends with end") == False
    )  # "end" is not the full string
    assert regex_matcher(r"exact", "exact") == True  # "exact" is the full string
    assert (
        regex_matcher(r"exact", "not exact") == False
    )  # "not exact" is not the full string


# Test valid regex compilation and matching
def test_valid_regex():
    regex = CompiledRegex(r"\d+")  # Compile a regex pattern for digits
    assert regex.match("123") is True  # Should match
    assert regex.match("abc") is False  # Should not match


# Test invalid regex pattern
def test_invalid_regex():
    with pytest.raises(ValueError, match="Invalid regex pattern"):
        CompiledRegex(r"*invalid*")  # Invalid regex pattern


# Test matching with a compiled regex
def test_match_compiled():
    regex = CompiledRegex(r"[A-Za-z]+")  # Compile a regex pattern for letters
    assert regex.match("Hello") is True  # Should match
    assert regex.match("123") is False  # Should not match


# Test multiple regex instances
def test_multiple_regex_instances():
    regex1 = CompiledRegex(r"\d{3}")  # Compile a regex pattern for exactly 3 digits
    regex2 = CompiledRegex(r"[a-z]+")  # Compile a regex pattern for lowercase letters

    assert regex1.match("123") is True  # Should match
    assert regex1.match("12") is False  # Should not match

    assert regex2.match("abc") is True  # Should match
    assert regex2.match("ABC") is False  # Should not match


# Test releasing compiled regex
def test_release_compiled():
    regex = CompiledRegex(r"\w+")  # Compile a regex pattern for word characters
    assert regex.match("word") is True  # Should match
    del regex  # Release the compiled regex
    # No direct way to test if the C++ object was released, but this ensures no crashes


# Test edge cases
def test_edge_cases():
    # Empty pattern
    regex = CompiledRegex(r"")
    assert regex.match("") is True  # Should match empty string
    assert regex.match("a") is False  # Expected behavior of std::regex

    # Complex pattern
    regex = CompiledRegex(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    )  # Email regex
    assert regex.match("test@example.com") is True  # Should match
    assert regex.match("invalid-email") is False  # Should not match
