from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_player
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import choosed_tournament
from views.choose_dt import ask_add_player
from views.choose_dt import create_round_4new_tour
from views.choose_dt import confirm_creation
from views.choose_dt import date_and_time

from views.lists_values import show_all_tournaments
from views.lists_values import show_all_players

from controller.controller import all_tournaments
from controller.controller import list_tournaments_players
from controller.controller import create_tournament
from controller.controller import create_round
from controller.controller import create_player
from controller.controller import add_round_2_tour
from controller.controller import create_round
from controller.controller import order_players
from controller.controller import add_players2_tour


def welcom_header(data):
    print("--- WELCOME TO THE CHESS GAME APPLICATION! ---")
    print(f"You have registred {len(data['tournaments'])} tournements")
    print(f"You alsow have {len(data['players'])} players")
    print('                ')


def create_round_from_tour(tour):
    if isinstance(tour,str):
        tour_id = tour
    else:
        tour_id = tour.id
    round_nbs = 4 #tour.round_numbers
    print("You can choose the round number to create a round")
    for x in range(1,round_nbs+1):
        round_nb = "replaced dt"# send_dt_round(x)
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


#---------------- Round Test part



#------------------


def main_page():
    welcom_header(list_tournaments_players())
    print(" -*-*-*-  -*-*-*- -*-*-*- -*-*-*-")
    choice1 = select_or_create()
    if choice1 == '1':
        print(" ")
        print("     Your Players Are:")
        show_all_players()
        add_player = ask_add_player()
        if add_player == 'yes':
            player = send_dt_player()
            create_player(player)
    if choice1 == '2':
        print(" ")
        show_all_tournaments()
        tour = select_tournament(all_tournaments())
        choosed_tournament(tour)
    elif choice1 == '3':
        print(" ")
        # print("Lets create some Tournaments ! ")
        # dt_tournament = send_dt_tourn()
        # tour = create_tournament(dt_tournament)
        # print(" ")
        # print("From the next player list you can choose the players for this tournament")
        # print("The number of players must be even. ")
        # print(" ")
        # show_all_players()
        # print("_________________")
        # add_players2_tour(tour)
        # print(" ")
        choice = create_round_4new_tour()
        if choice == 'back':
            return True
        from models.tournament import Tournament
        tour = Tournament.from_db("150Cartier_Goyave")
        existing_round = len(tour.rounds_list)
        # choice = confirm_creation(existing_round)
        # if choice == 'back':
        #     return True
        # data = date_and_time(existing_round)
        # round = create_round(data)
        
        sorted_players = order_players(tour.players_list)       
        from controller.controller import organize_game
        games = organize_game(sorted_players)
        for game in games:
            print(f"{game[0].first_name} {game[0].last_name} VS {game[1].first_name} {game[1].last_name}")

        input("buliding rounds part")
