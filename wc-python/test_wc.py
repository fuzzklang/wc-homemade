from wc import (
    count_bytes_file,
    count_lines_file,
    count_words_file,
    count_characters_file,
    count_bytes_stream,
    count_bytes_stream_buffered,
    count_lines_stream_buffered,
    count_words_stream,
    count_lines_chars_and_bytes,
    count_lines_chars_and_bytes_b,
    count_lines_chars_and_bytes_c,
    count_all,
)

TESTFILE = "./test.txt"
NEWLINES = 7137
WORDS = 58159
CHARS = 331983
BYTES = 334699


def test_count_bytes_file() -> None:
    """Tests count number of bytes in a file.
    Corresponds to wc -c.
    Tested number differs from example at website since
    git converts all CR+LF to LF on Linux, thus reducing
    total number of bytes from original file on my machine."""
    assert count_bytes_file(TESTFILE) == BYTES


def test_count_lines_file() -> None:
    """Tests count number of lines in a file.
    Corresponds to wc -l"""
    assert count_lines_file(TESTFILE) == NEWLINES


def test_count_words_file() -> None:
    """Tests count number of words in a file.
    Corresponds to wc -w"""
    assert count_words_file(TESTFILE) == WORDS


def test_count_characters() -> None:
    """Tests locale dependent character count.
    Corresponds to wc -m.
    If the current locale does not support multibyte characters
    this will match wc -c"""
    assert count_characters_file(TESTFILE) == CHARS


def test_count_bytes() -> None:
    with open(TESTFILE, 'rb') as input_stream:
        assert count_bytes_stream(input_stream) == BYTES


def test_count_bytes_stream_buffered() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_bytes_stream_buffered(input_stream, 8192) == BYTES


def test_count_lines_stream_buffered() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_lines_stream_buffered(input_stream, 8192) == NEWLINES


def test_count_words_stream() -> None:
    with open(TESTFILE, 'r') as input_stream:
        assert count_words_stream(input_stream) == WORDS


def test_count_lines_chars_and_bytes() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_lines_chars_and_bytes(input_stream, 8192) == (NEWLINES, CHARS, BYTES)


def test_count_lines_chars_and_bytes_b() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_lines_chars_and_bytes_b(input_stream, 8192) == (NEWLINES, CHARS, BYTES)


def test_count_lines_chars_and_bytes_c() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_lines_chars_and_bytes_c(input_stream) == (NEWLINES, CHARS, BYTES)


def test_count_all() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_all(input_stream) == (NEWLINES, WORDS, CHARS, BYTES)
