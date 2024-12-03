import random
from models.planing_game import PlaningGame

def create_id():
    return ''.join([str(random.randint(0,9)) for a in range(0,9)])

class Game(PlaningGame):
    def __init__(self, player1, player2, round_number, result):
        super().__init__(player1,player2,round_number)
        self.id = create_id()
        self.result = result
