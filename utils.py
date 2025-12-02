import time
import functools
from pathlib import Path
from collections.abc import Callable
import pyperclip

class RunnerConfig:
    """Global configuration for the runner."""
    INPUT_FILE = Path.cwd() / 'input.txt'
    ENABLE_LOGGING = True
    COPY_TO_CLIPBOARD = True

def run_solver(part_name: str, enable_print: bool = True, strip_lines: bool = True):
    """
    Decorator to read input, time execution, and handle output.
    
    :param part_name: Label for the output (e.g., "Part 1")
    :param enable_print: If False, suppresses stdout (useful for unit tests)
    :param strip_lines: If True, strips newline characters from input lines automatically
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not RunnerConfig.INPUT_FILE.exists():
                print(f"Error: {RunnerConfig.INPUT_FILE} not found.")
                return

            with open(RunnerConfig.INPUT_FILE, 'r') as f:
                if strip_lines:
                    data = [line.strip() for line in f.readlines()]
                else:
                    data = f.readlines()

            start_time = time.perf_counter()
            result = func(data, *args, **kwargs)
            end_time = time.perf_counter()
            
            elapsed = (end_time - start_time) * 1000

            if enable_print and RunnerConfig.ENABLE_LOGGING:
                time_str = f"[{elapsed:.4f} ms]"
                print(f"\033[1;36m{part_name}:\033[0m \033[1;32m{result}\033[0m \033[33m{time_str}\033[0m")
            
            if RunnerConfig.COPY_TO_CLIPBOARD and result is not None:
                pyperclip.copy(str(result))
                if enable_print:
                    print("\033[90m(Copied to clipboard)\033[0m")
            
            return result
        return wrapper
    return decorator