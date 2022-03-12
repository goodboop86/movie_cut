from __future__ import unicode_literals

import subprocess
from utils import utils


class Config:
    """
    - x:y:z -> x:int file, y:{'a','v'} video or audio, z:int channel
    - https://qiita.com/cabbage_lettuce/items/21348358ba46f4110d75
    """
    input_file = 'data/multitrack.mp4'
    video_file = 'data/video.mp4'
    audio_file = 'data/audio.mp3'
    voice_file = 'data/voice.mp3'
    silence_file = 'data/silence.txt'
    amix_file = 'data/amix.mp3'
    merge_file = 'data/merge.mp4'
    output_file = 'data/output.mp4'

    video = {'in_file': input_file, 'fmt': "0:v", 'out_file': video_file}
    audio = {'in_file': input_file, 'fmt': "0:a:0", 'out_file': audio_file}
    voice = {'in_file': input_file, 'fmt': "0:a:1", 'out_file': voice_file}
    silence_detect = {'in_file': voice_file, 'db': -20, 'duration': 0.5, 'out_file': silence_file}
    amix_audio = {'in_file1': audio_file, 'in_file2': voice_file, 'out_file': amix_file}
    amix_video = {'in_file1': input_file, 'in_file2': audio_file, 'out_file': merge_file}
    merge_movie = {'in_file1': video_file, 'in_file2': amix_file, 'fmt1': '-c:v', 'fmt2': '-c:a',
                   'out_file': merge_file}
    video_edit = {'file_in': merge_file, 'file_out': output_file, 'silence_file': silence_file, 'ease': 1}


c = Config()

# 音声ストリーム作成
subprocess.call(utils.cmd_save_stream(**c.video), shell=True)
subprocess.call(utils.cmd_save_stream(**c.audio), shell=True)
subprocess.call(utils.cmd_save_stream(**c.voice), shell=True)

# 無音区間取得
subprocess.call(utils.cmd_silence_detect(**c.silence_detect), shell=True)

# 音を結合
subprocess.call(utils.cmd_amix(**c.amix_audio), shell=True)
# subprocess.call(utils.cmd_amix(**c.amix_video), shell=True)
# subprocess.call(utils.cmd_merge(**c.amix_video), shell=True)

# 音と映像を結合
subprocess.call(utils.cmd_merge(**c.merge_movie), shell=True)

# 無音区間削除
utils.video_edit(**c.video_edit)
