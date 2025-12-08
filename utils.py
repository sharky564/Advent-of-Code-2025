import time
import functools
import re
import gc
import statistics
from pathlib import Path
from collections.abc import Callable
import pyperclip
from aocd import get_data, submit
import cProfile
import pstats
import io

_CACHE_REGISTRY = []
DEBUG = True

def dprint(*args, **kwargs):
    if DEBUG:
        print("\033[90m[DEBUG]\033[0m", *args, **kwargs)

class RunnerConfig:
    """Global configuration for the runner."""
    ENABLE_LOGGING = True
    COPY_TO_CLIPBOARD = False
    BENCHMARK_MIN_TIME = 1.0
    BENCHMARK_MIN_ITERS = 5
    BENCHMARK_WARMUP = 5

def _extract_number(s: str) -> int | None:
    match = re.search(r'\d+', s)
    return int(match.group()) if match else None

def cache_by_id(func: Callable):
    """
    Decorator that caches the result based on the unique ID of the first argument.
    Automatically registers itself to be cleared during benchmarks.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            return func(*args, **kwargs)
        
        input_id = id(args[0])
        
        if input_id in cache:
            print("Found in cache")
            return cache[input_id]
        
        result = func(*args, **kwargs)
        cache[input_id] = result
        return result
        
    def clear_cache():
        cache.clear()
    
    _CACHE_REGISTRY.append(clear_cache)
    
    wrapper.cache_clear = clear_cache
    return wrapper

def format_time(seconds: float) -> str:
    """Helper to format time in ns, us, ms, or s."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f}ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f}µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f}ms"
    else:
        return f"{seconds:.2f}s"

def run_solver(
    part_name: str, 
    submit_result: bool = False, 
    tests: list[tuple[str, int]] = None, 
    benchmark: bool = True, 
    profile: bool = False, 
    enable_print: bool = True, 
    strip_lines: bool = True, 
    raw_input: bool = False
):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if tests:
                print("\033[90mRunning Tests...\033[0m")
                all_passed = True
                for i, (test_input, expected) in enumerate(tests):
                    if raw_input:
                        t_data = test_input
                        if strip_lines:
                            t_data = t_data.strip()
                    elif strip_lines:
                        t_data = [line.strip() for line in test_input.strip().split('\n')]
                    else:
                        t_data = test_input.split('\n')

                    for clear_func in _CACHE_REGISTRY:
                        clear_func()
                    
                    t_start = time.perf_counter()
                    t_result = func(t_data, *args, **kwargs)
                    t_end = time.perf_counter()
                    
                    if t_result == expected:
                        print(f"  \033[32m✔ Test {i+1} passed\033[0m ({format_time(t_end-t_start)})")
                    else:
                        print(f"  \033[31m✘ Test {i+1} failed\033[0m")
                        print(f"    Expected: {expected}")
                        print(f"    Got:      {t_result}")
                        all_passed = False
                
                if not all_passed:
                    print("\033[91mTests failed. Aborting real run.\033[0m")
                    return None
            
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
                    input_file.parent.mkdir(parents=True, exist_ok=True)
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

            for clear_func in _CACHE_REGISTRY:
                clear_func()

            exec_start = time.perf_counter()
            result = func(data, *args, **kwargs)
            exec_end = time.perf_counter()
            
            parse_ms = (parse_end - parse_start) * 1000
            exec_time = exec_end - exec_start

            if enable_print and RunnerConfig.ENABLE_LOGGING:
                timing_str = f"\033[90m[Parse: {parse_ms:.2f}ms]\033[0m \033[33m[Run: {format_time(exec_time)}]\033[0m"
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

            if benchmark and result is not None:
                print(f"\033[90mRunning benchmark (min {RunnerConfig.BENCHMARK_MIN_TIME}s)...\033[0m")
                
                for _ in range(RunnerConfig.BENCHMARK_WARMUP):
                    for clear_func in _CACHE_REGISTRY:
                        clear_func()
                    func(data, *args, **kwargs)
                
                timings = []
                start_global = time.perf_counter()
                iter_count = 0
                
                while True:
                    for clear_func in _CACHE_REGISTRY:
                        clear_func()

                    gc_old = gc.isenabled()
                    gc.disable()
                    
                    t0 = time.perf_counter()
                    func(data, *args, **kwargs)
                    t1 = time.perf_counter()
                    
                    if gc_old:
                        gc.enable()
                    
                    timings.append(t1 - t0)
                    iter_count += 1
                    
                    if iter_count >= RunnerConfig.BENCHMARK_MIN_ITERS:
                        if (time.perf_counter() - start_global) > RunnerConfig.BENCHMARK_MIN_TIME:
                            break
                
                avg = statistics.mean(timings)
                median = statistics.median(timings)
                worst = max(timings)
                best = min(timings)
                stdev = statistics.stdev(timings) if len(timings) > 1 else 0

                print(f"  \033[90mStats ({iter_count} runs):\033[0m")
                print(f"  \033[94mMean: {format_time(avg)} ± {format_time(stdev)}\033[0m")
                print(f"  \033[90mMin: {format_time(best)} | Median: {format_time(median)} | Max: {format_time(worst)}\033[0m")

            if profile:
                for clear_func in _CACHE_REGISTRY:
                    clear_func()
                pr = cProfile.Profile()
                pr.enable()
                func(data, *args, **kwargs)
                pr.disable()
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                ps.print_stats(20)
                print(f"\033[90m{s.getvalue()}\033[0m")

            if not submitted and RunnerConfig.COPY_TO_CLIPBOARD and result is not None:
                pyperclip.copy(str(result))
                if enable_print:
                    print("\033[90m(Copied answer to clipboard)\033[0m")
            
            return result
        return wrapper
    return decorator