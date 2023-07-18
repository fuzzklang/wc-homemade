# /usr/bin/env python

import argparse
import os
import sys

from typing import (
    Dict,
    BinaryIO,
    TextIO,
    Tuple
)


def main() -> None:
    parser = setup_argparse()
    mode = get_mode(parser)
    filepath = parser.parse_args().FILE

    counts: Tuple[int,int,int,int]

    if filepath and filepath != "-":
        with open(filepath, 'rb') as stream:
            counts = count_all(stream)
    else:
        counts = count_all(sys.stdin.buffer)

    sys.stdout.write(get_output_string(counts, mode, filepath))
    sys.exit(0)


def get_output_string(results: Tuple[int,int,int,int], mode, filepath):
    output_string = ""

    # Check if interactive terminal
    if os.isatty(sys.stdout.fileno()):
        delimiter = ' '
    else:
        delimiter = '\n'

    if mode['lines']:
        output_string += f" {results[0]}" + delimiter
    if mode['words']:
        output_string += f"{results[1]}" + delimiter
    if mode['bytes']:
        output_string += f"{results[2]}" + delimiter
    if mode['chars']:
        output_string += f"{results[3]}" + delimiter

    if filepath and filepath != '-':
        output_string += f"{filepath}"

    output_string = output_string.rstrip() + '\n'

    return output_string


def count_all(stream: BinaryIO) -> Tuple[int, int, int, int]:
    line_count = 0
    word_count = 0
    char_count = 0
    byte_count = 0

    while bytes_read := stream.readline():
        as_text = bytes_read.decode('utf-8')
        line_count += 1
        char_count += len(as_text)
        word_count += len(as_text.split())
        byte_count += len(bytes_read)
    return (line_count, word_count, char_count, byte_count)


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="wc tool for files and stdin")
    parser.add_argument('-c', '--bytes', help="count number of bytes", action="store_true")
    parser.add_argument('-l', '--lines', help="count number of lines", action="store_true")
    parser.add_argument('-w', '--words', help="count number of words", action="store_true")
    parser.add_argument('-m', '--chars', help="count number of characters", action="store_true")
    parser.add_argument('FILE', type=str, nargs='?', help="Input file, - or empty for stdin")
    return parser


def get_mode(parser: argparse.ArgumentParser) -> Dict[str, bool]:
    default_mode = {
        "bytes": True,
        "lines": True,
        "words": True,
        "chars": False,
    }

    args = parser.parse_args()
    if (args.bytes or args.lines or args.words or args.chars):
        mode = {
            'bytes': args.bytes,
            'words': args.words,
            'lines': args.lines,
            'chars': args.chars,
        }
    else:
        mode = default_mode
    return mode


if __name__ == "__main__":
    main()



##########################
####### DEPRECATED #######
##########################

### only for timings and comparisons

def run_on_file_input(filepath: str) -> Tuple[int, int, int, int]:
    return (
        count_bytes_file(filepath),
        count_lines_file(filepath),
        count_words_file(filepath),
        count_characters_file(filepath)
    )


def run_on_stdin(mode: Dict[str, bool]) -> Tuple[int, int, int, int]:
    """Seperate calculation on
        - byte, line or char
        - word
        - all
    """
    line_count = 0
    word_count = 0
    char_count = 0
    byte_count = 0

    if (mode['lines'] or mode['bytes'] or mode['chars']) and not mode['word']:
        # Use BinaryIO
        byte_count, line_count, char_count = count_lines_chars_and_bytes(sys.stdin.buffer)
    elif mode['word'] and not (mode['lines'] or mode['bytes'] or mode['chars']):
        # Use TextIO
        word_count = count_words_stream(sys.stdin)
    else:
        byte_count, line_count, char_count, word_count = count_all(sys.stdin.buffer)

    return (line_count, word_count, char_count, byte_count)


def count_bytes_file(filepath: str) -> int:
    return os.path.getsize(filepath)


def count_lines_file(filepath: str) -> int:
    with open(filepath, 'r') as f:
        return len(f.readlines())


def count_words_file(filepath: str) -> int:
    with open(filepath, 'r') as f:
        count = 0
        for l in f.readlines():
            count += len(l.split())
        return count


def count_characters_file(filepath: str) -> int:
    with open(filepath, 'r') as f:
        count = 0
        for l in f.readlines():
            count += len(l)
        return count


def count_bytes_and_characters(stream: BinaryIO, buf_size: int = 8192) -> Tuple[int, int]:
    bytes_count = 0
    char_count = 0
    while bytes_read := stream.read(buf_size):
        bytes_count += len(bytes_read)
        for c in bytes_read:
            if c & 0xC0 != 0x80:
                char_count += 1
    return (bytes_count, char_count)


def count_lines_stream_buffered(stream: BinaryIO, buf_size: int = 8192) -> int:
    line_count = 0
    while bytes_read := stream.read(buf_size):
        line_count += bytes_read.count(b'\n')
    return line_count


def count_words_binary_stream(stream: BinaryIO, buf_size=None) -> int:
    word_count = 0

    while bytes_read := stream.readline():
        as_text = bytes_read.decode('utf-8')
        word_count += len(as_text.split())
    return word_count


def count_lines_chars_and_bytes(stream: BinaryIO, buf_size: int = 8192) -> Tuple[int, int, int]:
    line_count = 0
    char_count = 0
    byte_count = 0
    while bytes_read := stream.read(buf_size):
        byte_count += len(bytes_read)
        for c in bytes_read:
            if c & 0xC0 != 0x80:
                # UTF-8 multibytes start with 10xxxxxx,
                # ignore these when counting UTF-8 characters
                # https://en.wikipedia.org/wiki/UTF-8
                # https://stackoverflow.com/a/3586973
                char_count += 1
            if c == ord('\n'):
                line_count += 1
    return (line_count, char_count, byte_count)


def count_lines_chars_and_bytes_b(stream: BinaryIO, buf_size: int = 8192) -> Tuple[int, int, int]:
    line_count = 0
    char_count = 0
    byte_count = 0
    while bytes_read := stream.read(buf_size):
        line_count += bytes_read.count(b'\n')
        byte_count += len(bytes_read)
        for c in bytes_read:
            if c & 0xC0 != 0x80:
                # UTF-8 multibytes start with 10xxxxxx,
                # ignore these when counting UTF-8 characters
                # https://en.wikipedia.org/wiki/UTF-8
                # https://stackoverflow.com/a/3586973
                char_count += 1
    return (line_count, char_count, byte_count)


def count_lines_chars_and_bytes_c(stream: BinaryIO) -> Tuple[int, int, int]:
    line_count = 0
    char_count = 0
    byte_count = 0
    while bytes_read := stream.readline():
        line_count += 1
        byte_count += len(bytes_read)
        for c in bytes_read:
            if c & 0xC0 != 0x80:
                # UTF-8 multibytes start with 10xxxxxx,
                # ignore these when counting UTF-8 characters
                # https://en.wikipedia.org/wiki/UTF-8
                # https://stackoverflow.com/a/3586973
                char_count += 1
    return (line_count, char_count, byte_count)


def count_words_stream(stream: TextIO) -> int:
    word_count = 0
    for l in stream.readlines():
        word_count += len(l.split())
    return word_count


def count_bytes_stream(stream: BinaryIO) -> int:
    bytes_count = 0
    for l in stream.readlines():
        bytes_count += len(l)
    return bytes_count


def count_bytes_stream_buffered(stream: BinaryIO, buf_size: int = 8192) -> int:
    bytes_count = 0
    while bytes_read := stream.read(buf_size):
        bytes_count += len(bytes_read)
    return bytes_count
