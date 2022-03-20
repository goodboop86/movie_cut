from __future__ import unicode_literals

import subprocess

from config.config import Config
from utils import cmd, silence_plan


c = Config()

# 音声ストリーム作成
subprocess.call(cmd.cmd_save_stream(**c.video), shell=True)
subprocess.call(cmd.cmd_save_stream(**c.audio), shell=True)
subprocess.call(cmd.cmd_save_stream(**c.voice), shell=True)

# 無音区間取得
subprocess.call(cmd.cmd_silence_detect(**c.silence_detect), shell=True)

# 削除プランニング
silence_plan.main(**c.short_detect)

# 音を結合
subprocess.call(cmd.cmd_amix(**c.amix_audio), shell=True)

# 音と映像を結合
subprocess.call(cmd.cmd_merge_movie(**c.merge_movie), shell=True)

# 無音区間削除
cmd.video_edit(**c.video_edit)
