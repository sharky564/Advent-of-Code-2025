import sys
import os
import subprocess

TEMPLATE = """from utils import run_solver

def process_data(d: list[str]):
    return d

@run_solver("Part 1", submit_result=False)
def part1(d: list[str]) -> int:
    data = process_data(d)
    return None

@run_solver("Part 2", submit_result=False)
def part2(d: list[str]) -> int:
    data = process_data(d)
    return None

if __name__ == '__main__':
    part1()
    part2()
"""

def create_stub():
    if len(sys.argv) > 1:
        day_input = sys.argv[1]
    else:
        day_input = input("Enter question number: ")

    try:
        day_num = int(day_input)
        day_str = f"{day_num:02d}"
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    filename = f"q{day_str}.py"

    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists!")
        return

    try:
        with open(filename, "w") as f:
            f.write(TEMPLATE)
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error writing file: {e}")
        return

    try:
        subprocess.run(["code", filename], shell=True)
    except Exception:
        print("File created, but could not open VS Code automatically.")

if __name__ == "__main__":
    create_stub()