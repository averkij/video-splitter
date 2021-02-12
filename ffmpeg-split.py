#!/usr/bin/env python

# 1. download ffmpeg
# https://github.com/BtbN/FFmpeg-Builds/releases
# https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-02-11-12-32/ffmpeg-N-101061-gba2cebb49c-win64-gpl-vulkan.zip
 
# 2. add folder with ffmpeg to PATH

# 3. prepare manifest with srt2csv.py

# 4. usage
# python .\ffmpeg-split.py -f video/yarkost.avi -m video/manifest.csv -v libx264

# 5. ffmpeg docs
# https://ffmpeg.org/ffmpeg.html
 
# 6. make hardsubed video
# https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo

import csv
import subprocess
import math
import json
import os
import shlex
import pathlib
from optparse import OptionParser
from datetime import datetime, timedelta

#timestamp format is "05:20:25,620" => "%H:%M:%S,%f"
def parse_subtitles_timestamp(ts):
    if not ts:
        return None
    return ts.replace(',','.')

def split_by_manifest(filename, manifest, vcodec="copy", acodec="copy",
                      extra="", **kwargs):
    """ Split video into segments based on the given manifest file.

    Arguments:
        filename (str)      - Location of the video.
        manifest (str)      - Location of the manifest file.
        vcodec (str)        - Controls the video codec for the ffmpeg video
                            output.
        acodec (str)        - Controls the audio codec for the ffmpeg video
                            output.
        extra (str)         - Extra options for ffmpeg.
    """
    if not os.path.exists(manifest):
        print("File does not exist: %s" % manifest)
        raise SystemExit

    with open(manifest) as manifest_file:
        manifest_type = manifest.split(".")[-1]
        if manifest_type == "json":
            config = json.load(manifest_file)
        elif manifest_type == "csv":
            config = csv.DictReader(manifest_file, delimiter='\t')
        else:
            print("Format not supported. File must be a csv or json file")
            raise SystemExit

        pathlib.Path(os.path.join("output","videos")).mkdir(parents=True, exist_ok=True)
        # pathlib.Path(os.path.join("output","texts").mkdir(parents=True, exist_ok=True)

        split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec,
                     "-acodec", acodec, "-y"] + shlex.split(extra)
        try:
            fileext = filename.split(".")[-1]
        except IndexError as e:
            raise IndexError("No . in filename. Error: " + str(e))
        for video_config in config:
            split_str = ""
            split_args = []
            try:
                split_start = parse_subtitles_timestamp(video_config["start_time"])
                split_length = parse_subtitles_timestamp(video_config.get("end_time", None))
                if not split_length:
                    split_length = video_config["length"]
                filebase = os.path.join("output", "videos", video_config["rename_to"])
                if fileext in filebase:
                    filebase = ".".join(filebase.split(".")[:-1])

                split_args += ["-ss", str(split_start), "-to", str(split_length)]
                split_args += [filebase + "." + fileext]
                
                print("########################################################")
                print("About to run: "+" ".join(split_cmd+split_args))
                print("########################################################")
                subprocess.check_output(split_cmd+split_args)
            except KeyError as e:
                print("############# Incorrect format ##############")
                if manifest_type == "json":
                    print("The format of each json array should be:")
                    print("{start_time: <int>, length: <int>, rename_to: <string>}")
                elif manifest_type == "csv":
                    print("start_time,end_time,rename_to should be the first line ")
                    print("in the csv file.")
                print("#############################################")
                print(e)
                raise SystemExit

def main():
    parser = OptionParser()

    parser.add_option("-f", "--file",
                        dest = "filename",
                        help = "File to split, for example sample.avi",
                        type = "string",
                        action = "store"
                        )
    parser.add_option("-m", "--manifest",
                      dest = "manifest",
                      help = "Split video based on a json manifest file. ",
                      type = "string",
                      action = "store"
                     )
    parser.add_option("-v", "--vcodec",
                      dest = "vcodec",
                      help = "Video codec to use. ",
                      type = "string",
                      default = "copy",
                      action = "store"
                     )
    parser.add_option("-a", "--acodec",
                      dest = "acodec",
                      help = "Audio codec to use. ",
                      type = "string",
                      default = "copy",
                      action = "store"
                     )
    parser.add_option("-e", "--extra",
                      dest = "extra",
                      help = "Extra options for ffmpeg, e.g. '-e -threads 8'. ",
                      type = "string",
                      default = "",
                      action = "store"
                     )
    (options, args) = parser.parse_args()

    def bailout():
        parser.print_help()
        raise SystemExit

    if not options.filename:
        bailout()

    if options.manifest:
        split_by_manifest(**(options.__dict__))
    else:
        print("Please, provide the manifest *.csv file with timings to split")

if __name__ == '__main__':
    main()
