from __future__ import unicode_literals

import glob
import subprocess
import time
from typing import List
import os

os.environ["IMAGEIO_FFMPEG_EXE"] = '/opt/homebrew/bin/ffmpeg'

from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


def deco(func):
    def wrapper(*args, **kwargs):
        print("#### in {}:".format(func.__name__))
        print("# -> args: {}, kwargs: {}".format(args, kwargs))

        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        if isinstance(res, (str, int, dict)):
            print("# -> return: {}".format(res))
        end_time = time.perf_counter()
        print("#### time: {}".format(end_time - start_time))
        return res

    return wrapper


@deco
def cmd_save_stream(**kwargs) -> str:
    return '/opt/homebrew/bin/ffmpeg -y -i {} -map {} {} -y'.format(
        kwargs['in_file'],
        kwargs['fmt'],
        kwargs['out_file']
    )


@deco
def cmd_silence_detect(**kwargs) -> str:
    return '{} | {} | {} | {}'.format(
        '/opt/homebrew/bin/ffmpeg -y -hide_banner -vn -i {} -af "silencedetect=n={}dB:d={}" -f null - 2>&1'.format(
            kwargs['in_file'],
            kwargs['db'],
            kwargs['duration']),
        'grep "silence_end"',
        'awk \'{print $5 " " $8}\'',
        'tee {}'.format(
            kwargs['out_file']))


@deco
def cmd_amix(**kwargs) -> str:
    """
    https://nico-lab.net/amix_with_ffmpeg/
    """
    return '/opt/homebrew/bin/ffmpeg -y -i {} -i {} -filter_complex amix=inputs=2:duration=first:dropout_transition=2 {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['out_file']
    )


@deco
def cmd_amix_video(**kwargs) -> str:
    """
    https://stackoverflow.com/questions/44712868/ffmpeg-set-volume-in-amix
    """
    return '/opt/homebrew/bin/ffmpeg -y -i amovie=audio_to_add.mp4:loop=0,asetpts=N/SR/TB,volume=1.0[a] -i {} -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest[out]" ' \
           '-map 0:v -map [out] {}'. \
        format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['out_file']
    )


@deco
def cmd_merge(**kwargs) -> str:
    """
    https://stackoverflow.com/questions/44712868/ffmpeg-set-volume-in-amix
    """
    return '/opt/homebrew/bin/ffmpeg -y -i {} -i {} {} copy {} aac -map 0:v:0 -map 1:a:0 {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['out_file'],
        kwargs['fmt1'],
        kwargs['fmt2'],
    )


@deco
def cmd_merge_movie(**kwargs) -> str:
    return '/opt/homebrew/bin/ffmpeg -y -i {} -i {} {} copy {} copy {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['fmt1'],
        kwargs['fmt2'],
        kwargs['out_file']
    )


@deco
def cmd_to_playable(**kwargs) -> str:
    return '/opt/homebrew/bin/ffmpeg -y -i {} -pix_fmt yuv420p {}'.format(
        kwargs['in_file'],
        kwargs['out_file'],
    )


@deco
def video_edit(**kwargs) -> None:
    minimum_duration = 1.0

    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    in_handle = open(kwargs['silence_file'].replace('\\', ''), "r", errors='replace')
    video = VideoFileClip(kwargs['file_in'].replace('\\', ''))
    full_duration = video.duration
    clips = []
    while True:
        line = in_handle.readline()

        if not line:
            break

        end, duration = line.strip().split()

        # padding, end地点から1秒残したい
        end = float(end) - float(kwargs["padding"])

        # end地点からずれたpadding + start地点にもpaddingを残すため2回分減る
        duration = float(duration) - float(2 * kwargs["padding"])

        to = float(end) - float(duration)

        start = float(last)
        clip_duration = float(to) - start
        # Clips less than one seconds don't seem to work
        print("Clip Duration: {} seconds".format(clip_duration))

        if clip_duration < minimum_duration:
            continue

        if full_duration - to < minimum_duration:
            continue

        if start > kwargs['ease']:
            start -= kwargs['ease']

        print("Clip {} (Start: {}, End: {})".format(count, start, to))
        clip = video.subclip(start, to)
        clip = fadein(clip, 0.5)
        clip = fadeout(clip, 0.5)
        clips.append(clip)
        last = end
        count += 1

    if full_duration - float(last) > minimum_duration:
        print("Clip {} (Start: {}, End: {})".format(count, last, 'EOF'))
        clips.append(video.subclip(float(last) - kwargs['ease']))

    processed_video = concatenate_videoclips(clips)
    processed_video.write_videofile(
        kwargs['file_out'].replace('\\', ''),
        fps=60,
        preset='ultrafast',
        codec='libx264'
    )

    in_handle.close()
    video.close()


@deco
def movie_concat(conf):
    @deco
    def concat(_in_name, _out_name):
        subprocess.call(
            r'/opt/homebrew/bin/ffmpeg -y -i {} -vf "fade=t=in:st=0:d=0.5" -c:a copy {}'.format(_in_name, _out_name),
            shell=True)
        return 0

    # Import everything needed to edit video clips
    for in_name, out_name in conf.order:
        _ = concat(in_name, out_name)


@deco
def get_mp4title(path):
    titles: List[str] = []
    for file in glob.glob(path):
        title = os.path.split(file)[1].split('.')[0]
        titles.append(title)
    return titles
