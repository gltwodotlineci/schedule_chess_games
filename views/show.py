from models.player import Player
from controller.controller import white_king


class ShowDetails:
    @staticmethod
    def view_round_contest(data, games):
        print(" ")
        print("             The games are ")
        for i, pl in enumerate(data):
            p1 = f"{pl[0].first_name} {pl[0].last_name}"
            p2 = f"{pl[1].first_name} {pl[1].last_name}"
            p1_g = white_king(pl[0], games, p1)
            p2_g = white_king(pl[1], games, p2)
            print("______        <>  <>  <>       ______")
            print(f"                 Game {i+1}")
            print(f"{p1_g} vs {p2_g}")
        print(" ")

    @staticmethod
    def choosed_tournament(tournament):
        print(" ")
        print(f"You selected {tournament.name} at {tournament.place}")
        print(f"From {tournament.starting_date} to {tournament.ending_date}")
        if tournament.players_list == []:
            print("There are no players registred on this tournaments")
        else:
            print("The players registred of the turnament are: ")
            for pl_id in tournament.players_list:
                player = Player.from_db('id', pl_id)
                print(f"{player.first_name} {player.last_name} ")

        if tournament.rounds_list != []:
            print("The rounds for this turnament are.")
            for i in range(1, len(tournament.rounds_list)+1):
                print(f"Round {i}")

    @staticmethod
    def add_winner_instruct():
        print('__________________________________________')
        print("               Entering the results     ")
        print(" ")
        strt = "To enter the results you will be asked to choose between"
        strt += "the three posible cases"
        print(strt)
        instruct2 = "Write '1' if the player 1 won, '2' if the player 2"
        instruct2 += " won, and '3' if it's a draw."
        print(instruct2)
        print("   ")

    @staticmethod
    def after_contest(players):
        print(" ")
        results = "<p>"
        print("The players points after the game are")
        for pl in players:
            result = f"{pl.first_name} {pl.last_name} - {pl.points} points"
            print(result)
            results += result + "</p>"

        return results

    @staticmethod
    def game_details(games_list):
        results = ""
        for game in games_list:
            p1 = Player.from_db('id',game.player1)
            p2 = Player.from_db('id',game.player2)
            header = f"<p style='font-size: large;'>{p1.first_name} {p1.last_name}"
            header += f" against {p2.first_name} {p2.last_name}</p>"
            if game.res_p1 is None and game.res_p2 is None:
                result = "<p>The game is not played jet</p>"
            elif game.res_p1 is False:
                result = "<p>This game was draw </p>"
            elif game.res_p1 is True:
                result = '<p style="color: green;">'
                result += f'{p1.first_name} {p1.last_name} won the game</p>'
            elif game.res_p2 is True:
                result = f'<p style="color: green;">{p2.first_name}'
                result += f' {p2.last_name} won the game</p>'

            results += header + f"{result}"

        return results
