import scoreboard
import draft
import settings
from tba import *


def setup():
    for i in range(7):
        draft.create_draft(settings.GOOGLE_SERVICE_SECRET_FILE, i+1, settings.ADMINS, settings.PARTICIPANTS)
    scoreboard.create_scoreboard(settings.GOOGLE_SERVICE_SECRET_FILE, settings.ADMINS, settings.PARTICIPANTS)


def score(week):
    scoreboard.score_week(settings.GOOGLE_SERVICE_SECRET_FILE, week, 2017, settings.SCORING_SETTINGS)


if __name__ == "__main__":
    setup()
