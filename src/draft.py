import csv
import random
from oauth2client.service_account import ServiceAccountCredentials
import gspread

"""draft.py: Creates draft spreadsheets on Google Sheets and grabs data"""


def auth(creds_file):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    gc = gspread.authorize(credentials)
    return gc


def get_draft(creds_file, week):
    gc = auth(creds_file)
    title = "FF2017 Draft Week {}".format(week)
    try:
        sh = gc.open(title)
    except gspread.exceptions.SpreadsheetNotFound:
        return False
    return sh.get_worksheet(0)


def create_draft(creds_file, week, admin_file, participants_file):
    gc = auth(creds_file)
    title = "FF2017 Draft Week {}".format(week)
    try:
        sh = gc.open(title)
    except gspread.exceptions.SpreadsheetNotFound:
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

    random.shuffle(names)

    wks = sh.get_worksheet(0)
    wks.update_acell('A1', 'Name')
    for i in range(6):
        wks.update_cell(1, i+2, 'Pick {}'.format(i+1))

    for i in range(len(names)):
        cell = "A{}".format(i+2)
        name = names[i]
        wks.update_acell(cell, name)
