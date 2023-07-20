package timings

import (
	"fmt"
	"log"
	"os"
	"time"

	wc_go "github.com/fuzzklang/wc-homemade/wc-go/wc-go"
)

const test_file string = "./test.txt"

func RunTimings() {
	elapsed := timeCountAll()
	printResult("timeCountAll", elapsed, "")
}

func timeCountAll() (elapsed time.Duration) {
	f := openFile(test_file)
	start := time.Now()
	wc_go.CountAll(f)
	end := time.Now()
	elapsed = end.Sub(start)
	return
}

func openFile(filepath string) *os.File {
	f, err := os.OpenFile(filepath, os.O_RDONLY, os.ModePerm)
	if err != nil {
		log.Fatalf("open file error: %v", err)
	}

	return f
}

func printResult(funcName string, timing time.Duration, info string) {
	fmt.Printf("%s\t %d us\n %s", funcName, timing.Microseconds(), info)
}
