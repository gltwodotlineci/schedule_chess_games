import json
import random
from datetime import datetime
from operator import attrgetter

from models.player import Player
from models.round import Round
from models.tournament import Tournament
from models.game import Game
from controller.validator import ValidatePlayer
from controller.validator import ValidateRound
from controller.validator import ValidateTournament
from controller.refactor_cont import support_create


def today_str():
    return datetime.now().strftime("%d-%m-%Y-%H:%M")


'''
Round
'''

def create_round(data):
    round = support_create(ValidateRound, Round, data, 'round')
    # adding round id to Tournament
    tournament = Tournament.from_db(round.tournament_id)
    tournament.rounds_list.append(str(round.id))
    tournament.save(str(tournament.id))
    round.save()
    return round


#get the current round
def get_current_round(tour):
    current_round = tour.actual_round_number
    round_id = tour.rounds_list[current_round]
    round = Round.from_db(round_id)
    return round


'''
Tournement,
create ans serialize tournement
'''
def create_tournament(data):
    tournament = support_create(ValidateTournament, Tournament, data,'tournament')
    tournament.save()
    return tournament


def all_tournaments():
    tours = Tournament.all_data()
    return tours


def list_tournaments_players():
    data = {}
    data['tournaments'] = Tournament.all_data()
    data['players'] = Player.all_data()
    return data


def edit_tour_round(round):
    tour = Tournament.from_db(round.tournament_id)
    tour.actual_round_number += 1
    tour.save(str(tour.id))
    round.ending_date_hour = today_str()
    round.save(str(round.id))

    return tour


'''
Players part:
'''
# Create player
def create_player(data):
    player = support_create(ValidatePlayer, Player, data, 'player')
    player.save_dt()
    return player


# List of all players
def all_players():
    all_players = Player.all_data()
    all_players.sort(key=attrgetter('last_name'))
    return all_players


# List of players from a tournament
def tournament_players(players):
    tour_players_lst = players
    tour_players_lst.sort(key=attrgetter('last_name'))
    return tour_players_lst



# check if fin exists
def check_fin(data):
    for fin in Player.all_data():
        if fin.fin == data:
            return True

    return False


def enter_existing_player(fed_id,tour):
    for player_id in tour.players_list:
        player = Player.from_db('id',player_id)
        if player.fin == fed_id:
            return True

    return False


#selecting player from it's last name
def order_players(players_id,round1=False):
    lst_players = []
    for pl_id in players_id:
        player = Player.from_db('id',pl_id)
        lst_players.append(player)
    
    # ordering the players from last name
    if round1:
        lst_players.sort(key=attrgetter('last_name'))
    return lst_players


# ad multiple players
def add_player2_tour(tour, fed_id):
    pl = Player.from_db('fin',fed_id)
    tour.players_list.append(pl.id)

    tour.save(str(tour.id))


def refact_if__game(player_result):
    if player_result is True:
        return 1.0
    elif player_result is False:
        return 0.5
    elif player_result is None:
        return 0.0


'''
Game part:
create and serialize game
'''
# send selected games
def selected_games(inst,name):
    games = Game.filter_by_instance(inst,name)
    return games


def organize_game(players,round):
    existing_games = len(round.games_list)
    nb = len(players)
    games = []
    for i in range(existing_games*2,nb,2):
        game  = Game(
            round.id,
            players[i].id,
            players[i+1].id,
            )
        game.save()
        games.append(game)
    
    # Senging all the games of the round instead of half of them
    # In case we are restarting the game
    if existing_games != 0:
        games = selected_games('round_id',round.id)

    return games


def white_king(player, games, pname):
    for game in games:
        if player.id == game.white_king:
            return f"{pname} as white king"

        return f"{pname} as black king"


def sort_players_rnd2(players,old_games):
    finished_games =[]
    lst_players = []
    for game in old_games:
        gm = [game.player1, game.player2]
        finished_games.append(gm)

    players.sort(key=attrgetter('points'), reverse=True)

    for player in players:
        lst_players.append(player.id)

    combined_pl = combination_no_repeat(lst_players,finished_games)       
    new_pl_lst = [item for sublist in combined_pl for item in sublist]
    return new_pl_lst


def combination_no_repeat(players,used_comb):
    new_games = []
    for i in range(0,len(players),2):
        player1, player2 = sorted([players[i], players[i+1]])
        combination_key = tuple(player1), tuple(player2)
        if combination_key not in used_comb:
            new_games.append([player1, player2])

    return new_games


# givin games by round
def games_by_round(rnd_id):
    games_lst = []
    for game in Game.all_data():
        if game.round_id == rnd_id:
            games_lst.append(game)

    return games_lst


def add_results(result,game):
    # for i,game in enumerate(games):
    if game.res_p1 == None and game.res_p2 == None:
        if result == "1":
            game.set_winner(game.player1)
        elif result == "2":
            game.set_winner(game.player2)
        elif result == "3":
            game.set_winner("None")

        game.save(game.id)

    # closing hour round
    rd_id = game.round_id
    round = Round.from_db(rd_id)
    tour = Tournament.from_db(round.tournament_id)
    # tour.actual_round_number += 1
    # tour.save(str(tour.id))
    # round.ending_date_hour = today_str()
    # round.save(str(round.id))
    return game


# showing players contests for round
def round_players(games_by_round):
    players = []
    games = []
    for game in games_by_round:
        if None in game.player1_result and None in game.player2_result:
            id_p1 = game.player1
            id_p2 = game.player2
            playr1 = Player.from_db('id',id_p1)
            playr2 = Player.from_db('id',id_p2)
            players.append([playr1, playr2])
            games.append(game)

    return players, games


# convert game results to player instance points
def calculate_points(tour):
    rounds_id = tour.rounds_list
    games = []
    for round_id in rounds_id:
        games += selected_games('round_id', str(round_id))

    players = []
    for id in tour.players_list:
        count = 0.0
        for game in games:#Game.all_data():
            if id == game.player1:
                count += refact_if__game(game.player1_result[1])
                player = Player.from_db('id',id)
                player.points = count

            if id == game.player2:
                count += refact_if__game(game.player2_result[1])
                player = Player.from_db('id',id)
                player.points = count


        players.append(player)
        players.sort(key=attrgetter('points'), reverse=True)

    return players

#---------------------------------------
'''
Rapport
'''
from models.rapport import Rapport

def create_rapport():
    rapport = Rapport()
    return rapport
