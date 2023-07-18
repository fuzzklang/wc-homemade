import timeit

from typing import Any

from wc import count_all


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

    print("\n--- Timing binary stream reading functions ---")

    print_stat_header()
    timing = timeit.timeit(lambda: context_wrapper(count_all, mode='rb'), number=NUMBER_OF_EXC)
    per_call = timing / NUMBER_OF_EXC * 1000 * 1000
    print_stats(count_all.__name__, timing, per_call)



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
