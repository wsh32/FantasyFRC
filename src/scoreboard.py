from oauth2client.service_account import ServiceAccountCredentials
import gspread
from tba import *
import draft
import settings
import threading

"""scoreboard.py: Automatically updates the scoreboard. Thanks TBA"""

TITLE = settings.SCOREBOARD_TITLE

def auth(creds_file):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    gc = gspread.authorize(credentials)
    return gc


def get_scoreboard(gc):
    title = TITLE
    try:
        sh = gc.open(title)
    except gspread.exceptions.SpreadsheetNotFound:
        return False

    return sh.get_worksheet(0)


def create_scoreboard(creds_file, admin_file, participants_file):
    gc = auth(creds_file)
    title = TITLE
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


def score_week(creds_file, week, year, award_scoring):
    gc = auth(creds_file)
    wks = get_scoreboard(gc)
    dft = draft.get_draft(gc, week)

    col = wks.find('Week {}'.format(week)).col

    names = [x for x in wks.col_values(1)[1:] if x != ""]
    threads = []
    for name in names:
        t = threading.Thread(target=score_player, args=(dft, wks, col, name, week, year, award_scoring,))
        threads.append(t)
        t.start()


def score_player(dft, wks, col, name, week, year, award_scoring):
    dftrow = dft.find(name).row
    picks = [x for x in dft.row_values(dftrow)[1:] if x != ""]
    score = 0
    for pick in picks:
        score += score_team(pick, week, year, award_scoring, name, False)

    wks.update_cell(wks.find(name).row, col, score)


def score_team(number, week, year, award_scoring, player, debug):
    team = Team.get_team(number)
    if debug:
        print("Number", number)
    event = team.get_event_week(week, year)
    if not event or event is None:
        if debug:
            print("TEAM MISSING EVENT: ", number)
        return 0
    event_key = event.get_key()
    if debug:
        print(event_key)
    awards = team.get_awards(event_key)

    csvfile = open(award_scoring, 'r').read()

    csv = []

    for i in csvfile.split("\n")[1:]:
        csv.append(i.split("\t"))

    score = 0

    for award in awards:
        type = award.get_type()
        for i in csv:
            print(i[1])
            if str(type) == str(i[1]):
                if debug:
                    print(i[0], int(i[2]))
                score += int(i[2])
                break
            score += 2

            if debug:
                print("score", score)

    matches = team.get_matches(event_key)
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
        if debug:
            print('semi')
        score += 10
    elif highest_level == 1:
        if debug:
            print('quarter')
        score += 4

    ranking_score = event.get_team_stat_number(number, 2)
    if debug:
        print("ranking score", ranking_score)
    score += int(ranking_score)

    ranking = event.get_team_ranking(number)
    if debug:
        print("team:ranking",number,ranking)
    if ranking is None and debug:
        print("Missing", number)
    elif ranking == 1:
        score += 20
    elif ranking <= 3:
        score += 12
    elif ranking <= 8:
        score += 6
    elif ranking <= 12:
        score += 3
    elif ranking <= 16:
        score += 2
    if debug:
        print(ranking)
        print(score)

    print(player, number, score, sep='\t')
    return score
