from __future__ import unicode_literals

import subprocess

from config.concat import Config
from utils import cmd, silence_plan


def concat():
    c = Config()
    cmd.movie_concat(conf=c)


if __name__ == '__main__':
    concat()
