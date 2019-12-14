from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

SESSION_CONFIGS = [
    dict(
        name='e_tourism_market_control',
        display_name="Market Control",
        num_demo_participants=20,
        app_sequence=['app_0_consent', 'app_2_market_control', 'app_8_summary', 'app_7_question', 'app_9_report'],
        use_browser_bots=False,
    ),
    dict(
        name='e_tourism_market_practices',
        display_name="Market Commercial Practices",
        num_demo_participants=2,
        app_sequence=['app_0_consent', 'app_1_market_com_practices', 'app_8_summary', 'app_7_question', 'app_9_report'],
        use_browser_bots=False,
    ),
    dict(
        name='e_tourism_market_formal_sanction',
        display_name="Market Formal Sanction",
        num_demo_participants=20,
        app_sequence=['app_0_consent', 'app_3_market_formal_sanction', 'app_8_summary', 'app_7_question', 'app_9_report'],
        use_browser_bots=False,
    ),
    dict(
        name='e_tourism_market_informal_sanction',
        display_name="Market Informal Sanction",
        num_demo_participants=20,
        app_sequence=['app_0_consent', 'app_4_market_informal', 'app_8_summary', 'app_7_question', 'app_9_report'],
        use_browser_bots=False,
    ),
    dict(
        name='e_tourism_market_regret',
        display_name="Market Regret",
        num_demo_participants=20,
        app_sequence=['app_0_consent', 'app_5_market_regret', 'app_8_summary', 'app_7_question', 'app_9_report'],
        use_browser_bots=False,
    ),
    dict(
        name='bot_testing',
        display_name="Testing bots",
        num_demo_participants=2,
        app_sequence=['app_0_consent', 'app_2_market_control', 'app_8_summary', 'app_9_report'],
#        app_sequence=['app_7_question'],
        use_browser_bots=False, ),



]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = "ECU"
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0

ROOMS = [
    dict(
        name = 'Study',
        display_name = 'Study',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6mz7+0&jqmits*no-&%03jf7@rp+x2uky7mg-s(f-r0uqj2pl8'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
