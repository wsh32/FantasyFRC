import requests

"""tba.py: TBA API"""

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"

api_link = "https://www.thebluealliance.com/api/v2"


class Team:
    def __init__(self, key, name, number, location):
        self.key = key
        self.name = name
        self.number = number
        self.location = location

    @staticmethod
    def get_team(number):
        if str(number)[0] != 'f':
            req = requests.get("{}/team/frc{}".format(api_link, number)).json()
        else:
            req = requests.get("{}/team/{}".format(api_link, number)).json()
        team = Team(req['key'], req['nickname'], req['team_number'], req['location'])
        return team

    @staticmethod
    def get_team_list():
        teams = []
        i = 0
        req = ["HI"]
        while req:
            req = requests.get("{}/teams/{}".format(api_link, i)).json()
            for j in req:
                teams.append(j['team_number'])
            i += 1
        return teams

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def get_location(self):
        return self.location

    def get_events(self, year):
        req = requests.get("{}/team/{}/{}/events".format(api_link, self.key, year)).json()
        events = []
        for i in req:
            events.append(Event.get_event(i['key']))
        return events

    def get_awards(self, event_key):
        req = requests.get("{}/team/{}/event/{}/awards".format(api_link, self.key, event_key)).json()
        awards = []
        for i in req:
            recipients = []
            for j in i['recipient_list']:
                recipients.append(Team.get_team(j['team_number']))
            awards.append(Award(i['name'], i['award_type'], i['event_key'], recipients, i['year']))
        return awards

    def get_matches(self, event_key):
        req = requests.get("{}/team/{}/event/{}/matches".format(api_link, self.key, event_key)).json()
        matches = []
        for i in req:
            matches.append(Match.get_match(i['key']))
        return matches

    def get_media(self):
        return "Not Supported Yet"

    def get_all_events(self):
        req = requests.get("{}/team/{}/history/events".format(api_link, self.key)).json()
        events = []
        for i in req:
            events.append(Event.get_event(i['key']))
        return events


class Event:
    def __init__(self, key, name, code, type, district, year, week, teams, matches, awards, alliances):
        self.key = key
        self.name = name
        self.code = code
        self.type = type
        self.district = district
        self.year = year
        self.week = week
        self.teams = teams
        self.matches = matches
        self.awards = awards
        self.alliances = alliances

    @staticmethod
    def get_event(key):
        req = requests.get("{}/event/{}".format(api_link, key)).json()

        teams = []
        req_teams = requests.get("{}/event/{}/teams".format(api_link, key)).json()
        for i in req_teams:
            teams.append(Team.get_team(i['team_number']))

        matches = []
        req_matches = requests.get("{}/event/{}/matches".format(api_link, key)).json()
        for i in req_matches:
            matches.append(Match.get_match(i['key']))

        awards = []
        req_awards = requests.get("{}/event/{}/awards".format(api_link, key)).json()
        for i in req_awards:
            recipients = []
            for j in i['recipient_list']:
                recipients.append(Team.get_team(j['team_number']))
            award = Award(i['name'], i['award_type'], key, recipients, i['year'])
            awards.append(award)

        alliances = []
        for i in req['alliances']:
            declines = []
            for j in i['declines']:
                declines.append(Team.get_team(j))
            picks = []
            for j in i['picks']:
                picks.append(Team.get_team(j))
            alliances.append(Alliance(declines, i['backup'], i['name'], picks))

        event = Event(req['key'], req['name'], req['event_code'], req['event_type_string'],
                      req['event_district_string'], req['year'], req['week'], teams, matches, awards, alliances)
        return event

    @staticmethod
    def event_list(year):
        req = requests.get("{}/events/{}".format(api_link, year)).json()
        events = []
        for i in req:
            events.append(i['key'])
        return events

    def get_key(self):
        return self.key

    def get_code(self):
        return self.code

    def get_type(self):
        return self.type

    def get_district(self):
        return self.district

    def get_year(self):
        return self.year

    def get_week(self):
        return self.week

    def get_teams(self):
        return self.teams

    def get_opr(self, team_number):
        req = requests.get("{}/event/{}/stats".format(api_link, self.key)).json()
        if str(team_number) in req['opr']:
            return req['opr'][str(team_number)]

    def get_dpr(self, team_number):
        req = requests.get("{}/event/{}/stats".format(api_link, self.key)).json()
        if str(team_number) in req['dpr']:
            return req['dpr'][str(team_number)]

    def get_awards(self):
        req = requests.get("{}/event/{}/awards".format(api_link, self.key)).json()
        awards = []
        for i in req:
            recipients = []
            for j in i['recipient_list']:
                recipients.append(Team.get_team(j['team_number']))
            awards.append(Award(i['name'], i['award_type'], i['event_key'], recipients, i['year']))
        return awards


class Match:
    def __init__(self, key, level, set_number, match_number, alliances, score_breakdown, event_key, videos):
        self.key = key
        self.level = level
        self.set_number = set_number
        self.match_number = match_number
        self.alliances = alliances
        self.score_breakdown = score_breakdown
        self.event_key = event_key
        self.videos = videos

    @staticmethod
    def get_match(key):
        req = requests.get("{}/api/v2/match/{}".format(api_link, key)).json()
        match = Match(req['key'], req['comp_level'], req['set_number'], req['match_number'],
                      req['alliances'], req['score_breakdown'], req['event_key'], req['videos'])
        return match


class Award:
    def __init__(self, name, type, event_key, recipient_list, year):
        self.name = name
        self.type = type
        self.event_key = event_key
        self.recipient_list = recipient_list
        self.year = year

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_event_key(self):
        return self.event_key

    def get_recipient_list(self):
        return self.recipient_list

    def get_year(self):
        return self.year


class Alliance:
    def __init__(self, declines, backup, name, picks):
        self.declines = declines
        self.backup = backup
        self.name = name
        self.picks = picks