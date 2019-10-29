class Contestant():

    # , points_f, place_sf1, points_sf1, place_sf2, points_sf2, broadcaster, composer, writer):
    def __init__(self, year, country, performer, song, page_url,
                 running_final=None, running_sf1=None, running_sf2=None,
                 place_final=None, points_final=None,
                 place_sf1=None, points_sf1=None,
                 place_sf2=None, points_sf2=None,
                 points_tele_final=None, points_jury_final=None,
                 points_tele_sf1=None, points_jury_sf1=None,
                 points_tele_sf2=None, points_jury_sf2=None):

        self.year = year
        self.country = country
        self.performer = performer
        self.song = song
        self.page_url = page_url
        self.lyrics = None
        self.youtube_url = None
        
        
        self.running_final = running_final
        self.running_sf1 = running_sf1
        self.running_sf2 = running_sf2

        # All possible places and points
        self.place_final = place_final
        self.points_final = points_final
        self.place_sf1 = place_sf1
        self.points_sf1 = points_sf1
        self.place_sf2 = place_sf2
        self.points_sf2 = points_sf2
        self.points_tele_final = points_tele_final
        self.points_jury_final = points_jury_final
        self.points_tele_sf1 = points_tele_sf1
        self.points_jury_sf1 = points_jury_sf1
        self.points_tele_sf2 = points_tele_sf2
        self.points_jury_sf2 = points_jury_sf2

        # self.broadcaster = broadcaster
        # self.composer = composer
        # self.writer = writer

    def __str__(self):
        return '{} ({}) - {} - {}'.format(self.country, self.year, self.performer, self.song)
