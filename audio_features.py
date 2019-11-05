import os
import pickle
from tqdm import tqdm
import essentia.standard as es


audio_dir = 'audio'
features_dir = 'audio_features'
if not os.path.exists(features_dir):
    os.makedirs(features_dir)

c = 0
for root, dirs, files in tqdm(os.walk(audio_dir)):
    for f in files:
        fp = os.path.join(root, f)
        if os.path.splitext(fp)[1] != '.mp3':
            print(os.path.splitext(fp))
            continue
        

        c += 1
        year = root.split('/')[1]
        # Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
        # features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
        #                                             rhythmStats=['mean', 'stdev'],
        #                                             tonalStats=['mean', 'stdev'])(fp)

        # if not os.path.exists(os.path.join(features_dir, year)):
        #     os.makedirs(os.path.join(features_dir, year))

        # features_path = os.path.join(features_dir, year, '{}.features.pickle'.format(os.path.splitext(f)[0]))
        # features_frames_path = os.path.join(features_dir, year, '{}.features_frames.pickle'.format(os.path.splitext(f)[0]))

        # print('Saving features to {}'.format(features_path))
        # pickle.dump(features, open(features_path, "wb"))
        # print('Saving frame features to {}'.format(features_path))
        # pickle.dump(features_frames, open(features_frames_path, "wb"))

print(c)