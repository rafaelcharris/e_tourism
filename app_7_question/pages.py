from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class questionnaire_intro(Page):
    pass


class questionnaire(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'country', 'education', 'civil_status', 'income', 'online_frequency', 'online_purchase']

page_sequence = [
    questionnaire_intro,
    questionnaire,
]
