from __future__ import unicode_literals

import subprocess

from moviepy.editor import VideoFileClip, concatenate_videoclips


def deco(func):
    def wrapper(*args, **kwargs):
        print("## in {}:".format(func.__name__))
        print("-> args: {}, kwargs: {}".format(args, kwargs))
        res = func(*args, **kwargs)
        if isinstance(res, (str, int, dict)):
            print("-> return: {}".format(res))
        return res

    return wrapper


@deco
def get_lines(cmd):
    """
    :param cmd: str 実行するコマンド.
    :rtype: generator
    :return: 標準出力 (行毎).
    :usage:
        for line in get_lines(cmd=save_stream):
            print(line)
    """
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            yield line

        if not line and proc.poll() is not None:
            break


@deco
def cmd_save_stream(**kwargs) -> str:
    return 'ffmpeg -y -i {} -map {} {} -y'.format(
        kwargs['in_file'],
        kwargs['fmt'],
        kwargs['out_file']
    )

@deco
def cmd_save_multi_stream(**kwargs) -> str:
    return 'ffmpeg -i {} -map {} -map output.mkv'.format(
        kwargs['in_file'],
        kwargs['fmt'],
        kwargs['out_file']
    )

@deco
def cmd_silence_detect(**kwargs) -> str:
    return '{} | {} | {} | {}'.format(
        'ffmpeg -y -hide_banner -vn -i {} -af "silencedetect=n={}dB:d={}" -f null - 2>&1'.format(
            kwargs['in_file'],
            kwargs['db'],
            kwargs['duration']),
        'grep "silence_end"',
        'awk \'{print $5 " " $8}\'',
        'tee {}'.format(
            kwargs['out_file']))


@deco
def cmd_concat_audio(**kwargs) -> str:
    return 'ffmpeg -y -i "concat:{}|{}" -acodec copy {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['out_file']
    )


@deco
def cmd_amix(**kwargs) -> str:
    """
    https://nico-lab.net/amix_with_ffmpeg/
    """
    return 'ffmpeg -y -i {} -i {} -filter_complex amix=inputs=2:duration=first:dropout_transition=2 {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['out_file']
    )


@deco
def cmd_amix_video(**kwargs) -> str:
    """
    https://stackoverflow.com/questions/44712868/ffmpeg-set-volume-in-amix
    """
    return 'ffmpeg -y -i amovie=audio_to_add.mp4:loop=0,asetpts=N/SR/TB,volume=1.0[a] -i {} -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest[out]" ' \
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
    return 'ffmpeg -i {} -i {} -map 0:v -map 0:a -map 1:0 output.mp4'.format(
            kwargs['in_file1'],
            kwargs['in_file2'],
            kwargs['out_file']
        )

@deco
def cmd_merge_movie(**kwargs) -> str:
    return 'ffmpeg -y -i {} -i {} {} copy {} copy {}'.format(
        kwargs['in_file1'],
        kwargs['in_file2'],
        kwargs['fmt1'],
        kwargs['fmt2'],
        kwargs['out_file']
    )


@deco
def video_edit(**kwargs) -> None:
    minimum_duration = 1.0

    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    in_handle = open(kwargs['silence_file'], "r", errors='replace')
    video = VideoFileClip(kwargs['file_in'])
    full_duration = video.duration
    clips = []
    while True:
        line = in_handle.readline()

        if not line:
            break

        end, duration = line.strip().split()

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
        clips.append(clip)
        last = end
        count += 1

    if full_duration - float(last) > minimum_duration:
        print("Clip {} (Start: {}, End: {})".format(count, last, 'EOF'))
        clips.append(video.subclip(float(last) - kwargs['ease']))

    processed_video = concatenate_videoclips(clips)
    processed_video.write_videofile(
        kwargs['file_out'],
        fps=60,
        preset='ultrafast',
        codec='libx264'
    )

    in_handle.close()
    video.close()
