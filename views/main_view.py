from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_player
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.show import choosed_tournament
from views.choose_dt import ask_add_player
from views.choose_dt import create_round_4new_tour
from views.choose_dt import confirm_creation
from views.choose_dt import date_and_time
from views.choose_dt import choos_winner
from views.choose_dt import choos_fed_nb

from views.show import view_round_contest
from views.show import add_winner_instruct

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
from controller.controller import organize_game
from controller.controller import add_player2_tour
from controller.controller import games_by_round
from controller.controller import show_challanges
from controller.controller import add_results
from controller.controller import add_points_to_players


def welcom_header(data):
    print("--- WELCOME TO THE CHESS GAME APPLICATION! ---")
    print(f"You have registred {len(data['tournaments'])} tournements")
    print(f"You alsow have {len(data['players'])} players")
    print('                ')



#---------------- Test part


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
        # Geting round and creating games for round        
        first_round = tour.rounds_list[0]
        raunds_games = games_by_round(first_round)
        players = show_challanges(raunds_games)
        view_round_contest(players)
        add_winner_instruct()
        winners = choos_winner(players)
        games_res = add_results(winners,raunds_games)
        add_points_to_players(games_res)
        #Round 2
        choosed_tournament(tour, True)
        print("     ")
        print("Now you can pass to round two ")       
    elif choice1 == '3':
        print(" ")
        print("Lets create some Tournaments ! ")
        dt_tournament = send_dt_tourn()
        tour = create_tournament(dt_tournament)
        print(" ")
        print("From the next player list you can choose the players for this tournament")
        print("The number of players must be even. ")
        print(" ")
        show_all_players()
        print("_________________")

        nb_players = int(tour.nb_players)
        print("Exemple of the FED Id nb 'AB12345' ")
        for i in range(1,nb_players+1):
            add_player2_tour(tour,choos_fed_nb(tour,i))
        
        print(" ")
        
        choice = create_round_4new_tour()
        if choice == 'back':
            return True
        existing_round = len(tour.rounds_list)
        choice = confirm_creation(existing_round)
        if choice == 'back':
            return True
        data = date_and_time(existing_round)
        data['tournament_id'] = tour.id
        round = create_round(data)
        '''
        ordering the players from last name and creating games based on round
        adding the games on the round list field
        '''
        sorted_players = order_players(tour.players_list)       
        games = organize_game(sorted_players, round)
        # adding list games to the round
        lst_games_id = [x.id for x in games]
        round.games_list = lst_games_id
        round.save(round.id)
        input("Write anything if you want to go back ")

#-------
