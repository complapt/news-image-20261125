#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261125.

The image itself is bundled in this repository as entry.png: a single
1024x1024 summary of Wednesday 25 November 2026, drawn by
build_image.py from that day's reported news. This program does no
drawing and uses no network; it checks the bundled file and copies it
to /output/entry.png, so both grading runs write identical bytes.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

LIMIT_BYTES = 1024 * 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Return (width, height) after checking the PNG signature and IHDR."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != MAGIC:
        raise ValueError("entry.png is not a PNG file")
    if len(head) < 33 or head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    return struct.unpack(">II", head[16:24])


def main():
    size = os.path.getsize(SRC)
    if size > LIMIT_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit" % size)
    width, height = png_dimensions(SRC)
    if (width, height) != (1024, 1024):
        raise ValueError(
            "entry.png is %dx%d, expected 1024x1024" % (width, height))
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT_PATH)
    print("wrote %s (%d bytes, %dx%d)" % (OUT_PATH, size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
