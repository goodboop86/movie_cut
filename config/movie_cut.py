import os

from utils.cmd import deco


class Config:
    """
    - x:y:z -> x:int file, y:{'a','v'} video or audio, z:int channel
    - https://qiita.com/cabbage_lettuce/items/21348358ba46f4110d75
    """
    def __init__(self, title):

        self.title = title
        self.base_dir = r"/Users/kazuya/Google\ Drive/My\ Drive/movie/data"
        self.input_file = f'{self.base_dir}/{self.title}.mp4'
        self.video_file = f'{self.base_dir}/{self.title}/video.mp4'
        self.audio_file = f'{self.base_dir}/{self.title}/audio.wav'
        self.voice_file = f'{self.base_dir}/{self.title}/voice.wav'
        self.silence_file = f'{self.base_dir}/{self.title}/silence.txt'
        self.before_file = f'{self.base_dir}/{self.title}/before.png'
        self.after_file = f'{self.base_dir}/{self.title}/after.png'
        self.amix_file = f'{self.base_dir}/{self.title}/amix.mp3'
        self.merge_file = f'{self.base_dir}/{self.title}/merge.mp4'
        self.edit_file = f'{self.base_dir}/{self.title}/edit.mp4'
        self.output_file = f'{self.base_dir}/{self.title}/output.mp4'
        self.intermediate_output = [self.video_file, self.audio_file, self.voice_file, self.amix_file, self.edit_file]

        self.workdir = f'{self.base_dir}/{self.title}'

        self.video = {
            'in_file': self.input_file,
            'fmt': "0:v",
            'out_file': self.video_file}

        self.audio = {
            'in_file': self.input_file,
            'fmt': "0:a:0",
            'out_file': self.audio_file}

        self.voice = {
            'in_file': self.input_file,
            'fmt': "0:a:1",
            'out_file': self.voice_file}

        self.silence_detect = {
            'in_file': self.voice_file,
            'db': -10,
            'duration': 8,
            'out_file': self.silence_file}

        self.amix_audio = {
            'in_file1': self.audio_file,
            'in_file2': self.voice_file,
            'out_file': self.amix_file}

        self.amix_video = {
            'in_file1': self.input_file,
            'in_file2': self.audio_file,
            'out_file': self.merge_file}

        self.merge_movie = {
            'in_file1': self.video_file,
            'in_file2': self.amix_file,
            'fmt1': '-c:v',
            'fmt2': '-c:a',
            'out_file': self.merge_file}

        self.video_edit = {
            'file_in': self.merge_file,
            'file_out': self.edit_file,
            'silence_file': self.silence_file,
            'ease': 1,
            'padding': 2.5}

        self.short_detect = {
            'silence_file': self.silence_file,
            'before_file': self.before_file,
            'after_file': self.after_file,
            'out_file': self.silence_file,
            'noise_second': 5}

        self.to_playable = {
            'in_file': self.edit_file,
            'out_file': self.output_file}

    @deco
    def remove_intermediate(self):
        for path in self.intermediate_output:
            os.remove(path.replace('\\', ''))

    @deco
    def create_workdir(self):
        os.mkdir(self.workdir.replace('\\', ''))

