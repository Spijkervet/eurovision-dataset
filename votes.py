from collections import defaultdict

class Votes():
    """
    Class holding the voting data to and from all countries in a specific year
    """

    def __init__(self, year, contest_round, votes): 
        self.year = year
        self.round = contest_round
        self.table = votes