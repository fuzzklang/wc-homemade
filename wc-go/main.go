package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	wc_go "github.com/fuzzklang/wc-homemade/wc-go/wc-go"
	term "golang.org/x/term"
)

var filepath *string
var l *bool
var w *bool
var c *bool
var b *bool

func main() {
	filepath = flag.String("f", "-", "Input file, - or empty for stdin")
	l = flag.Bool("l", false, "count number of lines")
	w = flag.Bool("w", false, "count number of words")
	c = flag.Bool("c", false, "count number of characters")
	b = flag.Bool("b", false, "count number of bytes")
	flag.Parse()

	checkAndSetFlags()

	var f *os.File
	var err error

	if *filepath == "-" {
		f, err = os.OpenFile(os.Stdin.Name(), os.O_RDONLY, os.ModePerm)
	} else {
		f, err = os.OpenFile(*filepath, os.O_RDONLY, os.ModePerm)
		defer f.Close()
	}

	if err != nil {
		log.Fatalf("open file error: %v", err)
	}

	line_count, word_count, char_count, byte_count, _ := wc_go.CountAll(f)

	fmt.Printf(makeResultString(line_count, word_count, char_count, byte_count, *filepath))
}

func checkAndSetFlags() {
	// Default mode when no flags are set
	if !*l && !*w && !*c && !*b {
		*l = true
		*w = true
		*c = true
		*b = false
	}
}

func makeResultString(
	line_count int,
	word_count int,
	char_count int,
	byte_count int,
	filepath string) string {

	var result_string string = ""
	var delimiter string = ""
	if term.IsTerminal(int(os.Stdout.Fd())) {
		delimiter = " "
	} else {
		delimiter = "\n"
	}

	if *l {
		result_string += fmt.Sprintf("%d%s", line_count, delimiter)
	}
	if *w {
		result_string += fmt.Sprintf("%d%s", word_count, delimiter)
	}
	if *c {
		result_string += fmt.Sprintf("%d%s", char_count, delimiter)
	}
	if *b {
		result_string += fmt.Sprintf("%d%s", byte_count, delimiter)
	}
	if filepath != "-" {
		result_string += fmt.Sprintf("%s", filepath)
	}
	return fmt.Sprintf("%s\n", result_string)
}
