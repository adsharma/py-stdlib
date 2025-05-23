import pytest

from stdlib.re import CompiledRegex, error as re_error


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
    with pytest.raises(re_error, match="Invalid regex pattern"):
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


# Fixture to create a CompiledRegex object for testing
@pytest.fixture
def compiled_regex():
    return CompiledRegex(r"\d+")


# Test cases for the `search` method
def test_search_found(compiled_regex): # compiled_regex fixture uses r"\d+"
    text = "There are 123 apples and 456 oranges."
    match_obj = compiled_regex.search(text)
    assert match_obj is not None
    assert match_obj.group(0) == "123"  # First match should be "123"
    assert match_obj.groups() == ()     # No capturing groups in r"\d+"


def test_search_not_found(compiled_regex):
    text = "There are no numbers here."
    result = compiled_regex.search(text)
    assert result is None  # No match should return None


# Test cases for the `findall` method
def test_findall_multiple_matches(compiled_regex):
    text = "There are 123 apples and 456 oranges."
    result = compiled_regex.findall(text)
    assert result == ["123", "456"]  # All matches should be returned


def test_findall_no_matches(compiled_regex):
    text = "There are no numbers here."
    result = compiled_regex.findall(text)
    assert result == []  # No matches should return an empty list


def test_findall_empty_string(compiled_regex):
    text = ""
    result = compiled_regex.findall(text)
    assert result == []  # Empty string should return an empty list


# Test cases for the `sub` method
def test_sub_single_replacement(compiled_regex):
    text = "There are 123 apples."
    result = compiled_regex.sub("NUM", text)
    assert result == "There are NUM apples."  # Single replacement


def test_sub_multiple_replacements(compiled_regex):
    text = "There are 123 apples and 456 oranges."
    result = compiled_regex.sub("NUM", text)
    assert result == "There are NUM apples and NUM oranges."  # Multiple replacements


def test_sub_no_matches(compiled_regex):
    text = "There are no numbers here."
    result = compiled_regex.sub("NUM", text)
    assert result == text  # No matches, original text should be returned


def test_sub_empty_string(compiled_regex):
    text = ""
    result = compiled_regex.sub("NUM", text)
    assert result == ""  # Empty string should remain unchanged


# Edge case: Invalid regex pattern
def test_invalid_regex_pattern():
    with pytest.raises(re_error):
        CompiledRegex(r"*invalid")  # Invalid regex pattern should raise re_error


# Tests for character classes
def test_char_classes():
    assert CompiledRegex(r"\d").match("5")
    assert not CompiledRegex(r"\d").match("a")
    assert CompiledRegex(r"\w").match("w")
    assert CompiledRegex(r"\w").match("_")
    assert not CompiledRegex(r"\w").match("-")
    assert CompiledRegex(r"\s").match(" ")
    assert not CompiledRegex(r"\s").match("a")
    # Test '.' with match (full string match, so a single dot pattern needs a single char string)
    assert CompiledRegex(r".").match("a") 
    assert not CompiledRegex(r".").match("ab")
    assert not CompiledRegex(r".").match("")
    # Test '.' with search
    match_dot = CompiledRegex(r".").search("abc")
    assert match_dot is not None and match_dot.group(0) == "a"

    assert CompiledRegex(r"[abc]").match("a")
    assert not CompiledRegex(r"[abc]").match("d")
    assert CompiledRegex(r"[a-zA-Z]").match("X")
    assert not CompiledRegex(r"[a-zA-Z]").match("5")


