import os
from shutil import which
from glob import glob
import subprocess


if which('streaming_extractor_music') is None:
    raise FileNotFoundError('Essentia\'s streaming_extrator_music is not found in PATH')

files = glob('audio/**/*.mp3')
for f in files:
    output_path = os.path.join(os.path.splitext(f)[0] + '.json')
    print(output_path)
    if not os.path.exists(output_path):
        print('Extracting audio features from {}'.format(f))
        subprocess.call(['streaming_extractor_music', f, output_path])