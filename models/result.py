import random
def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])
    

class ResultGame:
    def __init__(self, after_game_id, winner):
        self.id = create_id()
        self.after_game_id = after_game_id
        self.winner = winner

    def serialize_result_game(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'winner': self.winner 
        }
