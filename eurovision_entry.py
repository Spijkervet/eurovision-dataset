class EurovisionEntry():

        def __init__(self, country, performer, song, place_f, points_f, place_sf1, points_sf1, place_sf2, points_sf2, year, broadcaster, composer, writer):
            self.year = year
            self.country = country
            self.performer = performer
            self.song = song
            self.place_f = place_f
            self.points_f = points_f
            self.place_sf1 = place_sf1
            self.points_sf1 = points_sf1
            self.place_sf2 = place_sf2
            self.points_sf2 = points_sf2

            self.broadcaster = broadcaster
            self.composer = composer
            self.writer = writer

        def __str__(self):
            return '{} ({}) - {} - {}'.format(self.country, self.year, self.performer, self.song)