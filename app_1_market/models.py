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
import numpy


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
            role = itertools.cycle([False, True])
            for p in self.get_players():
                p.role =next(role)
                p.participant.vars['role'] = p.role

        # loading valuiations:
        #seller_valuations = [7, 6, 5, 5, 4, 4, 3, 2, 1, 1]
        #buyer_valuations = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4]
        seller_valuations = itertools.cycle([7, 6, 5, 5, 4, 4, 3, 2, 1, 1])
        buyer_valuations = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])
        for p in self.get_players():
            if p.role == False:
                #p.seller_valuation = numpy.random.choice(seller_valuations, replace=False)
                p.seller_valuation = next(seller_valuations)
                p.participant.vars['seller_valuation'] = p.seller_valuation
            elif p.role == True:
                #p.buyer_valuation = numpy.random.choice(buyer_valuations, replace=False)
                p.buyer_valuation = next(buyer_valuations)
                p.participant.vars['buyer_valuation'] = p.buyer_valuation

        # loading packages:
        packages = [1, 2, 3, 4, 5]
        for p in self.get_players():
            if p.role == False:
                p.seller_package = numpy.random.choice(packages, replace=False)
                p.participant.vars['seller_package'] = p.seller_package


#        print("[[ APP_1_MARKET]] - PLAYER - CREATING_SESSION.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]")
#        print("[[ APP_1_MARKET]] - PLAYER - CREATING_SESSION.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]")
#        print("[[ APP_1_MARKET]] - PLAYER - CREATING_SESSION.............[[[ ROLE ==> ", self.participant.vars['role'], " <== ]]")
#        print("[[ APP_1_MARKET]] - PLAYER - CREATING_SESSION.............[[[ SELLER_VALUATION ==> ", self.participant.vars['seller_valuation'], " <== ]]")
#        print("[[ APP_1_MARKET]] - PLAYER - CREATING_SESSION.............[[[ BUYER_VALUATION ==> ", self.participant.vars['buyer_valuation'], " <== ]]")


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    role = models.BooleanField  # 0 = seller, 1 = buyer
    seller_valuation = models.IntegerField()
    buyer_valuation = models.IntegerField()
    seller_package = models.IntegerField()


