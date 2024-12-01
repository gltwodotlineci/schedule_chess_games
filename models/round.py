
class Round:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.games_list = []
#        self.player_list = player_list

    def serialize_round(self):
        return {
            'number': self.number,
            'name': self.name,
            'game_list': self.games_list
        }


    def organize_games(self):
        for player in self.player_list:
            print(player.name)
