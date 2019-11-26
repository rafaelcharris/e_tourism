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


#class UnalEmailValidator(EmailValidator):
#    def validate_domain_part(self, domain_part):
#        if domain_part != 'unal.edu.co':
#            return False
#        return True
#    message = "Por favor ingrese un correo con dominio @unal.edu.co"


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
            row['market_agent_role'] = p.participant.vars.get('agent_role')
            row['market_seller_valuation'] = p.participant.vars.get('seller_valuation')
            row['market_seller_package'] = p.participant.vars.get('seller_package')
            row['market_buyer_valuation_pac1'] = p.participant.vars.get('buyer_valuation_pac1')
            row['market_buyer_valuation_pac2'] = p.participant.vars.get('buyer_valuation_pac2')
            row['market_buyer_valuation_pac3'] = p.participant.vars.get('buyer_valuation_pac3')
            row['market_buyer_valuation_pac4'] = p.participant.vars.get('buyer_valuation_pac4')
            row['market_buyer_valuation_pac5'] = p.participant.vars.get('buyer_valuation_pac5')
            table_rows.append(row)
        return {'table_rows': table_rows}


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

#    e_mail = djmodels.EmailField(verbose_name='Correo Electrónico', validators=[UnalEmailValidator()])
