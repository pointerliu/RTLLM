import os
from pathlib import Path
import shutil
import subprocess

def clean():
    for directory in Path(".").rglob("*"):
        if not directory.is_dir():
            continue
        if not (directory / "makefile").exists():
            continue
        prob_name = directory.name
        print(f'Checking {prob_name}')
        if not (directory / f"verified_{prob_name}.v").exists():
            print(f'[ERROR] verified_{prob_name} not found, skipping')
            continue

        
        os.remove(directory / f"{prob_name}.v")
        os.remove(directory / "run.log")
        os.remove(directory / "simv")

if __name__ == '__main__':
    clean() 