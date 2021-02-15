import os
import re

from optparse import OptionParser

import srt

#https://github.com/cdown/srt

#usage
#python .\srt2csv.py -i video2\sub_pin.srt -o krad.csv

def process_file(input, output, **kwargs):
    if not input or not output:
        print("Provide input and output file names")
        return
    if not os.path.isfile(input):
        print("Input file not exist:", input)
        return
    with open(input, mode="r", encoding="utf-8") as input_file: 
        subs = list(srt.parse("\n".join([x.rstrip() for x in input_file.readlines()])))
        with open(output, mode="w", encoding="utf-8") as output_file: 
            output_file.write(f"start_time\tend_time\trename_to\tcontent\n")
            counter = 0
            for sub in subs:
                content = re.sub(r"\r?\n|r", '', sub.content).replace("\t",'')
                output_file.write(f"{srt.timedelta_to_srt_timestamp(sub.start)}\t{srt.timedelta_to_srt_timestamp(sub.end)}\tvideo{counter}.mpg\t{content}\n")
                counter += 1


def main():
    parser = OptionParser()
    parser.add_option("-i", "--input",
                        dest = "input",
                        help = "Subtitles to process, for example Terminator.srt",
                        type = "string",
                        action = "store"
                        )
    parser.add_option("-o", "--output",
                      dest = "output",
                      help = "Output file with timings, for example manifest.csv",
                      type = "string",
                      action = "store"
                     )
    (options, args) = parser.parse_args()
    process_file(**(options.__dict__))


if __name__ == '__main__':
    main()