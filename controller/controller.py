import json
from models.players import Player
from models.game import Game
from models.round import Round
from models.result import ResultGame


# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)



'''
Players part:
create and serialize player
'''
def create_player():
    players = []
    players.append(Player('aqif','kapertoni','22-06-1979').serialize_players())
    players.append(Player('Afrim', 'Tahipi', '01-01-2000').serialize_players())
    players.append(Player('Zeqo', 'Pilafi', '01-11-1912').serialize_players())
    with open('json_data/players.json', 'w') as f:
        json.dump(players,f,indent=2)


'''
Game part:
create and serialize game
'''
def create_games():
    # Calling rounds data
    # with open("json_data/rounds.json",'r') as rounds_file:
    #     rounds = json.load(rounds_file)
    rounds = read_json("json_data/rounds.json")
    games = []
    if rounds.get('number') == 1:
        players = read_json("json_data/players.json")
        sorted_players = sorted(players, key=lambda x: x['last_name'], reverse=False )

        for i in range(0,len(sorted_players),2):
            player1 = sorted_players[i]['id']
            player2 = sorted_players[i+1]['id']
            round_nb = rounds.get('number')
            game = Game(player1, player2, round_nb).__dict__
            games.append(game)
            rounds.get('game_list').append(game)

        # add games to json
        write_json("json_data/games.json", games)
        # adding list games to round
        with open("json_data/rounds.json",'w') as round_file2:
            json.dump(rounds, round_file2, indent=2)


    elif rounds.get('number') > 1:
        pass

'''
Rresult part:
create and associate points
'''
def create_results():
    rounds = read_json('json_data/rounds.json')
    games_list = rounds.get('game_list')
    all_results = []
    for game in games_list:
        game_id = game.get('id')
        result = ResultGame(game_id)
        all_results.append(result.__dict__)

    # write results as json
    write_json('json_data/results.json', all_results)

# passing the results to the game:
def passing_results2games():
    results = read_json('json_data/results.json')
    games = read_json('json_data/games.json')
    for result in results:
        game_id = result.get('game_id')
        winner = result.get('winner')
        new_game_list = []
        for game in games:
            if game.get('id') == game_id:
                game['winner'] = winner
                if result.get('winner') != 'draw':
                    game['winner_id'] = (game.get(winner))
                else:
                    game['winner_id'] = (game.get('player1'), game.get('player2'))
            
            new_game_list.append(game)
    write_json('json_data/games.json', new_game_list)

    return new_game_list

def add_points_to_players():
    games = read_json('json_data/games.json')
    players = read_json('json_data/players.json')
    new_list_players = []
    for player in players:
        player_id = player.get('id')
        for game in games:
            if player_id in game.get('winner_id'):
                if game.get('winner') == 'draw':
                    player['points'] += 0.5
                else:
                    player['points'] += 1.0
        
        new_list_players.append(player)

    write_json('json_data/players.json', new_list_players)



'''
Round part:
create and serialize round
'''
def create_round(round_name, number):
    round_dict = Round(round_name, number).serialize_round()
    new_round = json.dumps(round_dict)
    new_round
    with open("json_data/rounds.json", "w") as f:
        f.write(new_round)

#---------------------------------------


