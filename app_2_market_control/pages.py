from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class instructions(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.round_number == 1


class instructions_2(Page):
    pass


class MyWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.role() == 'buyer'

    title_text = "You are a Buyer"
    body_text = "Please wait while the sellers set their offers"


class seller(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini',
                   'see_list',
                   ]

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

#TODO: Fix sellers IDs so they show from 1 to 10 instead of 1 to 19
class seller_2(Page):
    form_model = 'player'
    form_fields = [
        'ask_price_fin'
    ]
    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        dict(
            role = self.player.role()
        )

class buyer(Page):

    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['my_seller']

    def is_displayed(self):
        return self.player.role() != 'seller'

    def before_next_page(self):
        import time
        self.player.time_spent = time.time()

#        if self.player.round_number == Constants.num_rounds:
#            self.player.payoff_final_f()

    def vars_for_template(self):
        self.group.drip_price()

        return dict(
            role = self.participant.vars['role'],
            pac_val = self.participant.vars['valuations'],
            #parece que esto que sigue es innecesario
            #pac1 = self.player.buyer_valuation_pac1,
            #pac2 = self.player.buyer_valuation_pac2,
            #pac3 = self.player.buyer_valuation_pac3,
            #pac4 = self.player.buyer_valuation_pac4,
            #pac5 = self.player.buyer_valuation_pac5
        )

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    def vars_for_template(self):
        self.group.set_payoff()
        self.group.who_purchased()
        if self.player.round_number == Constants.num_rounds:
            self.player.payoff_final_f()

        return dict(
            role = self.participant.vars['role'],
            payoff = self.player.payoff,
            price = self.player.paid,
            seller = self.player.my_seller,
            sold = self.player.sold
        )



page_sequence = [instructions,
                 instructions_2,
                 seller,
                 SellerWaitPage,
                 seller_2,
                 MyWaitPage,
                 buyer,
                 ResultsWaitPage,
                 Results
                 ]


