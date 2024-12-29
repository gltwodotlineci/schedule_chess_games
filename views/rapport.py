from controller.controller import all_players
from controller.controller import all_tournaments
from controller.controller import tournament_players
from controller.controller import games_by_round
from controller.controller import calculate_points

from views.show import after_contest
from views.show import game_details


def games_str(rounds):
    rounds_lst = []
    for round in rounds:
        round_str =  f'<p><b> {round.name} starting {round.starting_date_hour} ending {round.ending_date_hour}</b></p>'
        # geting the games of each round
        intro = f"<p><b>The games of this round are: </b></p>"
        games = games_by_round(round.id)
        round_games = game_details(games)
        rounds_lst.append(round_str+intro+round_games)

    return ''.join(rounds_lst)


def create_html_rapport(rapport):
    players = all_players()
    tournaments = all_tournaments()
    tour_players = tournament_players(rapport.players_list)

    # Opening or creating a new html file
    f = open(f"raport {rapport.date_rapport}.html", 'w')
    html_template = f"""<html> 
    <head> 
    <title>Rapport</title> 
    </head> 
    <body style="text-align: center;"> 
    <h1>Tournament Rapport date {rapport.date_rapport}</h1>
    <h2>Welcome to the Tournament rapport page.</h2>
    <p><b>The list of all tournaments is</b></p>
    """ 
    html_template += ''.join([f'<p>{tour.name}</p>' for tour in tournaments])
    html_template += """
    
    <p><b>The list of all the players is</b></p>
    """ 
    html_template += ''.join([f'<p>{pl.first_name} {pl.last_name} {pl.fin}</p>' for pl in players])
    html_template += """
    <p><b>The list of the the selected tournament and the list of it's players is: </b></p>
    """ 
    html_template += f'<p>The tournament name <b>"{rapport.tour.name}"</b></p>'
    html_template += ''.join([f'<p>{pl.first_name} {pl.last_name} {pl.fin}</p>' for pl in tour_players])
    html_template += """
    <h3>The rounds details of the the tournament selected are: </h3>
    """
    html_template +=  games_str(rapport.rounds_lists)

    html_template += """
    <h3> The classement for this tournament is </h3>
    """
    # players_id = [x.id for x in tour_players]
    actual_players = calculate_points(rapport.tour)
    html_template +=  after_contest(actual_players)

    html_template += """

    </body> 
    </html> 
    """ 
    f.write(html_template) 
    f.close()
