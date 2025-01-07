from datetime import datetime
from operator import attrgetter

from models.player import Player
from models.round import Round
from models.tournament import Tournament
from models.game import Game
from models.report import Report

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
    tournament.update(str(tournament.id))
    round.save()
    return round


# Get the current round
def get_current_round(tour):
    current_round = tour.actual_round_number
    round_id = tour.rounds_list[current_round]
    return Round.from_db(round_id)


# Get the passed round
def get_passed_round(tour):
    passed_round = tour.actual_round_number - 1
    round_id = tour.rounds_list[passed_round]
    return Round.from_db(round_id)


'''
Tournement,
create ans serialize tournement
'''


def create_tournament(data):
    tournament = support_create(
        ValidateTournament,
        Tournament,
        data,
        'tournament'
    )
    tournament.save()
    return tournament


def all_tournaments():
    tours = Tournament.all_data()
    return tours


def edit_tour_round(round):
    tour = Tournament.from_db(round.tournament_id)
    tour.actual_round_number += 1
    tour.update(str(tour.id))
    round.ending_date_hour = today_str()
    round.update(str(round.id))

    return tour


# Checking if the last tournamented created has all the players or rounds
def check_last_tour(tour=None):
    if tour:
        last_tour = tour
    else:
        last_tour = Tournament.last_tour()
        if last_tour is False:
            return False, None, None, None

    missing_players = int(last_tour.nb_players) - len(last_tour.players_list)
    missing_rounds = last_tour.round_numbers - len(last_tour.rounds_list)
    if missing_players > 0 or missing_rounds > 0:
        return False, last_tour, missing_players, missing_rounds

    return True, last_tour, missing_players, missing_rounds


'''
Players part:
'''


# Create player
def create_player(data):
    player = support_create(ValidatePlayer, Player, data, 'player')
    player.save()
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


# Check if fin exists
def check_fin(data):
    for fin in Player.all_data():
        if fin.fin == data:
            return True

    return False


def enter_existing_player(fed_id, tour):
    for player_id in tour.players_list:
        player = Player.from_db('id', player_id)
        if player.fin == fed_id:
            return True

    return False


# Selecting player from it's last name
def order_players(players_id, round1=False):
    lst_players = []
    for pl_id in players_id:
        player = Player.from_db('id', pl_id)
        lst_players.append(player)

    # Ordering the players from last name
    if round1:
        lst_players.sort(key=attrgetter('last_name'))
    return lst_players


# Add multiple players
def add_player2_tour(tour, fed_id):
    pl = Player.from_db('fin', fed_id)
    tour.players_list.append(pl.id)

    tour.update(str(tour.id))


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


# Send selected games
def selected_games(inst, name):
    games = Game.filter_by_instance(inst, name)
    return games


def organize_game(players, round):
    existing_games = len(round.games_list)
    nb = len(players)
    games = []
    for i in range(existing_games*2, nb, 2):
        game = Game(
            round.id,
            players[i].id,
            players[i+1].id,
        )
        game.save()
        games.append(game)

    # Sending all the games of the round instead of half of them
    # In case we are restarting the game
    if existing_games != 0:
        games = selected_games('round_id', round.id)

    return games


def white_king(player, games, pname):
    for game in games:
        if player.id == game.white_king:
            return f"{pname} as white king"

        return f"{pname} as black king"


def new_game_players(p, passed_games):
    old = []
    usd = []
    new_g = []

    for game in passed_games:
        old.append([game.player1, game.player2])

    for x in p:
        for i in range(0, len(p)):
            if x.id not in usd and p[i].id not in usd and x.id != p[i].id:
                if [x.id, p[i].id] not in old and [p[i].id, x.id] not in old:
                    new_g.append([x.id, p[i].id])
                    usd.append(x.id)
                    usd.append(p[i].id)

    # In case is impossible to avoid two players to play again
    if len(new_g) < len(old):
        pn = p[len(new_g)*2]
        pn_2 = p[len(new_g)*2+1]
        new_g.append([pn.id, pn_2.id])

    new_pl_lst = [item for sublist in new_g for item in sublist]
    return new_pl_lst


# Givin games by round
def games_by_round(rnd_id):
    games_lst = []
    for game in Game.all_data():
        if game.round_id == rnd_id:
            games_lst.append(game)

    return games_lst


def add_results(result, game):
    if game.res_p1 is None and game.res_p2 is None:
        if result == "1":
            game.set_winner(game.player1)
        elif result == "2":
            game.set_winner(game.player2)
        elif result == "3":
            game.set_winner("None")

        game.update(game.id)

    return game


# Showing players contests for round
def round_players(games_by_round):
    players = []
    games = []
    for game in games_by_round:
        if None in game.player1_result and None in game.player2_result:
            id_p1 = game.player1
            id_p2 = game.player2
            playr1 = Player.from_db('id', id_p1)
            playr2 = Player.from_db('id', id_p2)
            players.append([playr1, playr2])
            games.append(game)

    return players, games


# Convert game results to player instance points
def calculate_points(tour):
    rounds_id = tour.rounds_list
    games = []
    for round_id in rounds_id:
        games += selected_games('round_id', str(round_id))

    players = []
    for id in tour.players_list:
        count = 0.0
        for game in games:
            if id == game.player1:
                count += refact_if__game(game.player1_result[1])
                player = Player.from_db('id', id)
                player.points = count

            if id == game.player2:
                count += refact_if__game(game.player2_result[1])
                player = Player.from_db('id', id)
                player.points = count

        players.append(player)
        players.sort(key=attrgetter('points'), reverse=True)

    return players


# Report
def create_report():
    return Report()


def check_games(rounds_id_list):
    all_games = []
    for round_id in rounds_id_list:
        all_games += games_by_round(round_id)

    if all_games == []:
        return False

    return True
