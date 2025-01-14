from controller.controller import all_players
from controller.controller import all_tournaments
from controller.controller import check_last_tour


class ShowAll:
    @staticmethod
    def show_all_players():
        # Showing all the players and their details
        players = all_players()
        print("Playrs first name - last name - FED Id ")
        print("_______________________________________")
        for player in players:
            print(f"{player.first_name} {player.last_name}.  Id {player.fin}")
        print("_______________________________________")

    @staticmethod
    def show_all_tournaments():
        # Showing all the tournaments and their details
        tournaments = all_tournaments()
        state = "In progress... -> "
        if len(tournaments) > 0:
            print("Here you have the tournament names and their number. ")
            i = 1
            for tour in tournaments:
                if check_last_tour(tour)[0] is False:
                    state = "Uncompleted... -> "
                if tour.round_numbers == tour.actual_round_number:
                    state = "  -- Ended --  -> "

                print(f"{state} : {tour.name} - {i} ")
                i += 1
                state = "In progress... -> "
