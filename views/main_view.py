from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_round
from views.choose_dt import send_dt_player
from views.choose_dt import verify_choice
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import select_round
from views.choose_dt import select_player4_tour
from views.choose_dt import ask_add_player

from views.lists_values import show_all_tournaments
from views.lists_values import show_all_games
from views.lists_values import show_all_players
from views.lists_values import show_all_rounds

from controller.controller import all_players
from controller.controller import all_games
from controller.controller import all_rounds
from controller.controller import all_tournaments
from controller.controller import list_tournaments_players
from controller.controller import create_tournament
from controller.controller import create_round
from controller.controller import create_player
from controller.controller import add_round_2_tour
from controller.controller import edit_tournament

from views.create_veiw import ask_dt_tournament



def create_game():
    pass


def welcom_header(data):
    print("--- WELCOME TO THE CHESS GAME APPLICATION! ---")
    print(f"You have registred {len(data['tournaments'])} tournements")
    print(f"You alsow have {len(data['players'])} players")
    print('                ')
    #show_all_tournemnts(data.get('tournaments'))


# giving data for round
def data_for_round():
    print("Here you have the list of the round names")
    print("and a number at the side of each name: ")
        
    for i in range(1,11):
        print(f" Round {i} - {i}")
        x += i
    
    round_nb =verify_choice(
        "Your round number is? ",
        [str(x) for x in range(1,11)]
        )

    print(f'you choosed Round {round_nb}')
    return round_nb

def welcome_pg_bis():
    welcom_header(list_tournaments_players())
    show_all_tournaments(all_tournaments())
    choice = select_or_create()
    return choice


def select_tournaments(data):
    print("  ")
    if len(data) > 0:
        print("Here you have the tournement names and their number. ")
        i = 1
        for tour in data:
            print(f"{tour.get('name')} - {i}")
            i += 1

        tour = select_tournament(data)
        print(' ')
        print(f"You selected {tour.get('name')} at {tour.get('place')}")
        print(f"From {tour.get('starting_date')} to {tour.get('ending_date')}")
        
        if tour.get('players_list') == []:
            print("There are no players registred on this tournaments")
        else:
            print("The players registred at this turnament are: ")
            for pl in tour.get('players_list'):
                print(pl)
        
        tour_id = tour.get('id')
        if len(tour.get('rounds_list')) == 0:
            print(" The tournament you choosed has 0 rounds")
            round_nb = tour.get('round_numbers')
            print(f"This tournament is expected to have {round_nb} rounds")
            print("If you want to create the rounds for this tournament")
            confirm_select = input("Write 'yes' to cnfirm or anything else if not: ")
            return confirm_select, tour_id
        else:
            return 'no', tour_id


def create_round_from_tour(tour):
    if isinstance(tour,str):
        tour_id = tour
    else:
        tour_id = tour.id
    round_nbs = 4 #tour.round_numbers
    print("You can choose the round number to create a round")
    for x in range(1,round_nbs+1):
        round_nb = send_dt_round(x)
        round = create_round(round_nb, tour_id)
        add_round_2_tour(round)
        contin = input('write "continu" ')
        if contin != "continue":
            return "menu principale"
        if x < round_nbs:    
            stop = input("Write 'stop' if you want to stop or write anything if you want to continue ")
            if stop.lower() == 'stop':
                break
        else:
            print("You created the last round for this tournament")


def mock_show():
    
    # show_all_games(all_games())
    # show_all_rounds(all_rounds())
    choice = welcome_pg_bis()
    data = all_tournaments()
    if choice == "1":    
        tour_select = select_tournaments(data)

        if tour_select[0] == 'yes':
            create_round_from_tour(tour_select[1])

        # else:
        #     print("Do you want to start a game round? ")
        # list_players = select_player4_tour(all_players())
        # edit_tournament(tour_select[1],'players_list',list_players )
    elif choice == "2":
        dt_tournament = send_dt_tourn()
        tour = create_tournament(dt_tournament)
        print(tour)
        create_round_from_tour(tour)
        # player = create_player4_tour()
        list_players = select_player4_tour(all_players())
        edit_tournament(tour.id,'players_list',list_players)

    elif choice == '3':
        pass


def main_page():
    welcom_header(list_tournaments_players())
    print(" -*-*-*-  -*-*-*- -*-*-*- -*-*-*-")
    choice1 = select_or_create()
    data = all_tournaments()
    if choice1 == '0':
        print(" ")
        print("     Your Players Are:")
        show_all_players()
        add_player = ask_add_player()
        if add_player == 'yes':
            player = send_dt_player()
            create_player(player)

    if choice1 == '1':
        print(" ")
        tour_select = select_tournaments(data)
    elif choice1 == '2':
        print(" ")
        print("Lets create some Tournaments ! ")

