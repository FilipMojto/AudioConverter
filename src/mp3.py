from argparse import ArgumentParser
import glob
from pathlib import Path

from moviepy import VideoFileClip

from .config import AUDIOCON_DIR


INPUT_DIR = Path(AUDIOCON_DIR) / "audiocon_input"
OUTPUT_DIR = Path(AUDIOCON_DIR) / "audiocon_output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

parser = ArgumentParser()

parser.add_argument("-i", "--input", required=True, help="Input mp4 file path or regex pattern")
parser.add_argument("-r", "--regex", required=False, default=False, action="store_true", help="Use regex to match input file path")
# parser.add_argument("-o", "--output", required=False, default=None, help="Output mp3 file path")

args = parser.parse_args()

input_file_path = Path(INPUT_DIR / args.input)
# output_file_path = Path(OUTPUT_DIR / args.output if args.output else args.input) + Path(".mp3")

input_files = [input_file_path]  # Default to the provided input pattern

if args.regex:
    # input_files = glob.glob(str(INPUT_DIR / f"{input_file_path}.mp4"))
    input_files = glob.glob(input_file_path.as_posix())
    if not input_files:
        print(f"No files matched the regex pattern: {input_file_path}")
        raise SystemExit(1)
    
    input_files = [Path(f) for f in input_files]  # Convert to Path objects

    print(f"Input files: {input_files}")
    input("Press Enter to continue with the matched files or Ctrl+C to cancel...")

for input_file_path in input_files:
    # input_path = Path(input_file_path)
    output_path = Path(OUTPUT_DIR / (Path(input_file_path).stem + ".mp3"))
    

    # output_path.parent.mkdir(parents=True, exist_ok=True)

    # how to turn off verbose output from moviepy? I don't want to see the progress bar or any other output, just the final result.
    video = VideoFileClip(str(input_file_path))
    print(f"Converting {input_file_path.stem} to {output_path.stem}...")
    video.audio.write_audiofile(str(output_path), logger=None)
    print("Done. Final size: {:.2f} MB".format(output_path.stat().st_size / (1024 * 1024)))
