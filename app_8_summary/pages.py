from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class app_8_summary(Page):

    def vars_for_template(self):
        return dict(
            paying_round = self.participant.vars.get('paying_round'),
            payoff_final = self.participant.vars.get('payoff_final'),
            endowment = self.session.vars.get('endowment')
        )


page_sequence = [
    app_8_summary,
]
