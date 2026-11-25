#!/usr/bin/env python3
"""Deliver the one-line office joke.

The joke (entry.txt) ships inside this repository. At run time the
grader's container is a bare python:3.13, so this entrypoint does the
one job that matters there: place a verified copy of entry.txt into
$MAKEFUN_OUTPUT_DIR (default /output).

Standard library only, no network, no clock: the same input file
always lands byte-for-byte in the output directory.

The gate allows 1 to 199 UTF-8 characters on a single line, so the
copier validates length and line count before writing.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 199


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def asset_path() -> Path:
    return Path(__file__).resolve().parent / "entry.txt"


def deliver() -> Path:
    line = asset_path().read_text(encoding="utf-8").strip()
    if not line or len(line) > MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(line)))
    if "\n" in line:
        raise ValueError("entry must be a single line")
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    dst = target_dir / "entry.txt"
    dst.write_text(line, encoding="utf-8", newline="")
    if dst.read_text(encoding="utf-8") != line:
        raise ValueError("copied file failed verification: %s" % dst)
    print(line)
    return dst


def main():
    try:
        deliver()
    except Exception as exc:
        print("delivery failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
