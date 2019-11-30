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

    #Guardar los paquetes que los jugadores pueden comprar para mostrarles todas las opciones junto con la estrategia de compra
    buy_choices = []
    for i in range(1, players_per_group):
        choice = [i, 'Buy from seller {}'.format(i)]
        buy_choices.append(choice)

    packages = [i for i in range(1, 6)]

    seller_valuations = [7, 6, 5, 5, 4, 4, 3, 2, 1, 1]
    buyer_valuations = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4]

    com_practice = [i for i in range(1,5)]


class Subsession(BaseSubsession):
    def creating_session(self):
            if self.round_number == 1:
                    roles = itertools.cycle(['seller', 'buyer'])
                    for p in self.get_players():
                        p.participant.vars['role'] = next(roles)
                    #Esto le asigna a los jugadores desde la primera ronda el role de vededor o de comprador
    def assign_pac_val(self):
        #assign packages con replacement
        for p in self.get_players():
            if p.participant.vars['role'] == 'seller':
                p.seller_package = numpy.random.randint(1, 5)
                p.participant.vars['seller_package'] = p.seller_package
                p.seller_valuation = numpy.random.choice(Constants.seller_valuations, replace=False)
            else:
        # Assign valuations for each packaque for the sellers
        #Esta parte del código debería asignarle un valor random a cada valuación
                return {
                'packages_buyer': [
                    p.buyer_valuation_pac1, p.buyer_valuation_pac2, p.buyer_valuation_pac3,
                    p.buyer_valuation_pac4, p.buyer_valuation_pac5
                ],
                'valuations_packages': [numpy.random.choice(Constants.buyer_valuations, replace = False) for x in range(5)]
                }
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    def role(self):
        if self.participant.vars['role'] == 'buyer':
            return 'buyer'
        else:
            return 'seller'

    #Seller
    seller_package = models.IntegerField()
    seller_valuation = models.IntegerField()
    ask_price_ini = models.IntegerField()
    see_list = models.BooleanField(initial = False)
    com_practice = models.IntegerField(choices = [1, 2, 3, 4])
    ask_price_fin = models.IntegerField()

    #Buyer
    buyer_valuations_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()




