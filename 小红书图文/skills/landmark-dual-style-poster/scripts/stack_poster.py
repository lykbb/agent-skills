#!/usr/bin/env python3
"""Stack two equally sized landscape images into one portrait PNG."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


def read_size(path):
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    streams = json.loads(probe.stdout)["streams"]
    if not streams:
        raise ValueError(f"No image stream found in {path}")
    return streams[0]["width"], streams[0]["height"]


def stack_poster(photo, illustration, output):
    if output.suffix.lower() != ".png":
        raise ValueError("Choose a .png output path.")
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")

    width, height = read_size(photo)
    if read_size(illustration) != (width, height) or 2 * width != 3 * height:
        raise ValueError("Supply two images of the same size with a 3:2 aspect ratio.")

    result = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-noautorotate", "-i", str(photo),
            "-noautorotate", "-i", str(illustration),
            "-filter_complex", "[0:v]format=rgb24[top];[1:v]format=rgb24[bottom];"
            "[top][bottom]vstack=inputs=2",
            "-frames:v", "1", "-c:v", "png", "-f", "image2pipe", "pipe:1",
        ],
        check=True,
        capture_output=True,
    )
    if not result.stdout:
        raise ValueError("FFmpeg did not produce an image.")
    with output.open("xb") as image_file:
        image_file.write(result.stdout)
    return width, 2 * height


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", type=Path, help="Top image")
    parser.add_argument("illustration", type=Path, help="Bottom image")
    parser.add_argument("output", type=Path, help="Path to a new PNG")
    args = parser.parse_args()
    try:
        width, height = stack_poster(args.photo, args.illustration, args.output)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
        print(detail.strip() if detail else str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"{args.output} ({width} × {height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
