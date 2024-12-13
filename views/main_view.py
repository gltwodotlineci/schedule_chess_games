from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_round
from views.choose_dt import send_dt_player
from views.choose_dt import verify_choice
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import choosed_tournament
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
    if choice == "2":
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
        show_all_tournaments()
        tour = select_tournament(all_tournaments())
        choosed_tournament(tour)
        #tour_select = select_tournaments(data)
        #print("Tour select >>> ", tour_select)
    elif choice1 == '2':
        print(" ")
        print("Lets create some Tournaments ! ")
        dt_tournament = send_dt_tourn()
        tour = create_tournament(dt_tournament)
        print(tour)

