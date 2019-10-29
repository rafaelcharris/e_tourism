from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_8_summary'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    #primera parte:
    summary_addition_acc_was_correct = models.IntegerField()
    summary_addition_acc_payoff = models.IntegerField()
    summary_addition_final_payoff = models.FloatField()

    #segunda parte:
    #summary_trust_role = models.LongStringField()
    #summary_trust_round_number = models.IntegerField()
    summary_trust_t_money_payoff = models.IntegerField()
    summary_trust_b_money_payoff = models.IntegerField()
    summary_trust_totalsum_payoff = models.IntegerField()
    #FINAL
    summary_FINAL_payoff = models.FloatField()

    def push_vars_to_summary(self):
        self.summary_addition_acc_was_correct = self.participant.vars.get('addition_acc_was_correct')
        self.summary_addition_acc_payoff = self.participant.vars.get('addition_acc_payoff')
        self.summary_addition_final_payoff = self.participant.vars.get('addition_final_payoff')

        #self.summary_trust_role = self.participant.vars.get('addition_acc_was_correct')
        #self.summary_trust_round_number = self.participant.vars.get('addition_acc_acc_payoff')
        self.summary_trust_t_money_payoff = self.participant.vars.get('t_money_payoff')
        self.summary_trust_b_money_payoff = self.participant.vars.get('b_money_payoff')
        self.summary_trust_totalsum_payoff = self.participant.vars.get('trust_totalsum_payoff')

        self.summary_FINAL_payoff = self.participant.vars.get('addition_final_payoff') + self.participant.vars.get('trust_totalsum_payoff')
        print("[[ APP_3_SUMMARY]] - PLAYER - PUSH_VARS_TO_SUMMARY.............--------------------------------]")

    def report_summary(self):
        self.participant.vars['FINAL_payoff'] = self.summary_FINAL_payoff
        print("[[ APP_3_SUMMARY]] - PLAYER - REPORT_SUMMARY.............--------------------------------]")
