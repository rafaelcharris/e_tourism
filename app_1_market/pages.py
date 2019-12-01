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
    form_fields = ['package_purchased']

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

class buyer_2(Page):
    form_model = 'player'
    form_fields = ['seller']

    def vars_for_template(self):
        return dict(
        role=self.participant.vars['role'],
        player = self.player.id_in_group,
        price = self.player.ask_price_fin,
        seller_package = self.player.seller_package
        )

    def is_displayed(self):
        return self.player.role() != 'seller'

class ResultsWaitPage(WaitPage):
    def set_payoffs(self):
        # set payoff
        def set_payoff(self):
            buyer = self.get_player_by_role('buyer')
            seller = self.get_player_by_role('seller')

            for p in self.get_players():
                buyer.payoff = p.participant.vars['seller_valuations'][self.package_purchased] - \
                               p.participant['package_valuations'][
                                   self.package_purchased]  # necesito la id del jugador al que le compró

                seller.payoff = p.participant.vars['seller_valuations'][self.package_purchased] - \
                                p.participant['package_valuations'][
                                    self.package_purchased] - Constants.see_list_cost * int(self.see_list)

        pass

    def after_all_players_arrive(self):
        self.set_payoffs()

page_sequence = [instructions,
                 MyWaitPage,
                 seller,
                 SellerWaitPage,
                 seller_2,
                 SecondWaitPage,
                 buyer]
