import time
import functools
import re
from pathlib import Path
from collections.abc import Callable
import pyperclip
from aocd import get_data, submit

class RunnerConfig:
    """Global configuration for the runner."""
    ENABLE_LOGGING = True
    COPY_TO_CLIPBOARD = True

def _extract_number(s: str) -> int | None:
    match = re.search(r'\d+', s)
    return int(match.group()) if match else None

def run_solver(part_name: str, submit_result: bool, enable_print: bool = True, strip_lines: bool = True, raw_input: bool = False):
    """
    Decorator to read input, time execution, and handle output.
    
    :param part_name: Label for the output (e.g., "Part 1")
    :param submit_result: If True, prompts to submit the result via aocd. Falls back to clipboard if 'n'.
    :param enable_print: If False, suppresses stdout
    :param strip_lines: If True, strips newline characters from input lines (ignored if raw_input=True)
    :param raw_input: If True, passes the whole file as a single string instead of a list of lines
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            script_path = Path(func.__code__.co_filename)
            script_dir = script_path.parent
            year = _extract_number(script_dir.name)
            day = _extract_number(script_path.stem)
            if not year and not day:
                print(f"Error: Could not parse Day/Year from path: {script_path}")
            input_file = script_dir / f'input/input{day}.txt'
            if not input_file.exists():
                try:
                    print(f"Downloading input for Day {day}, {year}...")
                    data = get_data(day=day, year=year)
                    with open(input_file, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(data)
                except Exception as e:
                    print(f"Error fetching data with aocd: {e}")
                    return

            parse_start = time.perf_counter()
            
            with open(input_file, 'r') as f:
                if raw_input:
                    data = f.read()
                    if strip_lines:
                        data = data.strip()
                elif strip_lines:
                    data = [line.strip() for line in f.readlines()]
                else:
                    data = f.readlines()
            
            parse_end = time.perf_counter()

            exec_start = time.perf_counter()
            result = func(data, *args, **kwargs)
            exec_end = time.perf_counter()
            
            parse_ms = (parse_end - parse_start) * 1000
            exec_ms = (exec_end - exec_start) * 1000

            if enable_print and RunnerConfig.ENABLE_LOGGING:
                timing_str = f"\033[90m[Parse: {parse_ms:.4f}ms]\033[0m \033[33m[Run: {exec_ms:.4f}ms]\033[0m"
                print(f"\033[1;36m{part_name}:\033[0m \033[1;32m{result}\033[0m {timing_str}")
            
            submitted = False
            
            if submit_result and result is not None:
                part_id = None
                if "1" in part_name:
                    part_id = "a"
                elif "2" in part_name:
                    part_id = "b"
                
                if part_id:
                    user_resp = input(f"\033[33mSubmit answer '{result}' for Day {day} Part {part_id}? [y/n] \033[0m")
                    if user_resp.lower().startswith('y'):
                        print("\033[90mSubmitting...\033[0m")
                        submit(result, part=part_id, day=day, year=year)
                        submitted = True
                else:
                    print(f"\033[91mCannot determine part (a/b) from name '{part_name}', skipping submission.\033[0m")

            if not submitted and RunnerConfig.COPY_TO_CLIPBOARD and result is not None:
                pyperclip.copy(str(result))
                if enable_print:
                    print("\033[90m(Copied to clipboard)\033[0m")
            
            return result
        return wrapper
    return decorator