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
