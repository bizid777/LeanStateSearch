#!/usr/bin/env python3
"""Idempotent helper that fetches the LeanStateSearch pretrained model.

Run this once before starting the backend.  If `--target-dir` already exists,
no download happens.  Requires `git` and `git-lfs` to be on PATH.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

MODEL_REPO_URL = "https://huggingface.co/ruc-ai4math/LeanStateSearch2025.3"


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Lean State Search model via git-lfs"
    )
    parser.add_argument(
        "--target-dir",
        default="LeanStateSearch2025.3",
        help="Destination directory for the model",
    )
    args = parser.parse_args()

    target = Path(args.target_dir)
    if target.exists():
        print(f"Model directory '{target}' already exists – skipping download.")
        sys.exit(0)

    # Ensure git-lfs installed locally
    try:
        subprocess.check_output(["git", "lfs", "install", "--version"])
    except subprocess.CalledProcessError:
        print("git-lfs not found. Please install git-lfs first.", file=sys.stderr)
        sys.exit(1)

    run(["git", "lfs", "install"])
    run(["git", "clone", MODEL_REPO_URL, str(target)])
    print("Model downloaded to", target.resolve())


if __name__ == "__main__":
    main()
