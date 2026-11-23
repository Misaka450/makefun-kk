"""make.fun entry: Sum up 23 November's world news in one image.

Standard library only. Copies the entry image shipped beside this
file to the output directory, byte for byte, so both grader runs
produce identical output.

Output directory: $MAKEFUN_OUTPUT_DIR, or /output by default
(the kit's starter uses the same convention).
"""
import os
import shutil
from pathlib import Path

ENTRY = "entry.png"


def main():
    src = Path(__file__).resolve().parent / ENTRY
    # Guard against a truncated image: a PNG must start with its
    # 8-byte signature. The copy itself is byte-for-byte, so the
    # two grader runs still produce identical output.
    if src.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a valid PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / ENTRY)


if __name__ == "__main__":
    main()
