from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Rafael'

doc = """
Encuesta demográfica
"""

class Constants(BaseConstants):
    name_in_url = 'app_7_question'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    gender = models.IntegerField(
        label = 'What is your gender?',
        choices = [(0, "Female"),
                   (1, "Male"),
                   (2,"Other")],
        widget = widgets.RadioSelectHorizontal
    )

    age = models.IntegerField(
        label = 'What is your age?',
        min = 18, max = 70
    )

    country = models.StringField(
        label = "What is your country of origin?",
    )

    education = models.IntegerField(
        label = 'What is your education level (maximum degree of completed studies)?',
        choices = [(1, "No schooling"),
                   (2, "Primary School"),
                   (3, "Technical / Vocational school"),
                   (4, "Secondary School (High School)"),
                   (5, "University Degree (2-5 years)"),
                   (6, "Post-graduate Degree (Master / Ph.D.)")]
    )

    civil_status = models.IntegerField(
        label = 'What is your civil status',
        choices = [(1, 'Single (Never married)'),
                   (2, 'Living with partner'),
                   (3, 'Married'),
                   (4, 'Separated / Divorced'),
                   (5, 'Widower')]
    )

    income = models.IntegerField(
        label= 'What is your approximate gross (brutto) annual income level in your household?',
        choices = [
            (1, '0 - 20.000 Euro'),
            (2,'20.001 - 40.000 Euro'),
            (3,'40.001 - 60.000 Euro'),
            (4,'60.001 - 80.000 Euro'),
            (5,'80.001 - 100.000 Euro'),
            (6,'Above 100.000 Euro')])

    online_frequency = models.IntegerField(
        label = 'How often do you generally access the Internet?',
        choices = [
            (1, 'Continuously/On an hourly basis'),
            (2, 'Several times per day'),
            (3, 'Once per day'),
            (4, 'Several times per week'),
            (5, 'Once per week'),
            (6, 'Less often than once per week')
        ]
    )

    online_purchase = models.IntegerField(
        label = 'When buying products and services related to traveling (airplane / train tickets, hotel booking, travel'
                ' packages, etc.) Do you often use the internet for this purpose?',
        choices = [
            (0, 'No'),
            (1, 'Yes')
        ]
    )
