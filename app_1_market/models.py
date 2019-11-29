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
import numpy as np


author = 'UEC'

doc = """
Markets
"""


class Constants(BaseConstants):
    name_in_url = 'app_1_market'
    players_per_group = 10
    num_rounds = 5
    endowment = 3
    see_list_cost = 0.3

    buy_choices =[]


class Subsession(BaseSubsession):


    def creating_session(self):
        # loading packages:
        packages = [i for i in range(1, 6)]

        for p in self.get_players():
            if p.agent_role == False:
                p.seller_package = np.random.choice(packages,
                                                    replace=False)  # todo revisar si el replacement es en realidad True
                p.participant.vars['seller_package'] = p.seller_package

        for p in self.get_players():
            if p.agent_role == False:
                p.seller_package = np.random.choice(packages, replace=False) #todo revisar si el replacement es en realidad True
                p.participant.vars['seller_package'] = p.seller_package

        for i in range(1, Constants.players_per_group):
            choice = [i, 'Buy from seller {}'.format(i) + 'Package {}'.format(np.random.choice(packages))]
            Constants.buy_choices.append(choice)

        # loading valuations:
        seller_valuations = itertools.cycle([7, 6, 5, 5, 4, 4, 3, 2, 1, 1])
        buyer_valuations_pac1 = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])
        buyer_valuations_pac2 = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])
        buyer_valuations_pac3 = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])
        buyer_valuations_pac4 = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])
        buyer_valuations_pac5 = itertools.cycle([10, 10, 9, 8, 8, 7, 6, 6, 5, 4])

        for p in self.get_players():
            if p.agent_role == False:
                #p.seller_valuation = numpy.random.choice(seller_valuations, replace=False)
                p.seller_valuation = next(seller_valuations)
                p.participant.vars['seller_valuation'] = p.seller_valuation
            elif p.agent_role == True:
                #p.buyer_valuation = numpy.random.choice(buyer_valuations, replace=False)
                p.buyer_valuation_pac1 = next(buyer_valuations_pac1)
                p.buyer_valuation_pac2 = next(buyer_valuations_pac2)
                p.buyer_valuation_pac3 = next(buyer_valuations_pac3)
                p.buyer_valuation_pac4 = next(buyer_valuations_pac4)
                p.buyer_valuation_pac5 = next(buyer_valuations_pac5)
                p.participant.vars['buyer_valuation_pac1'] = p.buyer_valuation_pac1
                p.participant.vars['buyer_valuation_pac2'] = p.buyer_valuation_pac2
                p.participant.vars['buyer_valuation_pac3'] = p.buyer_valuation_pac3
                p.participant.vars['buyer_valuation_pac4'] = p.buyer_valuation_pac4
                p.participant.vars['buyer_valuation_pac5'] = p.buyer_valuation_pac5
        # loading packages:
        packages = [1, 2, 3, 4, 5]
        for p in self.get_players():
            if p.agent_role == False:
                p.seller_package = np.random.choice(packages, replace=False)
                p.participant.vars['seller_package'] = p.seller_package




class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def role(self):
        if self.id_in_group == Constants.players_per_group:
            return 'buyer'
        return 'seller {}'.format(self.id_in_group)


    agent_role = models.BooleanField()  # 0 = seller, 1 = buyer

    seller_package = models.IntegerField()
    seller_valuation = models.IntegerField()
    ask_price_ini = models.IntegerField()
    see_list = models.BooleanField()
    com_practice = models.IntegerField( choices = [1, 2, 3, 4])
    ask_price_fin = models.IntegerField()

    buyer_valuation_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()




