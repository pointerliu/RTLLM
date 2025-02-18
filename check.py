import os
from pathlib import Path
import shutil
import subprocess

if __name__ == '__main__':
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

        dut: Path = directory / f'{prob_name}.v'
        shutil.copy(directory / f'verified_{prob_name}.v', dut)

        ctx = dut.read_text().replace(f'verified_{prob_name}', f'{prob_name}')
        dut.write_text(ctx)

        ret = subprocess.run(f"make iverilog TEST_DESIGN={prob_name}", shell=True, cwd=directory)
        if ret.returncode != 0:
            print(f"[ERROR] exec iverilog compile at prob {directory} error")
            continue

        ret = subprocess.run(f"make sim", shell=True, cwd=directory)
        if ret.returncode != 0:
            print(f"[ERROR] exec iverilog sim at prob {directory} error")
            continue

        log: Path = directory / "run.log"
        if not log.exists() or "Your Design Passed" not in log.read_text():
            print(f"[ERROR] test failed at prob {directory} error")
