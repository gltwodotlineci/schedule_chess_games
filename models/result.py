import random
def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])
    

class ResultGame:
    def __init__(self, game_id):
        self.id = create_id()
        self.game_id = game_id
        possibles_results = ['player1', 'player2','draw']
        self.winner = possibles_results[random.randint(0,2)]

    def serialize_result_game(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'winner': self.winner 
        }
