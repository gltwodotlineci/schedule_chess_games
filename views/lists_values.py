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
    print("Playrs first name - last name - FED Id ")
    print("_______________________________________")
    for player in players:
        print(f"{player.first_name} {player.last_name}.  Id {player.fin}")

    print("_______________________________________")


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

from controller.controller import check_last_tour
def show_all_tournaments():
    tournaments = all_tournaments()
    state = "In progress... -> "
    if len(tournaments) > 0:
        print("Here you have the tournement names and their number. ")
        i = 1
        for tour in tournaments:
            if check_last_tour(tour)[0] is False:
                state = "Incompleted... -> "
            if tour.round_numbers == tour.actual_round_number:
                state = "  -- Ended --  -> "

            print(f"{state} : {tour.name} - {i} ")
            i += 1
            state = "In progress... -> "
