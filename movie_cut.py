from __future__ import unicode_literals

import subprocess

from config.movie_cut import Config
from utils import cmd, silence_plan
from utils.cmd import deco


@deco
def call(_cmd):
    status = subprocess.call(_cmd, shell=True)
    return status


@deco
def movie_cut(_title):
    c = Config(title=_title)
    c.create_workdir()

    # 音声ストリーム作成
    _ = call(cmd.cmd_save_stream(**c.video))
    _ = call(cmd.cmd_save_audio_stream(**c.audio))
    _ = call(cmd.cmd_save_audio_stream(**c.voice))

    # 無音区間取得
    _ = call(cmd.cmd_silence_detect(**c.silence_detect))

    # 削除プランニング
    silence_plan.main(**c.short_detect)

    # 音を結合
    _ = call(cmd.cmd_amix(**c.amix_audio))

    # 音と映像を結合
    _ = call(cmd.cmd_merge_movie(**c.merge_movie))

    # 無音区間削除
    cmd.video_edit(**c.video_edit)

    # quicktimeで再生できるようにする。
    _ = call(cmd.cmd_to_playable(**c.to_playable))

    # 中間成果物を削除
    c.remove_intermediate()


if __name__ == '__main__':
    titles = cmd.get_mp4title(path=r"/Users/kazuya/Google Drive/My Drive/movie/data/*.mp4")
    for title in titles:
        movie_cut(_title=title)
