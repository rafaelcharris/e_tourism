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
from django.db import models as django_models
import itertools
import numpy
import collections


author = 'UEC'

doc = """
Markets
"""


class Constants(BaseConstants):
    name_in_url = 'app_4_informal'
    players_per_group = 4
    num_rounds = 5
    endowment = c(25)
    see_list_cost = c(1)

    packages = [i for i in range(1, 6)]

    cities =["Rome", "Vienna", "Paris", "Madrid", "Berlin"]

    seller_valuations = [70, 60, 50, 50, 40, 40, 30, 20, 10, 10]
    buyer_valuations = [100, 100, 90, 80, 80, 70, 60, 60, 50, 40]

    com_practice = [i for i in range(1,5)]
    report_price = c(1)
    report_penalty = c(2)

    instructions_template ='app_1_market_com_practices/instructions.html'

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
                    id_s = itertools.cycle([i for i in range(1, 11)])
                    p.seller_package = numpy.random.randint(1, 5)
                    p.participant.vars['seller_package'] = p.seller_package
                    p.seller_valuation = numpy.random.choice(Constants.seller_valuations, replace=False)
                    p.seller_id = next(id_s)
                    #todo have to fix this id. They don't work as I would like it to
                    p.participant.vars['seller_id'] = p.seller_id #assign a seller id

                else:
            # Assign valuations for each packaque for the sellers
            #Esta parte del código debería asignarle un valor random a cada paquete
                    random_package = numpy.random.choice(Constants.buyer_valuations, size = 5, replace = False)
                    p.participant.vars["valuations_package"] = dict(zip(Constants.packages, random_package))
                    p.participant.vars["valuations"] = dict(zip(zip(Constants.packages, Constants.cities), random_package))
                    #p.buyer_valuation_pac1 = p.participant.vars["valuations"].get(1)
                    #p.buyer_valuation_pac2 = p.participant.vars["valuations"].get(2)
                    #p.buyer_valuation_pac3 = p.participant.vars["valuations"].get(3)
                    #p.buyer_valuation_pac4 = p.participant.vars["valuations"].get(4)
                    #p.buyer_valuation_pac5 = p.participant.vars["valuations"].get(5)

                    id_b = itertools.cycle([i for i in range(1, 11)])
                #todo fix this id. They don't work as it should
                    p.participant.vars['buyer_id'] = next(id_b)



