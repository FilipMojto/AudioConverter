# This script provides additional mp3 utilities like getting or updating mp3 metadata, and converting video files to mp3.

from argparse import ArgumentParser
import glob
from pathlib import Path

from mutagen.mp3 import MP3

from src.config import AUDIOCON_DIR

INPUT_DIR = Path(AUDIOCON_DIR) / "mp3_input"
INPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_mp3_metadata(file_path: Path) -> dict:
    audio = MP3(file_path)
    return {
        "title": audio.get("TIT2", None),
        "artist": audio.get("TPE1", None),
        "album": audio.get("TALB", None),
        "year": audio.get("TDRC", None),
        "genre": audio.get("TCON", None),
        "duration (min)": audio.info.length / 60,
    }


def main() -> None:
    parser = ArgumentParser(description="MP3 Utilities")
    parser.add_argument("-i", "--input", required=True, help="Input file path or glob pattern")
    parser.add_argument("-a", "--action", required=False, choices=["info", "update"], default="info", help="Action to perform: convert, get_metadata, or update_metadata")
    parser.add_argument("-r", "--regex", action="store_true", help="Treat the input as a glob pattern")

    args = parser.parse_args()
    action = args.action

    input_file_path = Path(INPUT_DIR / args.input) if not args.regex else Path(glob.glob(str(INPUT_DIR / args.input))[0])

    if not input_file_path.exists():
        parser.error(f"input file does not exist: {input_file_path}")

    if action == "info":
        metadata = get_mp3_metadata(input_file_path)
        print(f"Metadata for {input_file_path}:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    elif action == "update":
        # Placeholder for update metadata functionality
        print("Update metadata functionality is not implemented yet.")
    else:
        parser.error(f"Unknown action: {action}")



if __name__ == "__main__":
    main()