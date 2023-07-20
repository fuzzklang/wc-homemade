# wc in go
Go implementation of the unix command line tool `wc`

## Dependencies
- <= Go 1.18 (tested on 1.18)
- golang.org/x/sys
- golang.org/x/term

## Usage
`go run main.go [-h] [-c] [-l] [-w] [-m] [FILE]`

```txt
  -b    count number of bytes
  -c    count number of characters
  -f string
        Input file, - or empty for stdin (default "-")
  -l    count number of lines
  -w    count number of words

```

## Tests and timings
`go test`

`go test -bench .`

The tests and timings uses the input file `test.txt` (The Project Gutenberg eBook of The Art of War, by Sun Tzŭ)
