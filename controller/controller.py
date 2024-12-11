import json
import random
from models.player import Player
from models.planing_game import PlaningGame
from models.round import Round
from models.result import ResultGame
from models.tournament import Tournament
from models.game import Game
from controller.validator import ValidatePlayer
from controller.validator import ValidateRound
from controller.validator import ValidateTournament

# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)



'''
Round
'''
def all_rounds():
    list_rounds = read_json('json_data/rounds.json')
    return list_rounds


def create_round(round_nb,tournament_id=None):
    round_nb = round_nb[0]
    if tournament_id == None:
        tournament_id = input("Tournament id: ")
    validated_data = ValidateRound(tournament_id, f"Round {round_nb}",int(round_nb))
    round = Round(validated_data.tournament_id, validated_data.name, validated_data.number)
    # add round to json
    rounds_list = read_json('json_data/rounds.json')
    rounds_list.append(round.serialize_round())
    write_json('json_data/rounds.json',rounds_list)
    return round


def add_round_2_tour(round):
    list_tours = read_json('json_data/tournaments.json')
    for i,tour in enumerate(list_tours):
        if round.tournament_id == tour.get('id'):
            list_tours[i].get('rounds_list').append(round.name)
    write_json('json_data/tournaments.json', list_tours)


'''
Tournement,
create ans serialize tournement
'''
def all_tournaments():
    list_tournament = read_json('json_data/tournaments.json')
    return list_tournament


def list_tournaments_players():
    data = {}
    data['tournaments'] = read_json('json_data/tournaments.json')
    data['players'] = read_json('json_data/players.json')
    return data

def create_tournament(given_dt):
    valid_dt = ValidateTournament(**given_dt)
    tournement = Tournament(
        valid_dt.name,
        valid_dt.place,
        valid_dt.starting_date,
        valid_dt.ending_date,
        valid_dt.description
        )
    tournament_list = read_json('json_data/tournaments.json')
    tournament_list.append(tournement.serialize_data())
    write_json('json_data/tournaments.json', tournament_list)
    return tournement

def edit_tournament(tour_id,attribute,value):
    list_tours = read_json('json_data/tournaments.json')
    x = None
    for i,tour in enumerate(list_tours):
        if tour.get("id") == tour_id:
            x = i
            if attribute == 'players_list':
                for player in value:
                    list_tours[i][attribute].append(player)# replace with 'tour'
                

    list_tours[x][attribute] = list(dict.fromkeys(list_tours[x][attribute]))

    write_json('json_data/tournaments.json', list_tours)


def add_round_2tournement(round_id, tournament_id):
    list_tournament = read_json('json_data/tournaments.json')

    index_tour = None
    tour = None
    for i, tournament in enumerate(list_tournament):
        if tournament.get('id') == tournament_id:
            index_tour = i
            tour = tournament

    tour.get('rounds_list').append(round_id)
    list_tournament[index_tour] = tour

    write_json('json_data/tournaments.json', list_tournament)
    

# Adding player id to Taurnement
# ?????
def add_player2_tour(given_tour, player):
    tournaments = read_json('json_data/tournaments.json')
    for i,tour in enumerate(tournaments):
        if tour.get('id') == given_tour:#.id:
            tournaments[i]['players_list'].append(player.id)

    write_json('json_data/tournaments.json',tournaments)



'''
Players part:
create and serialize player
'''
# List of all players
def all_players():
    all_players = read_json('json_data/players.json')
    return all_players


def create_player(dt): 
    try:
        dt_validator = ValidatePlayer(**dt)
        player = Player(
            dt_validator.first_name,
            dt_validator.last_name,
            dt_validator.birth_date
        )
        validate = True
    except ValueError as e:
            print(f"Error: {e}")
            validate = False

    while validate != True:
        dt['birth_date'] = input("write again the birth date please: ")
        try:
            dt_validator = ValidatePlayer(**dt)
            player = Player(
                dt_validator.first_name,
                dt_validator.last_name,
                dt_validator.birth_date
            )
            validate = True
        except ValueError as e:
            print(f"Error: {e}")
            validate = False

    # saving player to data
    players = read_json('json_data/players.json')
    players.append(player.serialize_player())
    write_json('json_data/players.json',players)
    return player



'''
Game part:
create and serialize game
'''
def simulate_winner():
    possibles_results = ['player1', 'player2','draw']
    return possibles_results[random.randint(0,2)]


def all_games():
    games = read_json('json_data/games.json')
    return games


# givin games by round
def gemes_by_round(round_nb):
    games = read_json('json_data/preparing_game.json')
    gemes_round = []
    for game in games:
        if game.get('round_number') == round_nb:
            gemes_round.append(game)
    
    return gemes_round


# make the planing of thee games
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

def add_points_to_players(game):
    players = read_json('json_data/players.json')
    new_list_players = []
    for player in players:
        player_id = player.get('id')
        if player_id == game[0][0]:
            if game[0][1] == 'Draw':
                player['points'] += 0.5
            elif game[0][1] == 'Won':
                player['points'] += 1
        if player_id == game[1][0]:
            if game[1][1] == 'Draw':
                player['points'] += 0.5
            elif game[0][1] == 'Won':
                player['points'] += 1
        
        new_list_players.append(player)
    write_json('json_data/players.json', new_list_players)


# add points after game
def add_after_game():
    rounds = read_json("json_data/rounds.json")
    given_round_nb = 1
    
    # if given_round.get('number') == given_round:
    #     players = read_json("json_data/players.json")
    games = gemes_by_round(1)
    after_games = []
    results = []
    games_for_plyers = []

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
                ([player1,'Draw'],[player2,'Draw'])
                )
        # Adding points to players
        add_points_to_players(after_game.result)

        result = ResultGame(after_game.id,winner)
        after_games.append(after_game.__dict__)
        games_for_plyers.append(after_game)
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


#---------------------------------------
