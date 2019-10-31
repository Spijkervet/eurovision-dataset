import os
import subprocess
import pandas as pd
import youtube_dl

audio_dir = 'audio'
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir)

contestants = pd.read_csv('contestants.csv')
for i, r in contestants.iterrows():
    destination_dir = os.path.join(audio_dir, str(r['year']))
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    youtube_url = r['youtube_url']
    if youtube_url:
        fn = '{}_{}_{}'.format(
            r['from_country'], r['song'], r['performer'])

        # Skip if file already exists
        fp = os.path.join(destination_dir, fn)
        if os.path.exists(fp + '.mp3'):
            print('{} already exists'.format(fp))
            continue

        ydl_opts = {
            'outtmpl': fp + '.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except Exception as e:
            print(e)
            pass