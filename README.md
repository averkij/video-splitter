# Video Splitter via Subtitles Timestamps

This fork modifies the original scripts in a way of using subtitles for preparing the splitting config first. Using this config it splits the video into chunks.

Under the hood script uses **ffmpeg** so you will need to have that installed. Sound in 5.1 format squashes to the stereo by using the **ffmpeg** commands.


## Spliting video

As an input you should have the video and the **correctly timed** subtitles in *.srt* format. Please, check that before proceeding.

### Prepare the config

`python .\srt2csv.py -i input\Terminator.srt -o terminator_config.csv`

This makes the config file which looks like this:

|start_time|end_time|rename_to|content|
|-|-|-|-|
|...|...|...|...|
|00:05:53,697|	00:05:55,231|	video15.mpg|	You clothes.|
|00:05:55,299|	00:05:56,933|	video16.mpg|	Give them to me.|
|00:05:57,001|	00:05:58,301|	video17.mpg|	Now.|
|...|...|...|...|

You should inspect the config and leave only lines you want to extract from the input video.

### Split by subtitles

Using the config you can split the video now.

`python .\ffmpeg-split.py -f terminator.avi -m terminator_config.csv -v libx264`

This splits `terminator.avi` into chunks using the H.264 encoder. In case of troubles you can omit **-v** parameter to use the original encoder or choose different supported by ffmpeg encoder (see the list in the ffmpeg documentation).

### Output

The resulted video will be placed in the **output/video** folder.

## Installing ffmpeg

See [FFmpeg installation guide](https://www.ffmpeg.org/download.html) for details.

