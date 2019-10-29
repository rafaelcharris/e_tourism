from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import itertools


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_1_market'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):

        # loading roles:
        if self.round_number == 1:
            role = itertools.cycle([0,1])
            for p in self.get_players():
                p.role =next(role)
                p.participant.vars['role'] = p.role


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    role = models.BooleanField  # 0 = buyer, 1 = seller


