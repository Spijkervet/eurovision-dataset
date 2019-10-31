import pandas as pd
import os


def read_csv(fp):
    return pd.read_csv(fp)


def to_csv(contest):
    # all_votes = [votes for c in contests for votes in c.votes_to_list()]
    all_votes = contest.votes_to_list()
    df = pd.DataFrame(all_votes, columns=[
                      'year', 'round', 'from_country_id', 'to_country_id', 'from_country', 'to_country', 'total_points', 'tele_points', 'jury_points'])

    if not os.path.exists('votes.csv'):
        df.to_csv('votes.csv', index=False)
    else:
        df.to_csv('votes.csv', mode='a', header=False, index=False)

    all_contestants = contest.contestants_to_list()
    df = pd.DataFrame(all_contestants,
                      columns=['year', 'from_country_id', 'from_country', 'performer', 'song', 'sf_num',
                               'running_final', 'running_sf',
                               'place_final', 'points_final', 'place_sf', 'points_sf',
                               'points_tele_final', 'points_jury_final', 'points_tele_sf', 'points_jury_sf',
                               'composers', 'lyricists',
                               'lyrics', 'youtube_url'])

    if not os.path.exists('contestants.csv'):
        df.to_csv('contestants.csv', index=False)
    else:
        df.to_csv('contestants.csv', mode='a', header=False, index=False)
