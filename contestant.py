class Contestant():

    # , points_f, place_sf1, points_sf1, place_sf2, points_sf2, broadcaster, composer, writer):
    def __init__(self, year, country, performer, song, page_url,
                 running_final=None, running_sf=None,
                 sf_num=None,
                 place_final=None, points_final=None,
                 place_sf=None, points_sf=None,
                 points_tele_final=None, points_jury_final=None,
                 points_tele_sf=None, points_jury_sf=None):

        self.year = year
        self.country = country
        self.performer = performer
        self.song = song
        self.page_url = page_url
        self.composers = []
        self.lyricists = [] 
        self.lyrics = None
        self.youtube_url = None
        
        self.sf_num = sf_num
        self.running_final = running_final
        self.running_sf = running_sf

        # All possible places and points
        self.place_final = place_final
        self.points_final = points_final
        self.place_sf = place_sf
        self.points_sf = points_sf
        self.points_tele_final = points_tele_final
        self.points_jury_final = points_jury_final
        self.points_tele_sf = points_tele_sf
        self.points_jury_sf = points_jury_sf

        # self.broadcaster = broadcaster
        # self.composer = composer
        # self.writer = writer

    def __str__(self):
        return '{} ({}) - {} - {}'.format(self.country, self.year, self.performer, self.song)
