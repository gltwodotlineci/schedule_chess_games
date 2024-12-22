from views.choose_dt import verify_choice
from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_player
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import ask_add_player
from views.choose_dt import create_round_tour
from views.choose_dt import confirm_creation
from views.choose_dt import date_and_time
from views.choose_dt import choos_winner
from views.choose_dt import choos_fed_nb
from views.choose_dt import go_back
from views.show import after_contest

from views.show import view_round_contest
from views.show import add_winner_instruct
from views.show import choosed_tournament

from views.lists_values import show_all_tournaments
from views.lists_values import show_all_players

from controller.controller import all_tournaments
from controller.controller import list_tournaments_players
from controller.controller import create_tournament
from controller.controller import create_round
from controller.controller import create_player
from controller.controller import create_round
from controller.controller import order_players
from controller.controller import organize_game
from controller.controller import add_player2_tour
from controller.controller import games_by_round
from controller.controller import round_players
from controller.controller import add_results
from controller.controller import calculate_points
from controller.controller import sort_players_rnd2
from controller.controller import get_current_round
from controller.controller import selected_games


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
        else:
            return True
        # go back to main menue
        if go_back() == 'back':
            return True

    if choice1 == '2':
        print(" ")
        show_all_tournaments()
        tour = select_tournament(all_tournaments())
        choosed_tournament(tour)
        '''
        Organizing games by round.
        '''
        print("You can now start organzing the games or go back")
        content = "write 'yes' or 'back' "
        start_games = verify_choice(content,['yes','back'])
        if start_games == 'back':
            return True
        
        # get the courrent round
        while tour.actual_round_number < tour.round_numbers:
                
            round = get_current_round(tour)
            if tour.actual_round_number < 1:    
                sorted_players = order_players(tour.players_list,round1)
            else:
                games = selected_games('round_id',str(round.id))
                actual_players = calculate_points(tour.players_list)
                new_sorted_players_id = sort_players_rnd2(actual_players,games)
                sorted_players = order_players(new_sorted_players_id)

            games = organize_game(sorted_players, round)
            # adding list games to the round
            lst_games_id = [str(x.id) for x in games]
            round.games_list = lst_games_id
            round.save(str(round.id))
            # Geting round and creating games for round        
            round_games = games_by_round(str(round.id))
            players = round_players(round_games)
            view_round_contest(players)
            add_winner_instruct()
            winners = choos_winner(players)
            games = add_results(winners,round_games)
            # check the players points based on games results
            actual_players = calculate_points(tour.players_list)
            after_contest(actual_players)
            # Checking if all rounds have been played
            tour.actual_round_number
            print("If you want to continue or go back write 'c' or 'back'")
            content = "write 'c' or back "
            cont_back = verify_choice(content,['c','back'])
            if cont_back == 'back':
                break

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
        
        choice = create_round_tour(tour)
        if choice == 'back':
            return True

        # creating all the rounds
        existing_round = len(tour.rounds_list)
        needed_rounds = tour.round_numbers
        rounds = []
        for i in range(existing_round,needed_rounds):
            data = date_and_time(i)
            data['tournament_id'] = str(tour.id)
            rounds.append(create_round(data))
            ## If we want to stop creating rounds and start over
            ## latte... May be not a good solution
            # if i < needed_rounds-1:
            #     print(f"Do you want to continue to creat round {i+2}")
            #     content =" write 'yes' or 'stop' "
            #     stop_creating = verify_choice(content,['yes','stop'])
            #     if stop_creating == 'stop':
            #         break
        '''
        ordering the players from last name and creating games based on round
        adding the games on the round list field
        '''
        round1 = rounds[0]
        sorted_players = order_players(tour.players_list,round1=True)       
        games = organize_game(sorted_players, round1)
        # adding list games to the round
        lst_games_id = [str(x.id) for x in games]
        round1.games_list = lst_games_id
        round1.save(str(round1.id))

        print("Congratulation, You have created the {tour.name} tournament")
        verify_choice("write 'yes' to go to the main menue: ",['yes'])

#-------
