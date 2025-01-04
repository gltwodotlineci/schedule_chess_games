from controller.controller import all_players
from controller.controller import all_tournaments
from controller.controller import tournament_players
from controller.controller import games_by_round
from controller.controller import calculate_points

from views.show import ShowDetails


def games_str(rounds):
    rounds_lst = []
    for round in rounds:
        rnd_str = f'<p><b> {round.name} starting {round.starting_date_hour}'
        rnd_str += f' ending {round.ending_date_hour}</b></p>'
        # geting the games of each round
        intro = "<p><b>The games of this round are: </b></p>"
        games = games_by_round(round.id)
        round_games = ShowDetails.game_details(games)
        rounds_lst.append(rnd_str + intro + round_games)

    return ''.join(rounds_lst)


def create_html_report(report):
    players = all_players()
    tournaments = all_tournaments()
    tour_players = tournament_players(report.players_list)

    # Opening or creating a new html file
    f = open(f"raport {report.date_report}.html", 'w')
    html_template = f"""<html>
    <head>
    <title>Report</title>
    </head>
    <body style="text-align: center;">
    <h1>Tournament Report date {report.date_report}</h1>
    <h2>Welcome to the Tournament report page.</h2>
    <p><b>The list of all tournaments is</b></p>
    """
    html_template += ''.join([f'<p>{tour.name}</p>' for tour in tournaments])
    html_template += """

    <p><b>The list of all the players is</b></p>
    """
    x = ''
    for pl in players:
        x += f'<p>{pl.first_name} {pl.last_name} {pl.fin}</p>'

    html_template += x
    end_str = "<p><b>The list of the the selected tournament and "
    end_str += "the list of it's players is: </b></p>"
    html_template += end_str
    html_template += """
    """
    html_template += '<p>The tournament name <b>'
    html_template += f'"{report.tour.name}"</b></p>'

    y = ''
    for pl in tour_players:
        y += f'<p>{pl.first_name} {pl.last_name} {pl.fin}</p>'

    html_template += y
    html_template += """
    <h3>The rounds details of the the tournament selected are: </h3>
    """
    html_template += games_str(report.rounds_lists)

    html_template += """
    <h3> The classement for this tournament is </h3>
    """
    actual_players = calculate_points(report.tour)
    html_template += ShowDetails.after_contest(actual_players)

    html_template += """

    </body>
    </html>
    """
    f.write(html_template)
    f.close()
