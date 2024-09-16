import os
import sys
import subprocess
from pathlib import Path

def find_files(directory):
    mp3_files = {}
    cdg_files = {}

    # Traverse through the directory and all subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file  # Convert file to a Path object
            # Identify MP3 and CDG files
            if file_path.suffix == ".mp3":
                mp3_files[file_path.stem] = file_path
            elif file_path.suffix == ".cdg":
                cdg_files[file_path.stem] = file_path

    return mp3_files, cdg_files

def process_files(mp3_files, cdg_files, input_directory, output_directory):
    for stem, mp3_path in mp3_files.items():
        if stem in cdg_files:
            cdg_path = cdg_files[stem]

            # Calculate relative path from the input directory
            relative_path = mp3_path.parent.relative_to(input_directory)

            # Prepare output directory and file path in the specified output directory
            output_dir = output_directory / relative_path
            output_dir.mkdir(parents=True, exist_ok=True)  # Create directories if necessary
            output_file = output_dir / f"{mp3_path.stem}.mkv"

            # Check if the output .mkv file already exists
            if output_file.exists():
                print(f"Skipping {output_file}, already exists.")
                continue  # Skip this file as it has already been processed

            # Run ffmpeg command to combine mp3 and cdg
            command = [
                "ffmpeg",
                "-i", str(mp3_path),
                "-i", str(cdg_path),
                "-pix_fmt", "yuv420p",
                "-vcodec", "libx264",
                "-acodec", "copy",
                str(output_file)
            ]

            print(f"Processing {mp3_path} and {cdg_path} -> {output_file}")
            subprocess.run(command)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = Path(sys.argv[1])
    output_directory = Path(sys.argv[2])

    if not input_directory.is_dir():
        print(f"Error: {input_directory} is not a valid directory")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_directory.mkdir(parents=True, exist_ok=True)

    # Find matching mp3 and cdg files across all subdirectories
    mp3_files, cdg_files = find_files(input_directory)

    # Process and convert matched mp3 and cdg files
    process_files(mp3_files, cdg_files, input_directory, output_directory)

if __name__ == "__main__":
    main()
