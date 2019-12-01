from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class instructions(Page):
    pass

class MyWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.role() == 'buyer'

    title_text = "You are a Buyer"
    body_text = "Please wait while the sellers set their offers"


class seller(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini', 'see_list']

    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        return dict(
            seller_package = self.player.seller_package,
            role = self.participant.vars['role']
        )

class SellerWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.role() == 'seller'

    title_text = "Please Wait"
    body_text = "Please wait while the other sellers set their prices"

class seller_2(Page):
    form_model = 'player'
    form_fields = [
        'com_practice',
        'ask_price_fin'
    ]
    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        dict(
            role = self.player.role()
        )

class buyer(Page):
    form_model = 'player'
    form_fields = ['seller'] #la idea es que como tengo la id en group, puedo recuperar qué estaba vendiendo y a cómo.

    def is_displayed(self):
        return self.player.role() != 'seller'

    def vars_for_template(self):
        return dict(
            role = self.participant.vars['role'],
            pac1 = self.player.buyer_valuation_pac1,
            pac2 = self.player.buyer_valuation_pac2,
            pac3 = self.player.buyer_valuation_pac3,
            pac4 = self.player.buyer_valuation_pac4,
            pac5 = self.player.buyer_valuation_pac5
        )

class SecondWaitPage(WaitPage):
    title_text = "You offer has been made"
    def is_displayed(self):
        return self.player.role == "seller"

class ResultsWaitPage(WaitPage):
    #Acá calcular los resultados de la ronda para los pagos tengo el id del vendedor, a partir de eso
    #debo recuperar qué vendió y a cómo

    def set_payoffs(self):
        def get_package(self):
            for p in self.get_players():
                if p.role == 'buyer':
                    p.package_purchased = self.group.get_players_by_id(p.seller).seller.package
        # set payoff
        def set_payoff(self):
            for p in self.get_players():
                if p.role == "buyer":
                    #el pago de este jugador es el initial endowment + su valuación menos lo que le costó el paquete
                    p.payoff = Constants.endowment + p.participant.vars["valuations"][p.package_purchased] - \
                               self.group.get_players_by_id(seller).ask_price_fin

                #else:
                #    p.payoff = Constants.endowment + p.participant.vars['seller_valuations'][self.package] - \
                #                p.participant['package_valuations'][
                #                    self.package_purchased] - Constants.see_list_cost * int(self.see_list)


    def after_all_players_arrive(self):
        self.set_payoffs()

class Results(Page):

page_sequence = [instructions,
                 seller,
                 SellerWaitPage,
                 seller_2,
                 MyWaitPage,
                 SecondWaitPage,
                 buyer,
                 ResultsWaitPage]

