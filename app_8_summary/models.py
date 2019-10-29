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

    summary_name = models.LongStringField()
    summary_id = models.IntegerField()
    summary_role = models.BooleanField()

    def push_vars_to_summary(self): #pushes vars to summary page
        self.summary_role = self.participant.vars.get('role')
        self.summary_name = self.participant.vars.get('consent_name')
        self.summary_id = self.participant.vars.get('consent_id_number')
        print("[[ APP_8_SUMMARY]] - PLAYER - PUSH_VARS_TO_SUMMARY.............--------------------------------]")

#    def report_summary(self): # pushes vars to the admin_report
#        self.participant.vars['FINAL_payoff'] = self.summary_FINAL_payoff
#        print("[[ APP_8_SUMMARY]] - PLAYER - REPORT_SUMMARY.............--------------------------------]")
