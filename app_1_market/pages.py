from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class seller_p1(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini', 'see_list', 'com_practice', 'ask_price_fin']

    def is_displayed(self):
        if self.player.agent_role == False:
            return True
        else:
            return False

    def vars_for_template(self):
        return dict(
            agent_role = self.player.agent_role,
            seller_valuation = self.player.seller_valuation,
            seller_package = self.player.seller_package
        )

class buyer_p1(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    def is_displayed(self):
        if self.player.agent_role == True:
            return True
        else:
            return False

    def vars_for_template(self):
        return dict(
            agent_role = self.player.agent_role,
            buyer_valuation_pac1=self.player.buyer_valuation_pac1,
            buyer_valuation_pac2=self.player.buyer_valuation_pac2,
            buyer_valuation_pac3=self.player.buyer_valuation_pac3,
            buyer_valuation_pac4=self.player.buyer_valuation_pac4,
            buyer_valuation_pac5 = self.player.buyer_valuation_pac5,
            bid_price = self.player.bid_price,
        )

page_sequence = [seller_p1,
                 buyer_p1]
