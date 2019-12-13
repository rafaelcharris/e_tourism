from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random, itertools

class PlayerBot(Bot):

    def play_round(self):
        yield pages.questionnaire_intro
        yield pages.questionnaire, dict(gender = random.randint(0, 2),
                                        age = random.randint (18, 70),
                                        country = "Utopia",
                                        education = random.randint (1, 6),
                                        civil_status = random.randint (1, 5),
                                        income = random.randint (1, 6),
                                        online_frequency = random.randint (1, 6),
                                        online_purchase = random.randint (0 ,1),
                                        )
