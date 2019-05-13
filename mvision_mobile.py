import os
import json
import requests

from datetime import datetime, timedelta

class MMOBILE():

    def __init__(self):
        self.auth_url = 'https://iam.mcafee-cloud.com/iam/v1.0/token'
        self.event_url = 'https://ui-mcafee.mvision.mcafee.com/mvisionmobile/fetchThreatEventsList.do'
        self.user = '' #MVISION Login Username
        self.pw = '' #MVISION Login Password
        # Login to the MVISION EPO console and open a new tab
        # go to https://auth.ui.mcafee.com/support.html to retrieve your client_id
        self.client_id = ''

        self.scope = 'mv:m:admin'
        self.headers = {'Accept': 'application/json'}

        self.dir = '/home/mcafee/mvision_logs/mmobile_logs/' #Directory to where the logs should be stored

        now = datetime.utcnow()
        self.nowiso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        past = now - timedelta(minutes=5)
        self.pastiso = past.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.statefile = '/home/mcafee/mvision_logs/script/state.log' #Location of the pointer file

        if os.path.isfile(self.statefile):
             self.state = open(self.statefile, 'r').read()
        else:
             self.state = '0'

    def auth(self):
        data = {
            "username": self.user,
            "password": self.pw,
            "client_id": self.client_id,
            "scope": self.scope,
            "grant_type": "password"
        }

        r = requests.post(self.auth_url, headers=self.headers, data=data)
        self.token = r.json()['access_token']
        self.headers['Authorization'] = 'Bearer ' + self.token

    def events(self):
        r = requests.get(self.event_url + '?_start={}'.format(self.state), headers=self.headers)
        evts = r.json()
        return(evts)

    def write(self, evts):
        i = 0

        for event in evts['threatEventList']:
            file = open(self.dir + str(i) + '.json', 'w')
            file.write(json.dumps(event))
            file.close()
            i+=1

        open(self.statefile, 'w').write(str(evts['totalRecords']))
        self.new_state = evts['totalRecords'] - int(self.state)

if __name__ == '__main__':

    mmobile = MMOBILE()
    mmobile.auth()
    events = mmobile.events()

    mmobile.write(events)
    print(mmobile.nowiso + ': Successfully pulled logs {} from MVISION Mobile'.format(str(mmobile.new_state)))

