from controller.controller import all_players
from controller.controller import all_tournaments

def show_all_tournaments(dt):
    print("Here you have the names of the tournements")
    print("the starting and ending date")
    for tour in dt:
        print(f"{tour.get('name')} in {tour.get('place')}")
        print(f"From {tour.get('starting_date')} to {tour.get('ending_date')}")
        if tour.get('rounds_list') == []:
            print("The tournament has no rounds jet")
        else:
            print("The rounds of this tournament are: ")
            for round in tour.get('rounds_list'):
                print(round)


def show_all_players():
    players = all_players()
    print("The first name and the last name of the players")
    for player in players:
        print(f"Player Name: {player.first_name} {player.last_name}")


def show_all_rounds(dt):
    print("Here you have the name of the existing round")
    print("You have alsow the id of the Tournement")
    for round in dt:
        print(round.get('name'))
        print(round.get('tournament_id'))


def show_all_games(dt):
    print("You have here the list of games")
    for game in dt:
        print(game)
