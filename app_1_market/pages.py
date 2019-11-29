from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class seller(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini', 'see_list', 'com_practice', 'ask_price_fin', 'role', 'seller_package',
                   'seller_valuation']

    def is_displayed(self):
        if self.player.role == 'seller':
            return True

class buyer(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    def is_displayed(self):
        return self.player.role == 'buyer'

    def vars_for_template(self):
        return dict(
            buyer_valuation_pac1=self.player.buyer_valuation_pac1,
            buyer_valuation_pac2=self.player.buyer_valuation_pac2,
            buyer_valuation_pac3=self.player.buyer_valuation_pac3,
            buyer_valuation_pac4=self.player.buyer_valuation_pac4,
            buyer_valuation_pac5 = self.player.buyer_valuation_pac5,
            bid_price = self.player.bid_price,
        )

page_sequence = [seller, buyer]
