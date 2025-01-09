import datetime
import re
from models.player import Player
from models.round import Round
from models.tournament import Tournament


# validating the datas for the player creation
class ValidatePlayer(Player):
    def __init__(self, fin, first_name, last_name, birth_date):
        self._birth_date = birth_date
        super().__init__(fin, first_name, last_name, birth_date)

    def serialize_validator(self):
        return {
            'fin': self.fin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date
        }

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def fin(self):
        return self._fin

    @birth_date.setter
    def birth_date(self, val):
        try:
            datetime.datetime.strptime(val, "%d-%m-%Y")
            self._birth_date = val
        except ValueError:
            content_error = "Wrong date format, please"
            content_error += " retry with this format 'dd-mm-yyyy' "
            raise ValueError(content_error)

    @fin.setter
    def fin(self, nb):
        # regex
        if bool(re.match(r"^[A-Z]{2}\d{5}$", nb)) is False:
            content_error = "Wrong 'fin' format, please retray with"
            content_error += " the format 'AB12345' "
            raise ValueError(content_error)
        else:
            self._fin = nb


# validating the datas for the round creation
class ValidateRound(Round):
    def __init__(self, tournament_id, name, number, starting_date_hour):
        self._number = number
        self._starting_date_hour = starting_date_hour
        super().__init__(tournament_id, name, number, starting_date_hour)

    def serialize_validator(self):
        return {
            'tournament_id': self.tournament_id,
            'name': self.name,
            'number': self.number,
            'starting_date_hour': self.starting_date_hour,
        }

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, nb_val):
        if nb_val.is_integer():
            self._number = nb_val
        else:
            content_error = "Wrong number choise,"
            content_error += " Please be sure to choose a number "
            raise ValueError(content_error)

    @property
    def starting_date_hour(self):
        return self._starting_date_hour

    @starting_date_hour.setter
    def starting_date_hour(self, val):
        try:
            datetime.datetime.strptime(val, "%d-%m-%Y-%H:%M")
            self._starting_date_hour = val
        except ValueError:
            content_error = "Wrong date and hour format, please retry"
            content_error += " with this format, 'dd-mm-yyyy-HH:MM' "
            raise ValueError(content_error)


# validating the datas for the tournament creation
class ValidateTournament(Tournament):
    def __init__(
            self,
            name,
            place,
            starting_date,
            ending_date,
            description,
            nb_players,
            rounds_list=[],
            players_list=[],
            round_numbers=4,
            actual_round_number=0
    ):

        super().__init__(
            name,
            place,
            starting_date,
            ending_date,
            description,
            nb_players,
            rounds_list,
            players_list,
            round_numbers,
            actual_round_number
        )

        self._starting_date = starting_date
        self._ending_date = ending_date

    def serialize_validator(self):
        return {
            'name': self.name,
            'place': self.place,
            'starting_date': self.starting_date,
            'ending_date': self.ending_date,
            'description': self.description,
            'nb_players': self.nb_players,
        }

    @property
    def starting_date(self):
        return self._starting_date

    @property
    def ending_date(self):
        return self._ending_date

    @property
    def nb_players(self):
        return self._nb_players

    @starting_date.setter
    def starting_date(self, val):
        try:
            datetime.datetime.strptime(val, "%d-%m-%Y")
            self._starting_date = val
        except ValueError:
            content_error = "Wrong date format, please retry"
            content_error += " with this format 'dd-mm-yyyy' "
            raise ValueError(content_error)

    @ending_date.setter
    def ending_date(self, val):
        try:
            datetime.datetime.strptime(val, "%d-%m-%Y")
            self._ending_date = val
        except ValueError:
            error_content = "Wrong date format, please retry"
            error_content += " with this format 'dd-mm-yyyy' "
            raise ValueError(error_content)

    @nb_players.setter
    def nb_players(self, nb):
        if int(nb) % 2 != 0 or nb.isnumeric() is False:
            error_content = "Error, the number of"
            error_content += " players must be an even number "
            raise ValueError(error_content)
        else:
            self._nb_players = nb
