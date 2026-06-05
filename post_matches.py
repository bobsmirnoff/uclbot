import http.client
from datetime import datetime, timedelta
from get_matches import get_matches_struct
from optparse import OptionParser
from competition import comp
import os


def post_matches(date_str):
    connection = http.client.HTTPConnection('total.pipeinpipe.info')
    matches = get_matches_struct(date_str)

    print("Found " + str(len(matches)) + " matches")
    for m in matches:
        data = '{"ext_id": "%s", "datetime": "%s", "comp_id": %s, "comp1": {"ext_id": %s, "name": "%s"}, "comp2": {"ext_id": %s, "name": "%s"}}' \
            % (m['id'], m['start_time'], comp['id'], m['home_team']['id'], m['home_team']['name'], m['away_team']['id'], m['away_team']['name'])
        # print(data)
        data = data.replace("ş", "s").replace("ň", "n").encode('utf-8')
        connection.request('POST', '/api_proc.php?access_key=' + os.getenv('PIPEINPIPE_ACCESS_KEY', '') + '&action=import_ext_match', data)
        print("Posting match: " + str(data))
        print(connection.getresponse().read().decode())


parser = OptionParser()
parser.add_option("-d", "--date", default=None, help="date when matches to be posted start, YYYY-MM-DD")
(options, arguments) = parser.parse_args()
opts = options.__dict__


target_date = datetime.strptime(opts["date"], "%Y-%m-%d").date() if "date" in opts and opts["date"] \
        else datetime.date(datetime.today())

print("Posting matches for " + target_date.strftime("%Y-%m-%d"))
post_matches(target_date.strftime("%Y-%m-%d"))

print("Checking the next day")
post_matches((target_date + timedelta(1)).strftime("%Y-%m-%d"))

# test
#post_matches("2026-06-11")
