import timeit

from typing import (
    Any
)

from wc import (
    count_bytes_file,
    count_lines_file,
    count_words_file,
    count_characters_file,
    count_bytes_stream,
    count_bytes_stream_buffered,
    count_lines_stream_buffered,
    count_words_stream,
    count_words_binary_stream,
    count_lines_chars_and_bytes,
    count_lines_chars_and_bytes_b,
    count_lines_chars_and_bytes_c,
    count_all,
)

TESTFILE = "./test.txt"
NUMBER_OF_EXC = 20


def run_timings() -> None:
    def context_wrapper(fun: Any, mode: str='rb', **kwargs) -> int:
        if buf_size := kwargs.get('buf_size'):
            with open(TESTFILE, mode, buffering=buf_size) as stream:
                return fun(stream, **kwargs)
        else:
            with open(TESTFILE, mode) as stream:
                return fun(stream, **kwargs)

    print("===== TIMINGS =====")
    print(f"  number of executions pr function: {NUMBER_OF_EXC}")
    # args: <filepath>
    file_functions = [
        count_bytes_file,
        count_lines_file,
        count_words_file,
        count_characters_file,
    ]

    print("--- Timing file reading functions ---")

    print_stat_header()
    for file_func in file_functions:
        timing = timeit.timeit(lambda: file_func(TESTFILE), number=NUMBER_OF_EXC)
        per_call = timing / NUMBER_OF_EXC * 1000 * 1000
        print_stats(file_func.__name__, timing, per_call)


    print("\n--- Timing binary stream reading functions ---")

    binary_stream_funcs = [
        count_bytes_stream,
        count_lines_chars_and_bytes_c,
        count_all,
    ]

    print_stat_header()
    for bin_func in binary_stream_funcs:
        timing = timeit.timeit(lambda: context_wrapper(bin_func, mode='rb'), number=NUMBER_OF_EXC)
        per_call = timing / NUMBER_OF_EXC * 1000 * 1000
        print_stats(bin_func.__name__, timing, per_call)


    # args: <stream>, <buf_size>
    buffered_stream_funcs = [
        count_bytes_stream_buffered,
        count_lines_stream_buffered,
        count_words_binary_stream,
        count_lines_chars_and_bytes,
        count_lines_chars_and_bytes_b,

    ]

    buffer_sizes = [
        4096,
        8192,
        16384
    ]

    for buf_func in buffered_stream_funcs:
        print()
        for buf_size in buffer_sizes:
            timing = timeit.timeit(lambda: context_wrapper(buf_func, mode='rb', buf_size=buf_size), number=NUMBER_OF_EXC)
            per_call = timing / NUMBER_OF_EXC * 1000 * 1000
            print_stats(buf_func.__name__, timing, per_call, buf_size)

    # args: <stream>
    text_stream_funcs = [
        count_words_stream
    ]

    print("\n--- Timing text stream reading functions ---")

    for text_func in text_stream_funcs:
        timing = timeit.timeit(lambda: context_wrapper(text_func, mode='r'), number=NUMBER_OF_EXC)
        per_call = timing / NUMBER_OF_EXC * 1000 * 1000
        print_stats(text_func.__name__, timing, per_call)




PRINT_COLUMNS=[30, 20, 20, 20]

def print_stat_header():
    print(f"{'function': <{PRINT_COLUMNS[0]}}"
          f"{'total time':>{PRINT_COLUMNS[1]}}"
          f"{'per call':>{PRINT_COLUMNS[2]}}"
          f"{'buffer size (opt)':>{PRINT_COLUMNS[3]}}")


def print_stats(func_name, total_time, per_call, buf_size=""):
    func_name = f"{func_name}"
    total_time = f"{total_time:.5f} s"
    per_call = f"{per_call:.5f} μs"
    buf_size=f"{buf_size}"

    output_string = str(
        f"{func_name:<{PRINT_COLUMNS[0]}}"
        f"{total_time:>{PRINT_COLUMNS[1]}}"
        f"{per_call:>{PRINT_COLUMNS[2]}}"
        f"{buf_size:>{PRINT_COLUMNS[3]}}"
    )

    print(output_string)


if __name__ == '__main__':
    run_timings()
