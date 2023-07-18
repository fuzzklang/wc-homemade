# wc in python

Python implementation of the unix command line tool `wc`

Inspired by [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-wc/)

The branch `wc-python-with-timings` contains several implementations of the functions with tests and timings.


## Dependencies
- Python 3 (tested on 3.10)
- pytest for running tests

## Usage
`python3 wc.py [-h] [-c] [-l] [-w] [-m] [FILE]`

```txt
positional arguments:
  FILE         Input file, - or empty for stdin

options:
  -h, --help   show this help message and exit
  -c, --bytes  count number of bytes
  -l, --lines  count number of lines
  -w, --words  count number of words
  -m, --chars  count number of characters
```

## Tests and timings
`pytest`

`python3 timings.py`

The tests and timings uses the input file `test.txt` (The Project Gutenberg eBook of The Art of War, by Sun Tzŭ)
