# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import ffmpeg


class Config:
    """
    - x:y:z -> x:int file, y:{'a','v'} video or audio, z:int channel
    - https://qiita.com/cabbage_lettuce/items/21348358ba46f4110d75
    """
    in_fname = "multitrack"
    out_fname = "processed"
    type = "mp4"

    fmt_video = "0:v"
    fmt_audio = "0:a:0"
    fmt_voice = "0:a:1"


c = Config()

# ファイル取得
stream = ffmpeg.input(f"{c.in_fname}.{c.type}")
probe = ffmpeg.probe(f"{c.in_fname}.{c.type}")

print("stream")
# ストリーム抽出
video = ffmpeg.output(stream, filename=f'video.{c.type}', map=c.fmt_video)
audio = ffmpeg.output(stream, filename=f'audio.{c.type}', map=c.fmt_audio)
voice = ffmpeg.output(stream, filename=f'voice.{c.type}', map=c.fmt_voice)

print("channel")
# 分離し保存
ffmpeg.run(video, overwrite_output=True)
ffmpeg.run(audio, overwrite_output=True)
ffmpeg.run(voice, overwrite_output=True)

print("input")
# 音声ファイル取得
stream = ffmpeg.input(f"{c.fmt_audio}.{c.type}")

# 無音区間抽出

