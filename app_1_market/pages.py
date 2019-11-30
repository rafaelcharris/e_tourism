from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class seller(Page):
    form_model = 'player'
    form_fields = ['ask_price_ini', 'see_list', 'ask_price_fin', 'seller_package',
                   'seller_valuation']

    def is_displayed(self):
        return self.player.role() != 'buyer'

    def vars_for_template(self):
        self.subsession.assign_pac_val()

        return dict(
            seller_package = self.player.seller_package,
            role = self.participant.vars['role']
        )
class seller_2(Page):
    form_model = 'player'
    form_fields = [
        'see_list',
        'com_practice'
    ]
    def is_displayed(self):
        return self.player.role() != 'buyer'

class buyer(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    def is_displayed(self):
        return self.player.role() != 'seller'

    def vars_for_template(self):
        self.group.assign_pac_val()
        return dict(
            role = self.participant.vars['role']
        )
page_sequence = [seller, seller_2, buyer]
