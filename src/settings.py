"""settings.py: Holds settings. Alter here per project host"""


GOOGLE_API_KEY = open('../api_key.txt','r').read()
GOOGLE_SERVICE_SECRET_FILE = '../service_secret.json'
SCORING_SETTINGS = 'comp/scoring.csv'
PARTICIPANTS = 'comp/participants.csv'
ADMINS = 'comp/admins.csv'


SCOREBOARD_TITLE = "FF2017 Scoreboard"
DRAFT_TEMPLATE = "FF2017 Draft Week {}"
