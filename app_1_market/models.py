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

    buy_choices =[] #Tal vez me toca quitar esto
    packages = [i for i in range(1, 6)]

    seller_valuations = [7, 6, 5, 5, 4, 4, 3, 2, 1, 1]
    buyer_valuations = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4]

    com_practice = [i for i in range(1,5)]


class Subsession(BaseSubsession):

    def creating_session(self):
        #assign packages con replacement
        for p in self.group.get_players_by_role('seller'):
            p.seller_package = np.random.randint(1,5)
            p.participant.vars['seller_package'] = p.seller_package

        #Assign valuations. It is without replacement for sellers.
        for p in self.group.get_players_by_role('seller'):
            p.seller_valuation = np.random.choice(Constants.seller_valuations, replace = False)

        #Assign valuations for each packaque for the sellers
        for p in self.group.get_players_by_role('buyer'):
            for pac in Constants.packages:
                p.buyer_valuation[pac] = np.random.choice(Constants.buyer_valuations, replace = False)
                return dict(paquete = pac, valuation = p.buyer_valuation)
                #todo seria mejor crear in diccionario que relacione paquete y valuación.


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    #Definir los roles buyer o seller
    def role(self):
        if self.id_in_group % 2 ==0: # Si el id en el grupo es par asignele el role de buyer
            return 'buyer'
        else:
            return 'seller'


    agent_role = models.BooleanField()

    #Seller
    seller_package = models.IntegerField()
    seller_valuation = models.IntegerField()
    ask_price_ini = models.IntegerField()
    see_list = models.BooleanField(initial = 0)
    com_practice = models.IntegerField(choices = [1, 2, 3, 4])
    ask_price_fin = models.IntegerField()

    #Buyer
    buyer_valuations = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()




