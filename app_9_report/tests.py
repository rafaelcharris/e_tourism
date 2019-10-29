from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield pages.the_end, dict(e_mail=str(random.randint(1, 100)) + "@unal.edu.co")
