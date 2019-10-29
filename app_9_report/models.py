from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from django.core.validators import EmailValidator


author = 'Your name here'

doc = """
Your app description
"""


class UnalEmailValidator(EmailValidator):
    def validate_domain_part(self, domain_part):
        if domain_part != 'unal.edu.co':
            return False
        return True
    message = "Por favor ingrese un correo con dominio @unal.edu.co"


class Constants(BaseConstants):
    name_in_url = 'app_9_report'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        table_rows = []
        for p in self.get_players():
            row = p.participant.vars #quejesto?
            row['participant_code'] = p.participant.code
            row['consent_name'] = p.participant.vars.get('consent_name')
            row['consent_id_number'] = p.participant.vars.get('consent_id_number')
            row['addition_treatment'] = p.participant.vars.get('treatment')
            row['addition_acc_was_correct'] = p.participant.vars.get('addition_acc_was_correct')
            row['addition_acc_payoff'] = p.participant.vars.get('addition_acc_payoff')
            row['addition_final_payoff'] = p.participant.vars.get('addition_final_payoff')
            row['trust_metarole'] = p.participant.vars.get('metarole')
            row['trust_paying_round'] = p.participant.vars.get('paying_round')
            row['trust_t_money_payoff'] = p.participant.vars.get('t_money_payoff')
            row['trust_b_money_payoff'] = p.participant.vars.get('b_money_payoff')
            row['report_trust_totalsum_payoff'] = p.participant.vars.get('trust_totalsum_payoff')
            row['report_FINAL_payoff'] = p.participant.vars.get('FINAL_payoff')
            table_rows.append(row)
        return {'table_rows': table_rows}


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    e_mail = djmodels.EmailField(verbose_name='Correo Electrónico', validators=[UnalEmailValidator()])