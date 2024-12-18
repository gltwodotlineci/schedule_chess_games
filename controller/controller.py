import json
import random
from datetime import datetime
from operator import attrgetter

from models.player import Player
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


def today_str():
    return datetime.now().strftime("%d-%m-%Y-%H-%M")

'''
Round
'''
def all_rounds():
    list_rounds = read_json('json_data/rounds.json')
    return list_rounds


def create_round(data):
    validate = False
    while validate is not True:
        try:
            validated_data = ValidateRound(**data)
            round = Round(
                validated_data.tournament_id,
                validated_data.name,
                validated_data.number,
                validated_data.starting_date_hour
            )
            validate = True
        except ValueError as e:
            print(f"Error: {e}")
            validate = False
    tournament = Tournament.from_db(round.tournament_id)
    tournament.actual_round_number = round.number
    tournament.rounds_list.append(round.id)
    tournament.save(tournament.id)
    round.save()
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
    tours = Tournament.all_data()
    return tours


def list_tournaments_players():
    data = {}
    data['tournaments'] = Tournament.all_data()#read_json('json_data/tournaments.json')
    data['players'] = Player.all_data()#read_json('json_data/players.json')
    return data

def create_tournament(given_dt):

    try:
        valid_dt = ValidateTournament(**given_dt)
        tournament = Tournament(
            valid_dt.name,
            valid_dt.place,
            valid_dt.starting_date,
            valid_dt.ending_date,
            valid_dt.description,
            valid_dt.nb_players
        )
        validate = True
    except ValueError as e:
            print(f"Error: {e}")
            validate = False

    while validate != True:
        print("Remember the format of the date: 'dd-mm-yyyy' ")
        given_dt['starting_date'] = input("write again the starting date please: ")
        given_dt['ending_date'] = input("write again the ending date please: ")
        given_dt['nb_players'] = input("write again the number of players please: ")

        try:
            valid_dt = ValidateTournament(**given_dt)
            tournament = Tournament(
            valid_dt.name,
            valid_dt.place,
            valid_dt.starting_date,
            valid_dt.ending_date,
            valid_dt.description,
            valid_dt.nb_players
            )
        except ValueError as e:
            print(e)
            validate = False

    tournament.save()
    return tournament


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
# def add_player2_tour(given_tour, player):
#     tournaments = read_json('json_data/tournaments.json')
#     for i,tour in enumerate(tournaments):
#         if tour.get('id') == given_tour:#.id:
#             tournaments[i]['players_list'].append(player.id)

#     write_json('json_data/tournaments.json',tournaments)



'''
Players part:
'''
# List of all players
def all_players():
    all_players = Player.all_data()
    return all_players

# check if fin exists
def check_fin(data):
    for fin in Player.all_data():
        if fin.fin == data:
            return True

    return False


def enter_existing_player(fed_id,tour):
    count = 0
    for player_id in tour.players_list:
        try:
            Player.from_db('fin',fed_id)
            count += 1
        except ValueError:
            pass

    if count > 0:
        True

    False




def create_player(dt): 
    try:
        dt_validator = ValidatePlayer(**dt)
        player = Player(
            dt_validator.fin,
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
        print("Remember the fin format exemple is: 'AB1245' ")
        dt['fin'] = input("write again the fin number: ")
        try:
            dt_validator = ValidatePlayer(**dt)
            player = Player(
                dt_validator.fin,
                dt_validator.first_name,
                dt_validator.last_name,
                dt_validator.birth_date
            )
            validate = True
        except ValueError as e:
            print(f"Error: {e}")
            validate = False

    # saving player to data
    player.save_dt()


#selecting player from it's
def order_players(players_id):
    lst_players = []
    for pl_id in players_id:
        player = Player.from_db('id',pl_id)
        lst_players.append(player)
    
    # ordering the players from last name
    lst_players.sort(key=attrgetter('last_name'))
    lst_players.sort(key=attrgetter('points'), reverse=True)
    return lst_players

def add_players2_round(round, players):
    round.games_list = players
    round.save(round.id)



# ad multiple players
def add_player2_tour(tour, fed_id):
    
    pl = Player.from_db('fin',fed_id)
    intermedian = tour.players_list
    intermedian.append(pl.id)
    tour.players_list = intermedian
    
        # valide = False
        # while valide is False:
        #     try:
        #         pl = Player.from_db('fin',fed_id)
        #         valide = True
        #         tour.players_list.append(pl.id)

        #     except ValueError:
        #         print("Please check again your choice")
        #         print("It seams the FED Id does not exist")
        #         valide = False

    tour.save(tour.id)


def refac_if__game(player_result):
    pt = 0.0
    if player_result:
        pt = 1.0
    elif player_result is False:
        pt = 0.5
    return pt


def add_points_to_players(games):
    players = Player.all_data()

    for player in players:    
        for game in games:
            if player.id in game.player1_result:
                player.points += refac_if__game(game.player1_result[1])
                player.save_dt(player.id)

            elif player.id in game.player2_result:
                player.points += refac_if__game(game.player2_result[1])
                player.save_dt(player.id)
                round_id = game.round_id

                
    # Add closing hour to round.
    round = Round.from_db(round_id)
    round.ending_date_hour = today_str()
    round.save(round_id)

    return players


'''
Game part:
create and serialize game
'''
def simulate_winner():
    possibles_results = ['player1', 'player2','draw']
    return possibles_results[random.randint(0,2)]


def organize_game(players,round):
    nb = len(players)
    games = []
    for i in range(0,nb,2):
        game  = Game(
            round.id,
            players[i].id,
            players[i+1].id,
            round.number,
            )
        game.save()
        games.append(game)

    return games

def organize_game_rd2(players,round):
    nb = len(players)
    games = []
    for i in range(0,nb,2):
        game  = Game(
            round.id,
            players[i].id,
            players[i+1].id,
            round.number,
            )
        game.save()
        games.append(game)

    return games


# givin games by round
def games_by_round(round_nb):
    games_lst = []
    for game in Game.all_data():
        if game.round_id == round_nb:
            games_lst.append(game)

    return games_lst


def add_results(results_list,games):
    for i,game in enumerate(games):
        if results_list[i] == "1":
            game.set_winner(game.player1)
        elif results_list[i] == "2":
            game.set_winner(game.player2)
        elif results_list[i] == "3":
            game.set_winner("None")
        # save results on game:
        game.save(game.id)

    return games


#--
# make the planing of thee games
def planing_games():
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
        



# showing players contests for round
def show_challanges(games_by_round):
    players = []
    for game in games_by_round:
        id_p1 = game.player1
        id_p2 = game.player2
        playr1 = Player.from_db('id',id_p1)
        playr2 = Player.from_db('id',id_p2)
        players.append([playr1, playr2])

    return players

# add points after game
def add_after_game():
    rounds = read_json("json_data/rounds.json")
    given_round_nb = 1
    
    # if given_round.get('number') == given_round:
    #     players = read_json("json_data/players.json")
    games = games_by_round(1)
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
