from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class seller_p1(Page):
    form_model = 'player'
    form_fields = ['ask_price']

    def vars_for_template(self):
        return dict(
            role = self.player.role,
            seller_valuation = self.player.seller_valuation,
#            buyer_valuation = self.player.buyer_valuation,
#            bid_price = self.player.bid_price,

        )
page_sequence = [seller_p1]