# Tests for quantifiers
def test_quantifiers():
    assert CompiledRegex(r"a*").match("aaa")
    assert CompiledRegex(r"a*").match("")
    assert CompiledRegex(r"a+").match("a")
    assert not CompiledRegex(r"a+").match("")
    assert CompiledRegex(r"a?").match("a")
    assert CompiledRegex(r"a?").match("")
    
    # {m,n}
    assert CompiledRegex(r"a{2,4}").match("aa")
    assert CompiledRegex(r"a{2,4}").match("aaaa")
    assert not CompiledRegex(r"a{2,4}").match("a")
    assert not CompiledRegex(r"a{2,4}").match("aaaaa")
    
    # {m,}
    assert CompiledRegex(r"a{2,}").match("aa")
    assert CompiledRegex(r"a{2,}").match("aaaaa")
    assert not CompiledRegex(r"a{2,}").match("a")
    
    # {,n} - std::regex interprets {0,n}
    # A pattern like "a{,3}" means "up to 3 'a's".
    # For std::regex, this is typically written as "a{0,3}".
    # Let's test if `compile` handles it or if it's an error.
    # If it compiles, it should match "aaa", "aa", "a", "".
    try:
        # This syntax might be invalid for std::regex.
        # Python's re module supports it.
        r = CompiledRegex(r"a{,3}")
        assert r.match("aaa")
        assert r.match("aa")
        assert r.match("a")
        assert r.match("")
        assert not r.match("aaaa")
    except re_error:
        # If it's an error, this means std::regex does not support {,n}
        # We can then test "a{0,3}" explicitly if desired.
        # For now, we acknowledge this difference if it occurs.
        print("Note: Quantifier {,n} might not be supported or interpreted as {0,n} by underlying std::regex.")
        # As a fallback, test the equivalent supported by std::regex
        r_explicit_zero = CompiledRegex(r"a{0,3}")
        assert r_explicit_zero.match("aaa")
        assert r_explicit_zero.match("")
        assert not r_explicit_zero.match("aaaa")


# Tests for anchors
def test_anchors():
    # Test ^ and $ with search (should return MatchObject)
    match_start = CompiledRegex(r"^start").search("start of line")
    assert match_start is not None and match_start.group(0) == "start"

    match_end = CompiledRegex(r"end$").search("line ends with end")
    assert match_end is not None and match_end.group(0) == "end"
    
    # Test ^ and $ with match (full string match inherent to std::regex_match)
    assert CompiledRegex(r"^exact$").match("exact")
    assert not CompiledRegex(r"^exact$").match("not exact")
    # Test without explicit anchors, std::regex_match implies them
    assert CompiledRegex(r"exact").match("exact") 
    assert not CompiledRegex(r"exact").match("not exact")
    assert not CompiledRegex(r"start").match("start of the text") # match is full string

    # Test word boundaries (\b) with search
    # std::regex (ECMAScript flavor by default) supports \b
    match_wb1 = CompiledRegex(r"\bword\b").search("word")
    assert match_wb1 is not None and match_wb1.group(0) == "word"

    match_wb2 = CompiledRegex(r"\bword\b").search("a word in a sentence")
    assert match_wb2 is not None and match_wb2.group(0) == "word"
    
    assert CompiledRegex(r"\bword\b").search("anotherword") is None # word is part of anotherword
    
    match_wb3 = CompiledRegex(r"word\b").search("leadingword")
    assert match_wb3 is not None and match_wb3.group(0) == "word"

    match_wb4 = CompiledRegex(r"\bword").search("wordtrailing")
    assert match_wb4 is not None and match_wb4.group(0) == "word"


# Tests for search() with capturing groups
def test_search_with_groups():
    # Pattern with two capturing groups
    regex = CompiledRegex(r"(\w+)\s*=\s*(\d+)")
    text = "item1 = 100 and item2 = 200" # search finds first match
    
    match = regex.search(text)
    assert match is not None
    assert match.group(0) == "item1 = 100"  # Full match
    assert match.group(1) == "item1"        # First group
    assert match.group(2) == "100"          # Second group
    assert match.groups() == ("item1", "100") # Tuple of all captured groups

    # Test accessing a non-existent group by positive index
    with pytest.raises(IndexError):
        match.group(3)
    # Test accessing group by negative index (not supported by this MatchObject)
    with pytest.raises(IndexError): # Or TypeError depending on implementation, IndexError is more Pythonic
        match.group(-1)


    # Test search that finds nothing
    regex_no_match = CompiledRegex(r"nonexistentpattern")
    assert regex_no_match.search("text with no pattern") is None

    # Pattern with one group
    regex_one_group = CompiledRegex(r"name: (\w+)")
    text_one_group = "name: Alice"
    match_one_group = regex_one_group.search(text_one_group)
    assert match_one_group is not None
    assert match_one_group.group(0) == "name: Alice"
    assert match_one_group.group(1) == "Alice"
    assert match_one_group.groups() == ("Alice",)

    # Pattern with no capturing groups (should still return a MatchObject)
    regex_no_groups = CompiledRegex(r"\d+") # Fixture compiled_regex uses this
    text_no_groups = "12345"
    match_no_groups = regex_no_groups.search(text_no_groups)
    assert match_no_groups is not None
    assert match_no_groups.group(0) == "12345"
    assert match_no_groups.groups() == () # Empty tuple for no groups


