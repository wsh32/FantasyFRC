import csv
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from tba import *
import draft

"""scoreboard.py: Automatically updates the scoreboard. Thanks TBA"""

def auth(creds_file):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    gc = gspread.authorize(credentials)
    return gc


def get_scoreboard(gc):
    title = "FF2017 Scoreboard"
    try:
        sh = gc.open(title)
    except gspread.exceptions.SpreadsheetNotFound:
        return False

    return sh.get_worksheet(0)


def create_scoreboard(creds_file, admin_file, participants_file):
    gc = auth(creds_file)
    title = "FF2017 Scoreboard"
    sh = get_scoreboard(gc)
    if not sh:
        sh = gc.create(title)

    admin_csv = open(admin_file, 'r')
    admin_csv_reader = csv.DictReader(admin_csv, delimiter="\t")

    for i in admin_csv_reader:
        sh.share(i['Email'], perm_type='user', role='writer')

    participants_csv = open(participants_file, 'r')
    participants_csv_reader = csv.DictReader(participants_csv, delimiter="\t")
    names = []

    for i in participants_csv_reader:
        names.append(i['Name'])

    wks = sh.get_worksheet(0)
    wks.update_acell('A1', 'Name')
    for i in range(7):
        wks.update_cell(1, i + 2, 'Week {}'.format(i + 1))

    for i in range(len(names)):
        cell = "A{}".format(i+2)
        name = names[i]
        wks.update_acell(cell, name)


def score_week(creds_file, week, year):
    gc = auth(creds_file)
    wks = get_scoreboard(gc)
    dft = draft.get_draft(gc, week)

    col = wks.find('Week {}'.format(week)).col

    names = wks.col_values(1)[1:]

    for name in names:
        dftrow = dft.find(name).row
        picks = dft.get_row(dftrow)[1:]
        score = 0
        for pick in picks:
            score += score_team(pick)

        wks.update_cell(wks.find(name).row, col, score)


def score_team(number, week, year, award_scoring):
    team = Team.get_team(number)
    event = team.get_event_week(week, year)
    event_key = event.get_key()
    awards = team.get_awards(event_key)

    csvfile = open(award_scoring, 'r')
    reader = csv.DictReader(csvfile, delimiter="\t")

    score = 0

    for award in awards:
        type = award.get_type()
        for i in reader:
            if type == i['tba id number']:
                score += i['points']
                break
            score += 2

    matches = team.get_matches()
    highest_level = 0
    for match in matches:
        if match.get_level() == 'qf':
            if highest_level < 1:
                highest_level = 1
        elif match.get_level() == 'sf':
            if highest_level < 2:
                highest_level = 2
        elif match.get_level() == 'f':
            highest_level = 2

    if highest_level == 2:
        score += 10
    elif highest_level == 1:
        score += 4

    ranking = event.get_team_ranking(number)
    if ranking == 1:
        score += 20
    elif ranking <= 3:
        score += 12
    elif ranking <= 8:
        score += 6
    elif ranking <= 12:
        score += 3
    elif ranking <= 16:
        score += 2

    return score
