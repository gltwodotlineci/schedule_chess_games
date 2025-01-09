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
    '''
    Will create a round object and update it's id in tournament's rounds_list
    also saving the new round and updating tournament on theri json data
    :param data: dictionary
    :return: round object
    '''
    round = support_create(ValidateRound, Round, data, 'round')
    # adding round id to Tournament
    tournament = Tournament.from_db(round.tournament_id)
    tournament.rounds_list.append(str(round.id))
    tournament.update(str(tournament.id))
    round.save()
    return round


# Get the current round
def get_current_round(tour):
    '''
    Choose the round based on it's tour_id foreign key
    :param tour: tour object
    :return: round object updated
    '''
    current_round = tour.actual_round_number
    round_id = tour.rounds_list[current_round]
    return Round.from_db(round_id)


# Get the passed round
def get_passed_round(tour):
    '''
    Choose the n-1 round based on its given tour_id foreign key
    :param tour: tour object
    :return: round object updated
    '''
    passed_round = tour.actual_round_number - 1
    round_id = tour.rounds_list[passed_round]
    return Round.from_db(round_id)


'''
Tournement,
create ans serialize tournement
'''


def create_tournament(data):
    '''
    Will create a tournament object and save it on its json data
    :param data: dictionary
    :return: tournament object
    '''
    tournament = support_create(
        ValidateTournament,
        Tournament,
        data,
        'tournament'
    )
    tournament.save()
    return tournament


def all_tournaments():
    # Sending the list of all tournaments objects
    tours = Tournament.all_data()
    return tours


def edit_tour_round(round):
    '''
    Updating the round and tournament object and saving them to their
    respectiv json data
    :param round: tour object
    :return: tournament object updated
    '''
    tour = Tournament.from_db(round.tournament_id)
    tour.actual_round_number += 1
    tour.update(str(tour.id))
    round.ending_date_hour = today_str()
    round.update(str(round.id))

    return tour


# Checking if the last tournamented created has all the players or rounds
def check_last_tour(tour=None):
    ''''
    Checking the state of a given/last tournament if all their players are
    associeted and if all their rounds are created
    :param tour: None or tour object
    :return: False if the given/last tournament is uncomplate and the missing
    rounds or players. False if the given/last tournament is completed
    '''
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
    '''
    Will create a player object and save it in its json data file
    :param data: dictionary
    :return: player object
    '''
    player = support_create(ValidatePlayer, Player, data, 'player')
    player.save()
    return player


# List of all players
def all_players():
    # Sending the list of all players objects
    all_players = Player.all_data()
    all_players.sort(key=attrgetter('last_name'))
    return all_players


# List of players from a tournament
def tournament_players(players):
    '''
    Giving the list playes in alphabetic order
    :param players: list (with player objects)
    :return: list populated with player objects
    '''
    tour_players_lst = players
    tour_players_lst.sort(key=attrgetter('last_name'))
    return tour_players_lst


# Check if fin exists
def check_fin(data):
    '''
    Avoiding to create a double in data base
    :param data: string (fin number)
    :return: True if the player allredy exist on DB, False if not
    '''
    for fin in Player.all_data():
        if fin.fin == data:
            return True

    return False


# In this case
def enter_existing_player(fed_id, tour):
    '''
    Checking the fin allredy exist on the tournament
    :param data: string (fin number)
    :return: True if fin exist in the tournament. False if it doesn't
    '''
    for player_id in tour.players_list:
        player = Player.from_db('id', player_id)
        if player.fin == fed_id:
            return True

    return False


# Selecting player from it's last name
def order_players(players_id, round1=False):
    '''
    ordering the list of players in alphabet order
    :param players_id: uuid
    :param round1: integer/False
    :return: list of player objects
    '''
    lst_players = []
    for pl_id in players_id:
        player = Player.from_db('id', pl_id)
        lst_players.append(player)

    # Ordering the players from last name
    if round1:
        lst_players.sort(key=attrgetter('last_name'))
    return lst_players


def add_player2_tour(tour, fed_id):
    '''
    Adding players from db to the tournament
    :param tour: tour object
    :param fed_id: string (fin)
    Updating tournament playrs list with player's uuid
    '''
    pl = Player.from_db('fin', fed_id)
    tour.players_list.append(pl.id)

    tour.update(str(tour.id))


def refact_if__game(player_result):
    # refactoring the player point calculation
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
    '''
    Filter games that have a cummon round id
    :param inst: string (round_id)
    :param name: uuid
    :return: list of games objects
    '''
    games = Game.filter_by_instance(inst, name)
    return games


def organize_game(players, round):
    '''
    Organizing games and checking if some round games
    are cut in the midle. Saving new games
    :param players: list
    :param round: round object
    :return: list of games object
    '''
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
    '''
    Determine randomly witch player will be the white or the black king
    :param player: player object
    :param games: list of games object
    :pname: string
    :return: player frist and last name and if he is white/black king
    '''
    for game in games:
        if player.id == game.white_king:
            return f"{pname} as white king"

        return f"{pname} as black king"


def new_game_players(p, passed_games):
    '''
    ordering new game players based on their points and avoiding repetition
    :parametre p: player object
    :passed_games: list with passed games objects
    :return: list of players ordering by their points
    '''
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
    '''
    Adding resul in game updating the results on db
    :param result: string number
    :param game: game object
    :return: updated game object
    '''
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
    '''
    Calculate points of player int tournemant that he had participated
    :param: tournament object
    :return: list of players in classement oder
    '''
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
    # creating report and returning it
    return Report()


def check_games(rounds_id_list):
    '''
    Checking if the first round has alredy all its games created
    :param rounds_id_list: list with uuid
    :return: True if it allredy have games created, False if not
    '''
    all_games = []
    for round_id in rounds_id_list:
        all_games += games_by_round(round_id)

    if all_games == []:
        return False

    return True