# Test for MatchObject methods with different group configurations
def test_match_object_groups_method():
    # Match with multiple groups
    mo_multiple = CompiledRegex(r"(\w+)-(\d+)").search("data-123")
    assert mo_multiple is not None
    assert mo_multiple.groups() == ("data", "123")

    # Match with one group
    mo_single = CompiledRegex(r"(\w+)-\d+").search("data-123") # Group is (\w+)
    assert mo_single is not None
    assert mo_single.groups() == ("data",) # Corrected from "abc"

    # Match with zero explicit capturing groups
    mo_zero_capturing = CompiledRegex(r"\w+-\d+").search("data-123")
    assert mo_zero_capturing is not None
    assert mo_zero_capturing.groups() == ()

    # Match with non-capturing groups (?:...)
    # std::regex (ECMAScript flavor) supports non-capturing groups
    mo_non_capturing = CompiledRegex(r"(?:\w+)-(\d+)").search("data-123")
    assert mo_non_capturing is not None
    assert mo_non_capturing.groups() == ("123",) # Only captures the group '(\d+)'


# Test cases for the `sub` method with group references
def test_sub_with_group_references():
    # Test with numbered group references (e.g., $1, $2)
    regex_groups = CompiledRegex(r"(\w+)\s*:\s*(\w+)") # e.g., key : value
    text = "name : Alice , age : 30"
    # Swap key and value: "$2 : $1"
    result = regex_groups.sub(r"$2 : $1", text)
    assert result == "Alice : name , 30 : age"

    # Test with the whole match ($&)
    regex_word = CompiledRegex(r"\b\w+\b") # Matches whole words
    text_words = "hello world"
    result_amp = regex_word.sub(r"[$&]", text_words) # Enclose each word in []
    assert result_amp == "[hello] [world]"

    # Test with $` (preceding part) - less common, but part of ECMAScript spec
    # For "---abc---", if "abc" is matched, $` is "---"
    # This might be tricky with multiple matches. std::regex_replace processes iteratively.
    # Let's test a single match scenario for simplicity.
    regex_middle = CompiledRegex(r"middle")
    text_parts = "before-middle-after"
    result_pre = regex_middle.sub(r"[$`]", text_parts) 
    assert result_pre == "before-[before-]-after"

    # Test with $' (following part)
    # For "---abc---", if "abc" is matched, $' is "---"
    result_post = regex_middle.sub(r"[$']", text_parts)
    assert result_post == "before-[-after]-after"
    
    # Test with $$ (literal $)
    result_dollar = regex_groups.sub(r"$$$1-$2", text) # Results in "$key-value"
    assert result_dollar == "$name-Alice , $age-30"

    # Test sub with no match - should return original string
    text_no_match = "no groups here"
    result_no_match = regex_groups.sub(r"$1", text_no_match)
    assert result_no_match == text_no_match

    # Test sub with an empty replacement string
    text_to_empty = "remove all vowels"
    regex_vowels = CompiledRegex(r"[aeiou]")
    result_empty = regex_vowels.sub("", text_to_empty)
    assert result_empty == "rmv ll vwls"


