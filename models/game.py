import random

def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])

class Game:
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
        self.winner = None
        self.winner_id = None


    def serialize_game(self):
        return {
            'id': self.id,
            'player 1': self.player1,
            'player 2': self.player2,
            'round number': self.round_number,
            'winner': self.winner,
            'winner_id': self.winner_id
            }


    def wining(self):
        if random.int(0,1) == 0:
            print("player 1 won")