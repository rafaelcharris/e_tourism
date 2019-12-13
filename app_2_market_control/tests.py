from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random, itertools


class PlayerBot(Bot):
    def play_round(self):
        sellers = itertools.cycle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        if self.player.round_number == 1:
            if self.player.role() == "seller":
                yield pages.instructions
                yield pages.instructions_2
                yield pages.seller, dict(ask_price_ini = 70, see_list = bool(random.randint(0 ,1)))
                yield pages.seller_2, dict(ask_price_fin = 70)
                yield pages.Results
            elif self.player.role() == "buyer":
                yield pages.instructions
                yield pages.instructions_2
                yield pages.buyer, dict(my_seller = next(sellers))
                yield pages.Results
        else:
            if self.player.role() == "seller":
                yield pages.instructions_2
                yield pages.seller, dict(ask_price_ini = 70, see_list = bool(random.randint(0 ,1)))
                yield pages.seller_2, dict(ask_price_fin = 70)
                yield pages.Results
            elif self.player.role() == "buyer":
                yield pages.instructions_2
                yield pages.buyer, dict(my_seller = next(sellers))
                yield pages.Results





#buyer
