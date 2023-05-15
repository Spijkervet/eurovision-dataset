import json
import pandas as pd
import os


def read_csv(fp):
    return pd.read_csv(fp)


def to_csv(contest, round):
    # all_votes = [votes for c in contests for votes in c.votes_to_list()]
    all_votes = contest.votes_to_list()
    df = pd.DataFrame(
        all_votes,
        columns=[
            "year",
            "round",
            "from_country_id",
            "to_country_id",
            "from_country",
            "to_country",
            "total_points",
            "tele_points",
            "jury_points",
        ],
    )

    out_fname = f'votes_{round}.csv'
    if not os.path.exists(out_fname):
        df.to_csv(out_fname, index=False)
    else:
        df.to_csv(out_fname, mode="a", header=False, index=False)

    all_contestants = contest.contestants_to_list(round)
    df = pd.DataFrame(
        all_contestants,
        columns=[
            "year",
            "to_country_id",
            "to_country",
            "performer",
            "song",
            "place_contest",
            "sf_num",
            "running_final",
            "running_sf",
            "place_final",
            "points_final",
            "place_sf",
            "points_sf",
            "points_tele_final",
            "points_jury_final",
            "points_tele_sf",
            "points_jury_sf",
            "composers",
            "lyricists",
            "lyrics",
            "youtube_url",
        ],
    )

    out_fname = f'contestants_{round}.csv'
    if not os.path.exists(out_fname):
        df.to_csv(out_fname, index=False)
    else:
        df.to_csv(out_fname, mode="a", header=False, index=False)


def cast_int(i):
    if i is not None and i.isdigit():
        return int(i)
    return None

def prepend_key_in_dict(d: dict, prepend_key: str):
     return {f"{prepend_key}_{k}": v for k, v in d.items()}

def to_dict(obj, prepend_key: str = ""):
    o = json.loads(json.dumps(obj, default=lambda o: o.__dict__))
    if prepend_key != "":
        if type(o) == list:
            for idx in range(len(o)):
                o[idx] = prepend_key_in_dict(o[idx], prepend_key)
        elif type(o) == dict:
            o = prepend_key_in_dict(o, prepend_key)
    return o
