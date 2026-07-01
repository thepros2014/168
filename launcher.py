"""Launcher menu to choose between project variants.

Options:
- 1: CLI-only
- 2: Gamepad (real or simulated)
- 3: Gamepad Tool (real or simulated)
- 4: Run tests
- q: Quit
"""
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

TOOLS = [
    ("CLI-only", ROOT / 'CLI-only' / 'main.py'),
    ("Gamepad", ROOT / 'gamepad' / 'main.py'),
    ("Gamepad Tool", ROOT / 'gamepad_tool' / 'main.py'),
]


def run_script(path, args=None):
    cmd = [sys.executable, str(path)] + (args or [])
    return subprocess.call(cmd)


def menu():
    while True:
        print('\nSelect an option:')
        for i, (name, _) in enumerate(TOOLS, start=1):
            print(f'  {i}: {name}')
        print('  4: Run tests')
        print('  q: Quit')
        choice = input('Choice: ').strip()
        if choice.lower() == 'q':
            return
        if choice == '1':
            run_script(TOOLS[0][1], ['seed'])
        elif choice == '2':
            sim_in = input('Simulate? (y=simulate, enter=auto): ').strip().lower()
            args = ['gamepad']
            if sim_in == 'y':
                args.append('--simulate')
            run_script(TOOLS[1][1], args)
        elif choice == '3':
            sim_in = input('Simulate? (y=simulate, enter=auto): ').strip().lower()
            args = ['gamepad']
            if sim_in == 'y':
                args.append('--simulate')
            run_script(TOOLS[2][1], args)
        elif choice == '4':
            run_script(ROOT / 'scripts' / 'smoke_test.py')
        else:
            print('Unknown choice')


if __name__ == '__main__':
    menu()
