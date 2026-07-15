from moviepy import VideoFileClip
from argparse import ArgumentParser
import glob

parser = ArgumentParser()

parser.add_argument("-i", "--input", required=True, help="Input video file path, is relative to the directory where the script is run. Can be a regex pattern if -r is used.")
parser.add_argument("-r", "--regex", required=False, default=False, action="store_true", help="Use regex to match input file path")
parser.add_argument("-o", "--output", required=False, default=None, help="Output mp3 file path")

args = parser.parse_args()

input_file = args.input
output_file = args.output

input_files = [input_file]  # Default to the provided input pattern

if args.regex:
    input_files = glob.glob(input_file + ".mp4")
    if not input_files:
        print(f"No files matched the regex pattern: {input_file}")
        exit(1)
    # input_file = input_files[0]  # Take the first match
    # print(f"Using first matched file: {input_file}")

    if not input_files:
        print(f"No files matched the regex pattern: {input_file}")
        exit(1)
    else:
        print(f"Input files: {input_files}")
        user_input = input("Press Enter to continue with the matched files or Ctrl+C to cancel...")

for input_file in input_files:
    # if output_file is not provided, create it by replacing the input file's extension with .mp3
    output_file = output_file or input_file.rsplit('.', 1)[0] + '.mp3'

    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)