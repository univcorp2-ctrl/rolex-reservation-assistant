from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
    [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
    ["ruff", "check", "."],
    ["pytest"],
    [
        sys.executable,
        "-m",
        "rolex_reservation_assistant",
        "rehearse",
        "--profile",
        "config/applicant.example.json",
        "--location",
        "all",
        "--selectors",
        "config/selectors.mock.json",
        "--iterations",
        "100",
    ],
]


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    for command in COMMANDS:
        run(command)
    print("CI runner completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
