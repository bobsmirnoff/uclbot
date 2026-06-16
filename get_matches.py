import http.client
import json
import os
import requests
from datetime import datetime, timedelta
import string
from competition import comp

# with open('matches.json', 'w') as outfile:
   # json.dump(response, outfile)


def trim(team_name):
    return team_name
    if team_name == '' or not team_name:
        return ''
    return team_name.replace('AFC', '') \
               .replace('FC', '') \
               .replace('FK', '') \
               .replace('TC', '') \
               .replace('CF', '') \
               .replace('BV', '') \
               .replace('KV', '') \
               .replace('SSC', '') \
               .replace('SS', '') \
               .replace('SK', '') \
               .replace('09', '') \
               .replace('1901', '') \
               .replace('1.', '') \
               .replace('   ', '') \
               .replace('  ', ' ') \
               .strip()


def get_matches(date_str):
    url = "https://api.football-data.org"
    headers = {"X-Auth-Token": os.getenv('FOOTBALL_DATA_TOKEN', '')}

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url + '/v4/competitions/%s/matches?status=SCHEDULED' % comp['name'], allow_redirects=True).json()

    if 'matches' not in response:
        return []

    groups = dict(('GROUP_' + g, []) for g in string.ascii_uppercase[:26])
    play_off = []
    day_after = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    for match in response['matches']:
        if (match['utcDate'].startswith(date_str) or match['utcDate'].startswith(day_after)) and match['homeTeam']['name'] and match['awayTeam']['name']:
            title = trim(match['homeTeam']['name']) + " vs " + trim(match['awayTeam']['name'])
            if match.get('group'):
                groups[match['group']].append(title)
            else:
                play_off.append(title)

    matches = []
    for g in sorted(groups):
        if len(groups[g]) > 0:
            matches.append(g.replace('_', ' '))
            matches += groups[g]
            matches.append('')
    for m in play_off:
        matches.append(m)

    return matches


def get_matches_struct(date_str):
    url = "https://api.football-data.org"
    headers = {"X-Auth-Token": os.getenv('FOOTBALL_DATA_TOKEN', '')}

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url + '/v4/competitions/%s/matches?status=SCHEDULED' % comp['name'], allow_redirects=True).json()

    matches = []
    for m in response['matches']:
        if m['utcDate'].startswith(date_str) and m['homeTeam']['name'] and m['awayTeam']['name']:
            matches.append({'id': m['id'], 'start_time': datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d %H:%M:%S"),
                                'home_team': {'id': m['homeTeam']['id'], 'name': trim(m['homeTeam']['name'])},
                                'away_team': {'id': m['awayTeam']['id'], 'name': trim(m['awayTeam']['name'])}
            })
    return matches


def post_matches(date_str):
    connection = http.client.HTTPConnection('total.pipeinpipe.info')
    matches = get_matches_struct(date_str)

    for m in matches:
        data = '{"ext_id": "%s", "datetime": "%s", "comp_id": %s, "comp1": {"ext_id": %s, "name": "%s"}, "comp2": {"ext_id": %s, "name": "%s"}}' \
            % (m['id'], m['start_time'], comp['id'], m['home_team']['id'], m['home_team']['name'], m['away_team']['id'], m['away_team']['name'])
        connection.request('POST', '/api_proc.php?access_key=' + os.getenv('PIPEINPIPE_ACCESS_KEY', '')  + '&action=import_ext_match', data)
        print(connection.getresponse().read().decode())


def print_teams():
    url = "https://api.football-data.org"
    headers = {"X-Auth-Token": os.getenv('FOOTBALL_DATA_TOKEN', '')}

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url + '/v4/competitions/%s/teams' % comp['name'], allow_redirects=True).json()

    for t in response["teams"]:
        print(t["name"] + " - " + str(t["id"]))


#post_matches("2026-06-12")
#print(get_matches("2026-06-12"))
#print(get_matches_struct("2026-06-12"))
#print_teams()
