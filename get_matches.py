import http.client
import json
import os
from datetime import datetime
import string

# with open('matches.json', 'w') as outfile:
   # json.dump(response, outfile)


def trim(team_name):
    return team_name.replace('AFC', '') \
               .replace('FC', '') \
               .replace('FK', '') \
               .replace('TC', '') \
               .replace('BV', '') \
               .replace('KV', '') \
               .replace('SS', '') \
               .replace('09', '') \
               .replace('1901', '') \
               .replace('   ', '') \
               .replace('  ', ' ') \
               .replace('-', '\-') \
               .strip()


def get_matches(date_str):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': os.getenv('FOOTBALL_DATA_TOKEN', '') }

    print('ready to make request')
    connection.request('GET', '/v2/competitions/CL/matches?status=SCHEDULED', None, headers)
    response = connection.getresponse()
    raw_response = response.read().decode()
    print('got response ' + str(response.status))

    response = json.loads(raw_response)

    groups = dict(('Group ' + g, []) for g in string.ascii_uppercase[:8])
    play_off = []

    for match in response['matches']:
        if match['utcDate'].startswith(date_str):
            title = trim(match['homeTeam']['name']) + " vs " + trim(match['awayTeam']['name'])
            if match.get('group'):
                groups[match['group']].append(title)
            else:
                play_off.append(title)

    matches = []
    for g in sorted(groups):
        if len(groups[g]) > 0:
            matches.append(g)
            matches += groups[g]
            matches.append('')
    for m in play_off:
        matches.append(m)

    return matches


def get_matches_struct(date_str):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': os.getenv('FOOTBALL_DATA_TOKEN', '') }
    connection.request('GET', '/v2/competitions/CL/matches?status=SCHEDULED', None, headers )
    raw_response = connection.getresponse().read().decode()
    response = json.loads(raw_response)

    matches = []
    for m in response['matches']:
        if m['utcDate'].startswith(date_str):
            matches.append({'id': m['id'], 'start_time': datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ').strftime("%Y-%m-%d %H:%M:%S"),
                                'home_team': {'id': m['homeTeam']['id'], 'name': m['homeTeam']['name']},
                                'away_team': {'id': m['awayTeam']['id'], 'name': m['awayTeam']['name']}
            })
    return matches


def post_matches(date_str):
    connection = http.client.HTTPConnection('total.pipeinpipe.info')
    matches = get_matches_struct(date_str)

    for m in matches:
        data = '{"ext_id": "%s", "datetime": "%s", "comp_id": 25, "comp1": {"ext_id": %s, "name": "%s"}, "comp2": {"ext_id": %s, "name": "%s"}}' \
            % (m['id'], m['start_time'], m['home_team']['id'], m['home_team']['name'], m['away_team']['id'], m['away_team']['name'])
        connection.request('POST', '/api_proc.php?access_key=' + os.getenv('PIPEINPIPE_ACCESS_KEY', '')  + '&action=import_ext_match', data)
        print(connection.getresponse().read().decode())


def get_teams():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': os.getenv('FOOTBALL_DATA_TOKEN', '') }
    connection.request('GET', '/v2/competitions/CL/teams', None, headers)
    raw_response = connection.getresponse().read().decode()
    response = json.loads(raw_response)

    for t in response["teams"]:
        print(t["name"] + " - " + str(t["id"]))
    return response


# post_matches("2020-11-03")
