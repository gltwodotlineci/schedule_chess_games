import random
def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])


class Game():
    def __init__(self,round_id, player1, player2, round_nb):
        self.id = create_id()
        self.round_id = round_id,
        self.player1_result = [player1, None]
        self.player2_result = [player2, None]
        self.round_nb = round_nb

    @property
    def player1(self):
        return self.player1_result[0]
    
    @property
    def player2(self):
        return self.player2_result[0]

    def set_winner(self, winner):
        if winner == self.player1:
            self.player1_result[1] = True
        elif winner == self.player2:
            self.player2_result[1] = True
        
    def serialize_game(self):
        return {
            'id': self.id,
            'result': (self.player1_result,self.player2_result)
        }
