# /usr/bin/env python

import argparse
import os
import sys

from typing import (
    Dict,
    BinaryIO,
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
