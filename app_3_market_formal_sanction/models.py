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
import collections
import random


author = 'UEC'

doc = """
Markets
"""


class Constants(BaseConstants):
    name_in_url = 'app_3_formal_sanction'
    players_per_group = 20
    num_rounds = 5
    endowment = 25
    see_list_cost = 1
    prob_audit = 0.2
    punishment = 20
    packages = [i for i in range(1, 6)]
    reference_20 = 20

    cities =["Rome", "Vienna", "Paris", "Madrid", "Berlin"]

    seller_valuations = [70, 60, 50, 50, 40, 40, 30, 20, 10, 10]
    buyer_valuations = [100, 100, 90, 80, 80, 70, 60, 60, 50, 40]

    com_practice = [i for i in range(1,5)]

    instructions_template ='app_3_market_formal_sanction/instructions.html'

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
                    p.buyer_valuation_pac1 = p.participant.vars["valuations_package"].get(1)
                    p.buyer_valuation_pac2 = p.participant.vars["valuations_package"].get(2)
                    p.buyer_valuation_pac3 = p.participant.vars["valuations_package"].get(3)
                    p.buyer_valuation_pac4 = p.participant.vars["valuations_package"].get(4)
                    p.buyer_valuation_pac5 = p.participant.vars["valuations_package"].get(5)

                    id_b = itertools.cycle([i for i in range(1, 11)])
                #todo fix this id. They don't work as it should
                    p.participant.vars['buyer_id'] = next(id_b)



class Group(BaseGroup):

    def set_payoff(self):
        for p in self.get_players():
            if p.role() == "buyer":
                if p.my_seller > 0:
                    the_seller = self.get_player_by_id(p.my_seller)
                    the_seller.my_buyer = p.id_in_group
                    p.package_purchased = the_seller.seller_package
                    p.paid = the_seller.ask_price_fin
                    p.payoff = int(Constants.endowment)
                    p.payoff += int(p.participant.vars['valuations_package'].get(p.package_purchased) - p.paid) if p.participant.vars['valuations_package'].get(p.package_purchased) - p.paid > 0 else 0
                    p.package_purchased = p.package_purchased if p.participant.vars['valuations_package'].get(p.package_purchased) - p.paid > 0 else 0
                    the_seller.sold = True if p.package_purchased > 0 else False
                else: # En caso de que el vendedor sea cero, entonces dele paquete 0 y pago 0
                        p.package_purchased = 0
                        p.payoff = int(Constants.endowment)
            else:
                p.payoff = int(Constants.endowment)
                p.payoff += int((p.ask_price_fin - p.seller_valuation)*int(p.sold) - int(p.see_list)*Constants.see_list_cost - int(p.bad_practice)*Constants.punishment)

    def who_purchased(self):
        sellers =[]
        for p in self.get_players():
            if p.role() == "buyer":
                if p.my_seller > 0:
                    the_seller = self.get_player_by_id(p.my_seller)
                    p.package_purchased = the_seller.seller_package
                    sellers.append(the_seller.id_in_group)

        if len(sellers) != len(set(sellers)): #si la length de ambas listas difiere, signiifca que hay algun repetido que set elimino (porque en los sets no puede haber repetidos)
            sellers_dic = dict(collections.Counter(sellers))
            #print("EL DICTIONARIO DE VENDEDORES ES: " + str(sellers_dic))

            for key, value in sellers_dic.items():
                if value > 1:
                    #print("THIS WORKS: " + str(key))
                    buyers_time = {}
                    for p in self.get_players():
                        if p.role() == "buyer":
                            #print("JUGADOR: " + str(p.id_in_group) + " PAQUETE: " + str(p.package_purchased) + " KEY: " + str(key))

                            if p.my_seller == key:
                                #print("INFO: " + str(p.package_purchased) + "key: " + str(key))
                                buyers_time[p.id_in_group] = p.time_spent
                                #print("DICTIONARY INSIDE LOOP: " + str(buyers_time))


                    #print("DICTIONARY: " + str(buyers_time))
                    # after looping over all players I have here buyers and times
                    # get the one with tge less time
                    real_buyer = min(buyers_time, key = buyers_time.get)
                    for jugador in buyers_time.keys():
                        if jugador != real_buyer:
                            b = self.get_player_by_id(jugador)
                            b.package_purchased = 0
                            b.payoff = int(Constants.endowment)

    def drip_price(self):
        for p in self.get_players():
            p.drip = p.ask_price_fin - 1 if p.role() == "seller" else 0

    def ref_20(self):
        for p in self.get_players():
            p.discount = 0
            p.discount = (p.ask_price_ini - p.ask_price_fin) if p.role() == "seller" and p.ask_price_ini > p.ask_price_fin else 0
            p.ref20 = p.ask_price_fin + p.discount + Constants.reference_20 if p.role() == "seller" else 0

    def audit(self):
        prices = []

        for p in self.get_players():
            if p.role() == "seller":
                prices.append(p.ask_price_fin)
        # esta función debería prenderse un 20% de las veces para hacer un audit

        if numpy.random.uniform(0, 1) <= Constants.prob_audit:

            for p in self.get_players():
                if p.role() == "seller":
                    p.audited = True
                    if p.com_practice == 1:
                        p.bad_practice = p.ask_price_fin > min(prices) #esto es para todos los paquetes.
                    elif p.com_practice == 3:
                        p.bad_practice = True
                    elif p.com_practice == 4 and p.see_list is False:  # p.comm_practice == 3:
                        p.bad_practice = True



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
        [1, "Best Price Guarantee"], [2,"Reference Pricing"], [3, "Reference Pricing (+20 ECU of discount)"], [4, "Drip Pricing"], [5, "None"]
    ])
    ask_price_fin = models.IntegerField()

    def ask_price_fin_min(self):
        return self.seller_valuation

    seller_id = models.IntegerField()
    sold = models.BooleanField(initial = False)
    bad_practice = models.BooleanField(initial = False)
    audited = models.BooleanField(initial = False)
    my_buyer = models.IntegerField(initial = 0)
    ref20 = models.IntegerField()

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
    paying_round = models.IntegerField()
    payoff_final = models.IntegerField()
    discount = models.IntegerField()

    def payoff_final_f(self):
        self.paying_round = random.randint(1, Constants.num_rounds)
        self.payoff_final = int(self.in_round(self.paying_round).payoff)
        self.participant.vars['paying_round'] = self.paying_round
        self.participant.vars['payoff_final'] = self.payoff_final
        self.session.vars['endowment'] = Constants.endowment
        print("##########################", self.paying_round)
        print("##########################", self.payoff_final)