class Group(BaseGroup):

    penalty_bonus = models.IntegerField()

    def set_payoff(self):
        for p in self.get_players():
            if p.role() == "buyer":
                if p.my_seller > 0:
                    the_seller = self.get_player_by_id(p.my_seller)
                    the_seller.sold = True
                    p.package_purchased = the_seller.seller_package
                    p.paid = the_seller.ask_price_fin
                    p.payoff = p.participant.vars['valuations_package'].get(p.package_purchased) - p.paid - int(p.report)*Constants.report_price
                    print("VALUATION DEL PAQUETE: " + str(p.participant.vars['valuations_package'].get(p.package_purchased)))
                    p.payoff = p.payoff if p.payoff >= 0  else 0

                else: # En caso de que el vendedor sea cero, entonces dele paquete 0 y pago 0
                    p.package_purchased = 0
                    p.payoff = 0
            else:

                p.payoff = (p.ask_price_fin - p.seller_valuation - int(p.see_list)*Constants.see_list_cost)*int(p.sold)

    def who_purchased(self):
        sellers =[]
        for p in self.get_players():
            if p.role() == "buyer":
                if p.my_seller > 0:
                    the_seller = self.get_player_by_id(p.my_seller)
                    p.package_purchased = the_seller.seller_package
                    sellers.append(the_seller.id_in_group)
        print("LISTA DE SELLERS: " + str(sellers))
        if len(sellers) != len(set(sellers)): #si la length de ambas listas difiere, signiifca que hay algun repetido que set elimino (porque en los sets no puede haber repetidos)
            sellers_dic = dict(collections.Counter(sellers)) #todo creo que hay problema acá. no parece contar bien
            print("EL DICTIONARIO DE VENDEDORES ES: " + str(sellers_dic))

            for key, value in sellers_dic.items():
                if value > 1:
                    print("THIS WORKS: " + str(key))
                    buyers_time = {}
                    for p in self.get_players():
                        if p.role() == "buyer":
                            print("JUGADOR: " + str(p.id_in_group) + " PAQUETE: " + str(p.package_purchased) + " KEY: " + str(key))

                            if p.my_seller == key:
                                print("INFO: " + str(p.package_purchased) + "key: " + str(key))
                                buyers_time[p.id_in_group] = p.time_spent
                                print("DICTIONARY INSIDE LOOP: " + str(buyers_time))


                    print("DICTIONARY: " + str(buyers_time))
                    # after looping over all players I have here buyers and times
                    # get the one with tge less time
                    real_buyer = min(buyers_time, key = buyers_time.get)
                    for jugador in buyers_time.keys():
                        if jugador != real_buyer:
                            b = self.get_player_by_id(jugador)
                            b.package_purchased = 0
                            b.payoff = 0

    def drip_price(self):
        for p in self.get_players():
            p.drip = p.ask_price_fin - 1 if p.role() == "seller" else 0

    def get_times_reported(self):
        for p in self.get_players():
            if p.role() == "buyer":
                if p.report is True:
                    seller_rep = self.get_player_by_id(p.report_seller)
                    seller_rep.times_reported += 1

        for p in self.get_players():
            if p.role() == "seller":
                p.penalty = int(Constants.report_penalty) * int(p.times_reported) if p.times_reported > 3 else 0
                p.payoff -= p.penalty
                self.penalty_bonus = p.penalty//(Constants.players_per_group//2)

        if self.penalty_bonus > 0:
            for p in self.get_players():
                if p.role() == "buyer":
                    p.payoff += self.penalty_bonus


class Player(BasePlayer):

    def role(self):
        if self.participant.vars['role'] == 'buyer':
            return 'buyer'
        else:
            return 'seller'

    drip = models.IntegerField(initial = 0)


    #Seller
    seller_package = models.IntegerField(choices =
    [
        [0, "None"],
        [1, "Rome"],
        [2, "Vienna"],
        [3, "Paris"],
        [4, "Madrid"],
        [5, "Berlin"]

    ])
    seller_valuation = models.IntegerField()
    ask_price_ini = models.IntegerField()

    def ask_price_ini_min(self):
        return self.seller_valuation

    see_list = models.BooleanField(initial = False)
    com_practice = models.IntegerField(choices = [
        [1, "Best Price Guarantee"], [2,"Reference Pricing"], [3, "Drip Pricing"], [4, "None"]
    ])
    ask_price_fin = models.IntegerField()

    def ask_price_fin_min(self):
        return self.seller_valuation

    seller_id = models.IntegerField()
    sold = models.BooleanField(initial = False)
    times_reported = models.IntegerField(initial = 0)
    penalty = models.IntegerField()
    #Buyer
    #Preguntar a Felipe si puedo borrar estos campos de valuación de cada paquete
    buyer_valuation_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()

    buyer_packages = models.IntegerField(choices =
    [
        [0, "None"],
        [1, "Rome"],
        [2, "Vienna"],
        [3, "Paris"],
        [4, "Madrid"],
        [5, "Berlin"]
    ]
    )

    package_purchased = models.IntegerField( choices =
        [
            [0, "None"],
            [1, "Rome"],
            [2, "Vienna"],
            [3, "Paris"],
            [4, "Madrid"],
            [5, "Berlin"]
        ]
    )
    my_seller = models.IntegerField(initial = 0)
    paid = models.IntegerField(initial = 0)
    buyer_id = models.IntegerField()
    time_spent = models.FloatField()
    report = models.BooleanField()
    report_seller = models.IntegerField()