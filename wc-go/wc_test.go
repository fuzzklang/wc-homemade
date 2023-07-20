package main

import (
	"bytes"
	"fmt"
	"os"
	"testing"

	wc_go "github.com/fuzzklang/wc-homemade/wc-go/wc-go"
)

// TestCountAll call wc.CountAll checking valid return values
func TestCountAll(t *testing.T) {
	f := openFile("./test.txt")
	defer f.Close()

	// Expected values
	l_exp, w_exp, c_exp, b_exp := 7137, 58159, 334699, 334699

	l, w, c, b, err := wc_go.CountAll(f)

	if err != nil {
		t.Fatalf("CountAll() raised error: %v", err)
	} else if l != l_exp ||
		w != w_exp ||
		c != c_exp ||
		b != b_exp {
		t.Fatalf("Unexpected value: %d %d %d %d, expected %d %d %d %d",
			l, w, c, b,
			l_exp, w_exp, c_exp, b_exp)
	}
}

func BenchmarkOpenFileAndCountAll(b *testing.B) {
	for i := 0; i < b.N; i++ {
		f := openFile("./test.txt")
		wc_go.CountAll(f)
		f.Close()
	}
}

func BenchmarkCountAllReadBytes(b *testing.B) {
	reader, err := readFile("./test.txt")
	if err != nil {
		b.Fatalf("Error when reading test file: %v", err)
	}
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		wc_go.CountAll(reader)
	}
}

func openFile(path string) (f *os.File) {
	f, err := os.OpenFile(path, os.O_RDONLY, os.ModePerm)
	if err != nil {
		fmt.Println(fmt.Errorf("Error when opening test file: %v. %w", path, err))
		os.Exit(1)
	}
	return
}

func readFile(path string) (r *bytes.Reader, err error) {
	data, err := os.ReadFile(path)
	if err != nil {
		fmt.Println(fmt.Errorf("Error when reading test file: %v. %w", path, err))
		return nil, err
	}
	r = bytes.NewReader(data)
	return
}
