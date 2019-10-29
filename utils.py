import pandas as pd


def read_csv(fp):
    return pd.read_csv(fp)


def to_csv(contests):
    all_votes = [votes for c in contests for votes in c.votes_to_list()]
    df = pd.DataFrame(all_votes, columns=[
                      'year', 'round', 'from_country_id', 'to_country_id', 'from_country', 'to_country', 'points'])
    df.to_csv('votes.csv', index=False)

    all_contestants = [
        contestant for c in contests for contestant in c.contestants_to_list()]
    df = pd.DataFrame(all_contestants,
                      columns=['year', 'from_country_id', 'from_country', 'performer', 'song',
                      'running_final', 'running_sf1', 'running_sf2',
                      'place_final', 'points_final', 'place_sf1', 'points_sf1', 'place_sf2', 'points_sf2', 
                      'points_tele_final', 'points_jury_final', 'points_tele_sf1', 'points_jury_sf1',
                      'points_tele_sf2', 'points_jury_sf2', 'lyrics', 'youtube_url'])
    df.to_csv('contestants.csv', index=False)