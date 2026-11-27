#!/usr/bin/env python3
"""news-image-20261127: print Friday 27 November 2026's front page.

The page is drawn ahead of time by build_image.py (Pillow, deterministic)
and stored as assets/entry.png: an image-led 12-story front page for
Friday 27 November 2026. Nvidia tells Dell and Supermicro to stop
shipping AI servers to Malaysia, Singapore, Thailand and Indonesia under
new US export controls; Kyiv braces for a new Russian mass strike after
ballistic missiles hit the capital and Ukraine downs a drone with a laser
in a world-first; 13 miners are dead and 13 missing in a flooded
unauthorised gold mine in Bogor, West Java; and chip stocks lead a Black
Friday rebound. Eight briefs from around the world and a markets strip
(Friday futures and overseas, labelled as such) complete the page.

This program only places that finished page at /output/entry.png. It reads
nothing else, reaches no network, and writes the same bytes every run.
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets" / "entry.png"
DEST_DIR = Path(os.environ.get("OUTPUT_DIR", "/output"))

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the competition's 1 MiB cap
EXPECTED_SIZE = (1024, 1024)


def check_source(path):
    """Refuse to ship anything but the finished 1024x1024 page under 1 MiB."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        return f"{path} is {len(data)} bytes, over the 1 MiB cap"
    if not data.startswith(PNG_SIGNATURE):
        return f"{path} is not a PNG"
    # IHDR is the first chunk: width and height are big-endian uint32 at 16..24.
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        return f"{path} is {width}x{height}, expected 1024x1024"
    return None


def main():
    if not SOURCE.is_file():
        print(f"missing {SOURCE}")
        return 1
    problem = check_source(SOURCE)
    if problem:
        print(problem)
        return 1
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    target = DEST_DIR / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes, 1024x1024 PNG)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
