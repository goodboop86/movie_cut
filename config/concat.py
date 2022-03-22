import os

from utils.cmd import deco
from collections import OrderedDict


class Config:
    """
    - x:y:z -> x:int file, y:{'a','v'} video or audio, z:int channel
    - https://qiita.com/cabbage_lettuce/items/21348358ba46f4110d75
    """
    def __init__(self):

        self.base_dir = r"/Users/kazuya/Google\ Drive/My\ Drive/movie/artifact/my_movie"

        self.intro = r"transit.mp4"
        self.elem1 = r"elem1.mp4"
        self.transit = r"transit.mp4"
        self.elem2 = r"elem2.mp4"
        self.outro = r"outro.mp4"
        self.artifact = f"{self.base_dir}/artifact.mp4"

        self.txt = f"{self.base_dir}/concat.txt"
        self.artifact = f"{self.base_dir}/artifact.mp4"

        self.order = [
            [r'{}/{}'.format(self.base_dir, self.intro), r'{}/fade_{}'.format(self.base_dir, self.intro)],
            [r'{}/{}'.format(self.base_dir, self.elem1), r'{}/fade_{}'.format(self.base_dir, self.elem1)],
            [r'{}/{}'.format(self.base_dir, self.transit), r'{}/fade_{}'.format(self.base_dir, self.transit)],
            [r'{}/{}'.format(self.base_dir, self.elem2), r'{}/fade_{}'.format(self.base_dir, self.elem2)],
            [r'{}/{}'.format(self.base_dir, self.outro), r'{}/fade_{}'.format(self.base_dir, self.outro)]]



    @deco
    def remove_intermediate(self):
        for path in self.intermediate_output:
            os.remove(path.replace('\\', ''))
