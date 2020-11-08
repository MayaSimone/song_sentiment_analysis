from collections import Counter
import pytest

from song_analysis import (
    format_name,
)

format_name_cases = [
    # 0: Check an empty string.
    ("", ""),
    # 1: Check a case in which there are no capital letter, spaces, or
    # punctuation characters.
    ("panicatthedisco", "panicatthedisco"),
    # 2: Check a case with spaces.
    ("panic at the disco", "panicatthedisco"),
    # 3: Check a case with capital letters.
    ("PanicAtTheDisco", "panicatthedisco"),
    # 4: Check a case with punctuation.
    ("panic!atthedisco", "panicatthedisco"),
    # 5: Check a case that is a string of only spaces.
    ("   ", ""),
    # 6: Check a case that is a string of only capital letters.
    ("PANICATTHEDISCO", "panicatthedisco"),
    # 7: Check a case that is a string of only punctuation.
    ("!@#$%^&*()_+-=}{][<>?.,/|~`", ""),
    # 8: Check a case with spaces and punctuation.
    ("panic! at the disco", "panicatthedisco"),
    # 9: Check a case with spaces and capitalization.
    ("Panic At The Disco", "panicatthedisco"),
    # 10: Check a case with capitalization and punctuation.
    ("Panic!AtTheDisco", "panicatthedisco"),
    # 11: Check a case with spaces, capital letters, and punctuation.
    ("Panic! At The Disco", "panicatthedisco")
]

@pytest.mark.parametrize("name,formatted", format_name_cases)
def test_format_name(name, formatted):
    assert format_name(name) == formatted