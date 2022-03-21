class Config:
    """
    - x:y:z -> x:int file, y:{'a','v'} video or audio, z:int channel
    - https://qiita.com/cabbage_lettuce/items/21348358ba46f4110d75
    """

<<<<<<< HEAD
    title = 'win_sana_2022-03-15_23-06-34'
=======
    title = 'kabi_win_2022-03-19_00-14-21'
>>>>>>> 1f9a34461e61918bf335c1152c7583f07b936431
    input_file = f'data/{title}/{title}.mp4'
    video_file = f'data/{title}/video.mp4'
    audio_file = f'data/{title}/audio.wav'
    voice_file = f'data/{title}/voice.wav'
    silence_file = f'data/{title}/silence.txt'
    amix_file = f'data/{title}/amix.mp3'
    merge_file = f'data/{title}/merge.mp4'
    output_file = f'data/{title}/output.mp4'
    silence_file = f'data/{title}/silence.txt'
    before_file = f'data/{title}/before.png'
    after_file = f'data/{title}/after.png'

    video = {'in_file': input_file,
             'fmt': "0:v",
             'out_file': video_file}

    audio = {'in_file': input_file,
             'fmt': "0:a:0",
             'out_file': audio_file}

    voice = {'in_file': input_file,
             'fmt': "0:a:1",
             'out_file': voice_file}

    silence_detect = {'in_file': voice_file,
                      'db': -10, 'duration': 8,
                      'out_file': silence_file}

    amix_audio = {
        'in_file1': audio_file,
        'in_file2': voice_file,
        'out_file': amix_file}

    amix_video = {'in_file1': input_file,
                  'in_file2': audio_file,
                  'out_file': merge_file}

    merge_movie = {'in_file1': video_file,
                   'in_file2': amix_file,
                   'fmt1': '-c:v',
                   'fmt2': '-c:a',
                   'out_file': merge_file}

    video_edit = {'file_in': merge_file,
                  'file_out': output_file,
                  'silence_file': silence_file,
                  'ease': 1, 'padding': 2.5}

    short_detect = {'silence_file': silence_file,
                    'before_file': before_file,
                    'after_file': after_file,
                    'out_file': silence_file,
                    'noise_second': 5}
