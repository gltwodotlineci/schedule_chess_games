import json
import random
from models.players import Player
from models.planing_game import PlaningGame
from models.round import Round
from models.result import ResultGame
from models.tournament import Tournament
from models.game import Game
from views.view1 import geting_dt_tournament


# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)


'''
Tournement,
create ans serialize tournement
'''
def create_tournement():
    given_dt = geting_dt_tournament()
    tournement = Tournament(given_dt[0], given_dt[1], given_dt[2], given_dt[3], given_dt[4])
    
    tournement_list = read_json('json_data/tournement.json')
    tournement_list.append(tournement.__dict__)
    write_json('json_data/tournement.json', tournement_list)
    
def add_round_2tournement():
    list_tournement = read_json('json_data/tournement.json')
    list_rounds = read_json('json_data/rounds.json')
    print("Here is the list of the tornements names:")
    i = 1
    for tournement in list_tournement:
        print(f"{tournement.get('name')} - {i}")
        i +=1

    nb = input(" Chose the number of tournement: ")
    choosed_tournement = list_tournement[int(nb)-1]
    for round in list_rounds:
        if round.get('tournement_id') == choosed_tournement.get('id'):
            choosed_tournement['rounds_list'].append(round)
            
    list_tournement[int(nb)-1] = choosed_tournement

    write_json('json_data/tournement.json', list_tournement)
    print(f'You choosed the "{choosed_tournement.get('name')}" tournement')
    


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
'''
    AfterGame
'''
def simulate_winner():
    possibles_results = ['player1', 'player2','draw']
    return possibles_results[random.randint(0,2)]


# givin games by round
def gemes_by_round(round_nb):
    games = read_json('json_data/preparing_game.json')
    gemes_round = []
    for game in games:
        if game.get('round_number') == round_nb:
            gemes_round.append(game)
    
    return gemes_round


def add_after_game():
    rounds = read_json("json_data/rounds.json")
    given_round_nb = 1
    
    # if given_round.get('number') == given_round:
    #     players = read_json("json_data/players.json")
    games = gemes_by_round(1)
    after_games = []
    results = []
    for game in games:
        player1 = game.get('player1')
        player2 = game.get('player2')
        winner = simulate_winner()
        if winner == 'player1':
            after_game = Game(
                player1,
                player2,
                given_round_nb,
                ([player1,'Won'],[player2,'Loose'])
                )
        elif winner == 'plyer2':
            after_game = Game(
                player1,
                player2,
                given_round_nb,
                ([player1,'Loose'],[player2,'Won'])
                )
        else:
            after_game = Game(
                player1,
                player2,
                given_round_nb,
                ([player1,'Won'],[player2,'Loose'])
                )
        result = ResultGame(after_game.id,winner)
            
        after_games.append(after_game.__dict__)
        results.append(result.__dict__)


    rounds_new = rounds
    for i in range(len(rounds_new)):
        if rounds_new[i].get('number') == given_round_nb:
            rounds_new[i]['game_list'] = after_games

    # adding games with results and results
    write_json('json_data/after_game.json', after_games)
    write_json('json_data/results.json',results)
    # adding list games to round
    write_json('json_data/rounds.json',rounds_new)
                
        


#---------------------------
def planing_games():
    # Calling rounds data
    # with open("json_data/rounds.json",'r') as rounds_file:
    #     rounds = json.load(rounds_file)
    rounds = read_json("json_data/rounds.json")[0]
    games = []
    if rounds.get('number') == 1:
        players = read_json("json_data/players.json")
        sorted_players = sorted(players, key=lambda x: x['last_name'], reverse=False )

        for i in range(0,len(sorted_players),2):
            player1 = sorted_players[i]['id']
            player2 = sorted_players[i+1]['id']
            round_nb = rounds.get('number')
            game = PlaningGame(player1, player2, round_nb)
            games.append(game.__dict__)
            rounds.get('game_list').append(game.__dict__)

        # add games to json
        write_json("json_data/preparing_game.json", games)
        


    elif rounds.get('number') > 1:
        pass

'''
Rresult part:
create and associate points
'''
def prod_result(game_id):
    results_list = read_json('json_data/results.json')
    result = ResultGame(game_id).__dict__
    results_list.append(result)
    # write results as json
    write_json('json_data/results.json', results_list)


def create_results():
    rounds = read_json('json_data/rounds.json')
    print("Please Chose this round number between the next rounds: ")
    for round in rounds:
        print(f"Round N° {round.get('number')}")
    
    round_nb = input(" Your round nb is: ")
    games = read_json('json_data/games.json')
    games_list = []
    for game in games:
        if game.get('round_number') == int(round_nb):
            games_list.append(game)

    for game in games_list:
        game_id = game.get('id')
        result = ResultGame(game_id)
        all_results.append(result.__dict__)

    # write results as json
    #write_json('json_data/results.json', all_results)

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


