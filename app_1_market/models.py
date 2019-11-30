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
    players_per_group = 4
    num_rounds = 5
    endowment = 3
    see_list_cost = 0.3

    #Guardar los paquetes que los jugadores pueden comprar para mostrarles todas las opciones junto con la estrategia de compra
    #buy_choices = []
    #for i in range(1, players_per_group):
    #    choice = [i, 'Buy from seller {}'.format(i)]
    #    buy_choices.append(choice)

    packages = [i for i in range(1, 6)]

    seller_valuations = [7, 6, 5, 5, 4, 4, 3, 2, 1, 1]
    buyer_valuations = [10, 10, 9, 8, 8, 7, 6, 6, 5, 4]

    com_practice = [i for i in range(1,5)]

    instructions_template ='app_1_market/instructions.html'

class Subsession(BaseSubsession):
    def creating_session(self):
        #crear roles
            if self.round_number == 1:
                    roles = itertools.cycle(['seller', 'buyer'])
                    for p in self.get_players():
                        p.participant.vars['role'] = next(roles)

        #Esto le asigna a los jugadores desde la primera ronda el role de vededor o de comprador
        #assign packages con replacement
            for p in self.get_players():
                if p.participant.vars['role'] == 'seller':
                    p.seller_package = numpy.random.randint(1, 5)
                    p.participant.vars['seller_package'] = p.seller_package
                    p.seller_valuation = numpy.random.choice(Constants.seller_valuations, replace=False)
                    #todo Y si hago un diccionario relacionando valuation package y price final?!!!!
                else:
            # Assign valuations for each packaque for the sellers
            #Esta parte del código debería asignarle un valor random a cada paquete
                    p.participant.vars["valuations"] = dict(zip(Constants.packages, numpy.random.choice(Constants.buyer_valuations, size =5, replace = False)))
                    p.buyer_valuation_pac1 = p.participant.vars["valuations"].get(1)
                    p.buyer_valuation_pac2 = p.participant.vars["valuations"].get(2)
                    p.buyer_valuation_pac3 = p.participant.vars["valuations"].get(3)
                    p.buyer_valuation_pac4 = p.participant.vars["valuations"].get(4)
                    p.buyer_valuation_pac5 = p.participant.vars["valuations"].get(5)

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
    buyer_valuation_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()
    package_purchased = models.IntegerField()


