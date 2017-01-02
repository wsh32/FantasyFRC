import scoreboard
import draft
import settings
from tba import *

#draft.create_draft(settings.GOOGLE_SERVICE_SECRET_FILE, 1, settings.ADMINS, settings.PARTICIPANTS)

#scoreboard.create_scoreboard(settings.GOOGLE_SERVICE_SECRET_FILE, settings.ADMINS, settings.PARTICIPANTS)

scoreboard.score_week(settings.GOOGLE_SERVICE_SECRET_FILE,1,2016,settings.SCORING_SETTINGS)
