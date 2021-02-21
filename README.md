# Video Splitter via Subtitles Timestamps

These scripts split the original video into chunks accordnig to subtitles timestamps.

Under the hood script uses **ffmpeg** so you will need to have that installed. Sound in 5.1 format squashes to the stereo by using the **ffmpeg** commands.

![terminator](/img/terminator.jpg)

## Requirements

1. FFmpeg for manipulating with video file.
    - See [FFmpeg installation guide](https://www.ffmpeg.org/download.html) for details.
3. Python 3 for running the scripts.
4. srt library to parse the .srt file with subtitles.
    - Install it with <code>pip install srt</code>.

## Hardsub
You can optionally burn the subtitles into the video with the following ffmpeg command:
- <code>ffmpeg -i cutted.avi -vcodec libx264 -vf subtitles=cutted.srt:force_style='Fontsize=26' -y output.avi</code>

Use the **force_style** attribute to adjust the subtitles appearance. Also see the [Subtitles filter documentation](http://ffmpeg.org/ffmpeg-filters.html#subtitles-1) and this [How to burn subtitles into video](https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo) guide.

## Splitting video

As an input you should have the video and the **correctly synchronized** subtitles in *.srt* format. Please, check that before proceeding.

### Prepare the config

- <code>python .\srt2csv.py -i input\Terminator.srt -o terminator_config.csv</code>

This makes the config file which looks something like this:

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

- <code>python .\ffmpeg-split.py -f terminator.avi -m terminator_config.csv -v libx264</code>

This splits `terminator.avi` into chunks using the H.264 encoder. In case of troubles you can omit **-v** parameter to use the original encoder or choose different supported by ffmpeg encoder (see the list in the ffmpeg documentation).

### Output

The resulted video will be placed in the **output/video** folder.

## Useful ffmpeg commands
- To cut the 10 seconds after the first minute
  - <code>ffmpeg -i input.mkv -vcodec libx264  -ss 00:01:00 _**-t**_ 00:00:10 cutted_10s.mkv</code>
- To cut the video between two timestamps
  - <code>ffmpeg -i input.mkv -vcodec libx264 -ss 00:02:00 _**-to**_ 00:02:30 cutted_30s.mkv</code>
- To rescale the video
  - <code>ffmpeg -i input.avi -vf scale=1200:-1 output.avi</code>


