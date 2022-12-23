#!/usr/bin/env python3
"""Convert pptx to mp4 using pptx2ari
"""
import datetime
import psutil
import webvtt

from pathlib import Path
# from run_command import run_command

UPLOAD_DIR = '/var/www/html/pptx'
MAIN_DIR = '/var/www/html'


def run_conversion(input_file, output_file):
    """Run pptx2ari.sh to do the actual conversion to video
    """
    return_code = None
    voice = input_file.split('__')[-1].split('.')[-2]

    with open(f"{input_file}.log", 'wb') as logfile:
        proc = psutil.Popen(["/opt/pptx2ari.sh", input_file, output_file,
                             voice], stdout=logfile, stderr=logfile,
                            universal_newlines=True)
        proc.wait()
        # convert srt to vtt
        vtt = webvtt.from_srt(Path(output_file).with_suffix(".srt"))
        vtt.save()


def convert_files(upload_directory, main_dir):
    """Convert presentation to video

    With each move the input file to the main directory, under timestamped
    subdirectory, then convert it with pptx2ari to mp4
    """
    # foreach input_pptx `mv input_pptx /var/www/html/timestamp_dir/`
    for f in upload_directory.iterdir():
        if f.is_file() and f.suffix == '.pptx':
            output_dir = main_dir.joinpath(f.stem)
            output_dir.mkdir(parents=True, exist_ok=True)

            input_file = output_dir.joinpath(f.name)
            f.replace(input_file)
            output_file = output_dir.joinpath(f.stem + ".mp4")

            input_file = input_file.resolve()
            output_file = output_file.resolve()

            print(f"Convert {input_file} to {output_file}")
            run_conversion(str(input_file), str(output_file))


def main():
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    main_dir = Path(MAIN_DIR).joinpath(timestamp)
    if not main_dir.exists():
        main_dir.mkdir()

    convert_files(Path(UPLOAD_DIR), main_dir)


if __name__ == '__main__':
    main()