# Test cases for the `findall` method with group behaviors
def test_findall_with_groups():
    # Case 1: No capturing groups (mark_count == 0)
    # The compiled_regex fixture uses r"\d+", which has 0 capturing groups.
    # Its mark_count should be 0.
    regex_no_groups = CompiledRegex(r"\d+")
    assert regex_no_groups.mark_count == 0 
    text_no_groups = "123 abc 456 def 789"
    result_no_groups = regex_no_groups.findall(text_no_groups)
    assert result_no_groups == ["123", "456", "789"] # List of full matches

    # Case 2: One capturing group (mark_count == 1)
    regex_one_group = CompiledRegex(r"name: (\w+)") # Group 1 is (\w+)
    assert regex_one_group.mark_count == 1
    text_one_group = "name: Alice, name: Bob, name: Charlie"
    result_one_group = regex_one_group.findall(text_one_group)
    assert result_one_group == ["Alice", "Bob", "Charlie"] # List of strings from group 1

    # Case 3: More than one capturing group (mark_count > 1)
    regex_multiple_groups = CompiledRegex(r"(\w+)\s*=\s*(\d+)") # group 1: (\w+), group 2: (\d+)
    assert regex_multiple_groups.mark_count == 2
    text_multiple_groups = "item1 = 100, item2 = 200, item3 = 300"
    result_multiple_groups = regex_multiple_groups.findall(text_multiple_groups)
    expected_multiple = [("item1", "100"), ("item2", "200"), ("item3", "300")]
    assert result_multiple_groups == expected_multiple # List of tuples of strings

    # Test findall with no matches (for each group case)
    text_no_match_here = "no relevant data here"
    assert regex_no_groups.findall(text_no_match_here) == []
    assert regex_one_group.findall(text_no_match_here) == []
    assert regex_multiple_groups.findall(text_no_match_here) == []

    # Test findall on an empty string
    assert regex_no_groups.findall("") == []
    assert regex_one_group.findall("") == []
    assert regex_multiple_groups.findall("") == []

    # Test findall with a pattern that can produce empty matches (e.g. r"a*")
    # C++ code was updated to handle potential infinite loops with empty matches.
    regex_empty_match = CompiledRegex(r"a*") # 0 groups
    assert regex_empty_match.mark_count == 0
    # "baca" -> "" (match before 'b'), "a" (match 'a'), "" (match after 'c'), "" (match after 'a')
    # Python's re.findall('a*', 'baca') -> ['', 'a', '', 'a', ''] - includes empty match at end
    # My C++ code search_start advancement logic:
    #   - After matching "a" in "baca", search_start points to "ca".
    #   - `regex_search` on "ca" with "a*" matches "" at "c". suffix is "ca". search_start becomes "a".
    #   - `regex_search` on "a" with "a*" matches "a". suffix is "". search_start becomes end.
    #   - `regex_search` on "" with "a*" matches "". suffix is "". search_start becomes end.
    # The loop termination condition (search_start == s_text.cbegin() && current_match[0].length() == 0)
    # plus advancing search_start if current_match is empty should handle this.
    # The specific behavior for empty matches with findall can be subtle.
    # Python's re.findall for 'a*' on 'baca' is ['', 'a', '', 'a', '']
    # My current C++ loop:
    # "baca":
    # 1. search "baca", match "" at "b", add "", search_start -> "b"
    # 2. search "baca"+1, match "a", add "a", search_start -> "c"
    # 3. search "baca"+2, match "" at "c", add "", search_start -> "a"
    # 4. search "baca"+3, match "a", add "a", search_start -> end
    # 5. search "baca"+4 (empty), match "", add "", search_start -> end (loop terminates)
    # Expected: ["", "a", "", "a", ""]
    assert regex_empty_match.findall("baca") == ["", "a", "", "a", ""]


    regex_empty_one_group = CompiledRegex(r"(a*)b") # Group 1 is (a*)
    assert regex_empty_one_group.mark_count == 1
    # Python: re.findall('(a*)b', 'ab caab') -> ['a', 'aa']
    assert regex_empty_one_group.findall("ab caab") == ["a", "aa"]

    regex_empty_multi_group = CompiledRegex(r"(a*):(b*)") # Group 1 (a*), Group 2 (b*)
    assert regex_empty_multi_group.mark_count == 2
    # Python: re.findall('(a*):(b*)', 'a::b aa:bb :') -> [('a', ''), ('', 'b'), ('aa', 'bb'), ('', '')]
    assert regex_empty_multi_group.findall("a::b aa:bb :") == [("a", ""), ("", "b"), ("aa", "bb"), ("", "")]
