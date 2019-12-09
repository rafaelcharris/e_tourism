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
    name_in_url = 'app_5_market_formal_sanction'
    players_per_group = 4
    num_rounds = 5
    endowment = c(30)
    see_list_cost = c(3)
    prob_audit = 0.2
    packages = [i for i in range(1, 6)]
    sanction = c(6)

    seller_valuations = [70, 60, 50, 50, 40, 40, 30, 20, 10, 10]
    buyer_valuations = [100, 100, 90, 80, 80, 70, 60, 60, 50, 40]

    com_practice = [i for i in range(1,5)]

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
                    p.participant.vars['seller_id'] = p.seller_id #assign a seller id

                else:
            # Assign valuations for each packaque for the sellers
            #Esta parte del código debería asignarle un valor random a cada paquete
                    p.participant.vars["valuations"] = dict(zip(Constants.packages, numpy.random.choice(Constants.buyer_valuations, size =5, replace = False)))
                    p.buyer_valuation_pac1 = p.participant.vars["valuations"].get(1)
                    p.buyer_valuation_pac2 = p.participant.vars["valuations"].get(2)
                    p.buyer_valuation_pac3 = p.participant.vars["valuations"].get(3)
                    p.buyer_valuation_pac4 = p.participant.vars["valuations"].get(4)
                    p.buyer_valuation_pac5 = p.participant.vars["valuations"].get(5)
                    id_b = itertools.cycle([i for i in range(1, 11)])
                    p.participant.vars['buyer_id'] = next(id_b)


class Group(BaseGroup):

    #Acá calcular los resultados de la ronda para los pagos tengo el id del vendedor, a partir de eso
    #debo recuperar qué vendió y a cómo

    def set_payoff(self):
        #todo podría crear la lista de precios acá de una vez
        for p in self.get_players():
            if p.role() == "buyer":
                the_seller = self.get_player_by_id(p.my_seller)
                the_seller.sold = True
                #get info of the package
                p.package_purchased = the_seller.seller_package
                p.paid = the_seller.ask_price_fin
                p.payoff = p.participant.vars['valuations'].get(p.package_purchased) - p.paid
            else:

                p.payoff = (p.ask_price_fin - p.seller_valuation - int(p.see_list)*Constants.see_list_cost)*int(p.sold) - p.bad_practice*Constants.sanction

    def audit(self):
        prices = []

        for p in self.get_players():
            if p.role() == "seller":
                prices.append(p.ask_price_fin)
        #esta función debería prenderse un 20% de las veces para hacer un audit

        if numpy.random.uniform(0, 1) <= Constants.prob_audit:

            for p in self.get_players():
                if p.role() == "seller":
                    p.audited = True
                    if p.com_practice == 1:
                        p.bad_practice = p.ask_price_fin > min(prices)
                    elif p.com_practice == 2:
                        p.bad_practice = p.ask_price_fin >= p.ask_price_ini
                    else: # p.comm_practice == 3:
                        p.bad_practice = False
                        #todo definir cómo es hacer trampa con drip pricing.


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
    bad_practice = models.BooleanField(initial = False)
    audited = models.BooleanField(initial = False)

    #Buyer
    #Preguntar a Felipe si puedo borrar estos campos de valuación de cada paquete
    buyer_valuation_pac1 = models.IntegerField()
    buyer_valuation_pac2 = models.IntegerField()
    buyer_valuation_pac3 = models.IntegerField()
    buyer_valuation_pac4 = models.IntegerField()
    buyer_valuation_pac5 = models.IntegerField()
    bid_price = models.IntegerField()
    package_purchased = models.IntegerField()
    my_seller = models.IntegerField()
    paid = models.IntegerField()
    buyer_id = models.IntegerField()
    time_spent = models.FloatField()