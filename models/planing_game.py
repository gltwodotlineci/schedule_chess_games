import random

def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])

class PlaningGame:
    def __init__(self, player1, player2, round_number):
        self.id = create_id()
        self.player1 = player1
        self.player2 = player2
        if random.randint(0,1) == 0:
            self.white_king = self.player1
            self.black_king = self.player2
        else:
            self.white_king = self.player2
            self.black_king = self.player1
        self.round_number = round_number
