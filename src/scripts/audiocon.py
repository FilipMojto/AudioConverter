from argparse import ArgumentParser
import glob
from pathlib import Path
import subprocess

from imageio_ffmpeg import get_ffmpeg_exe
from moviepy import VideoFileClip

from ..config import AUDIOCON_DIR


INPUT_DIR = Path(AUDIOCON_DIR) / "audiocon_input"
OUTPUT_DIR = Path(AUDIOCON_DIR) / "audiocon_output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def convert_durationless_file(input_path: Path, output_path: Path) -> None:
    """Extract audio with FFmpeg when MoviePy cannot determine the duration."""
    command = [
        get_ffmpeg_exe(),
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-c:a",
        "libmp3lame",
        "-q:a",
        "2",
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"FFmpeg could not convert {input_path}") from exc



def main() -> None:
    parser = ArgumentParser(description="Convert video files to MP3")
    parser.add_argument("-i", "--input", required=True, help="Input file path or glob pattern")
    parser.add_argument("-r", "--regex", action="store_true", help="Treat the input as a glob pattern")

    args = parser.parse_args()

    input_file_path = Path(INPUT_DIR / args.input)
    input_files = [input_file_path] if not args.regex else [Path(path) for path in glob.glob(input_file_path.as_posix())]

    if args.regex:
        # input_files = [Path(path) for path in glob.glob(input_file_path.as_posix())]
        if not input_files:
            parser.error(f"no files matched the pattern: {input_file_path}")

        print(f"Input files: {input_files}")
        input("Press Enter to continue with the matched files or Ctrl+C to cancel...")

    for input_path in input_files:
        if not input_path.exists():
            parser.error(f"input file does not exist: {input_path}")

        output_path = OUTPUT_DIR / f"{input_path.stem}.mp3"

        print(f"Converting {input_path.stem} to {output_path.stem}...")
        try:
            with VideoFileClip(str(input_path)) as video:
                if video.audio is None:
                    parser.error(f"input file has no audio track: {input_path}")
                video.audio.write_audiofile(str(output_path), logger=None)
        except OSError as exc:
            if "Duration: N/A" not in str(exc):
                raise
            print("Duration is unavailable; falling back to direct FFmpeg conversion...")
            convert_durationless_file(input_path, output_path)
        print(f"Done. Final size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    main()
