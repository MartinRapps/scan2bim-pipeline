#!/usr/bin/env python3
"""Create one deterministic evaluation-frame list for all model stages."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stride", type=int, default=8)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    if args.stride <= 0 or args.offset < 0:
        parser.error("--stride must be positive and --offset must be non-negative")

    images = sorted(
        path.name
        for path in args.images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    if not images:
        raise FileNotFoundError(f"No images found in {args.images_dir}")
    selected = [name for index, name in enumerate(images) if index % args.stride == args.offset]
    if not selected:
        raise ValueError("The evaluation split is empty")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(selected) + "\n", encoding="utf-8")
    print(f"Evaluation split: {len(selected)} of {len(images)} images -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
