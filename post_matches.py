import http.client
from datetime import datetime, timedelta
from get_matches import get_matches_struct
from optparse import OptionParser

def post_matches(date_str):
    connection = http.client.HTTPConnection('total.pipeinpipe.info')
    matches = get_matches_struct(date_str)

    print("Found " + str(len(matches)) + " matches")
    for m in matches:
        data = '{"ext_id": "%s", "datetime": "%s", "comp_id": 25, "comp1": {"ext_id": %s, "name": "%s"}, "comp2": {"ext_id": %s, "name": "%s"}}' \
            % (m['id'], m['start_time'], m['home_team']['id'], m['home_team']['name'], m['away_team']['id'], m['away_team']['name'])
        data = data.replace("ş", "s")
        connection.request('POST', '/api_proc.php?access_key=' + os.getenv('PIPEINPIPE_ACCESS_KEY', '') + '&action=import_ext_match', data)
        print("Posting match: " + data)
        print(connection.getresponse().read().decode())


parser = OptionParser()
parser.add_option("-d", "--date", default=None, help="date when matches to be posted start, YYYY-MM-DD")
(options, arguments) = parser.parse_args()
opts = options.__dict__


target_date = datetime.strptime(opts["date"], "%Y-%m-%d").date() if "date" in opts and opts["date"] \
        else datetime.date(datetime.today())

print("Today is " + target_date.strftime("%Y-%m-%d"))
post_matches(target_date.strftime("%Y-%m-%d"))

print("Checking tomorrow")
post_matches((target_date + timedelta(1)).strftime("%Y-%m-%d"))
#post_matches("2020-11-04")
