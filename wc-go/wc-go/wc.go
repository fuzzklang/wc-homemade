package wc_go

import (
	"bufio"
	"io"
	"strings"
)

func CountAll(r io.Reader) (line_count int, word_count int, char_count int, byte_count int, err error) {
	sc := bufio.NewScanner(r)
	for sc.Scan() {
		line_count += 1
		byte_count += len(sc.Bytes()) + 1 // + 1 for removed newline
		char_count += len(sc.Text()) + 1
		word_count += len(strings.Fields(sc.Text()))

		_ = sc.Text()
	}
	err = nil
	return
}
