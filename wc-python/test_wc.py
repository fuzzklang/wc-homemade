from wc import count_all

TESTFILE = "./test.txt"
NEWLINES = 7137
WORDS = 58159
CHARS = 331983
BYTES = 334699


def test_count_all() -> None:
    with open(TESTFILE, 'rb', buffering=8192) as input_stream:
        assert count_all(input_stream) == (NEWLINES, WORDS, CHARS, BYTES)
