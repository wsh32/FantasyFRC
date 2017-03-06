import scoreboard
import draft
import settings
from tba import *


def setup():
    print("Fantasy Setup")
    for i in range(7):
        draft.create_draft(settings.GOOGLE_SERVICE_SECRET_FILE, i+1, settings.ADMINS, settings.PARTICIPANTS)
    scoreboard.create_scoreboard(settings.GOOGLE_SERVICE_SECRET_FILE, settings.ADMINS, settings.PARTICIPANTS)


def score(week):
    scoreboard.score_week(settings.GOOGLE_SERVICE_SECRET_FILE, week, 2017, settings.SCORING_SETTINGS)


def test():
    # api_link = "https://www.thebluealliance.com/api/v2"
    # headers = {'X-TBA-App-Id': 'frc687:fantasy_scout:v01'}
    #
    # req = requests.get("{}/event/{}/rankings".format(api_link, '2017txlu'), headers=headers).json()
    # for i in req:
    #     # print(i)
    #     print(i[1])
    #     if i[1] == 118:
    #         print(int(i[0]))
    #         print("HI")
    scoreboard.score_team('1595', 1, 2017, settings.SCORING_SETTINGS, 'SPENCER', True)


if __name__ == "__main__":
    test()
