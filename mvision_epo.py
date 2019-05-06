import json
import requests

from datetime import datetime, timedelta

class MEPO():

    def __init__(self):
        self.auth_url = 'https://iam.mcafee-cloud.com/iam/v1.0/token'
        self.event_url = 'https://arevents.mvision.mcafee.com/eventservice/api/v1/events'

        self.user = '' #MVISION Login Username
        self.pw = '' #MVISION Login Password
        # Login to the MVISION EPO console and open a new tab
        # go to https://auth.ui.mcafee.com/support.html to retrieve your client_id
        self.client_id = ''

        self.scope = 'epo.evt.r' #Change if required
        self.headers = {'Accept' : 'application/json'}

        self.dir = '/home/mcafee/mvision_logs/logs/' #Directory to where the logs should be stored

        now = datetime.utcnow()
        self.nowiso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        past = now - timedelta(minutes=5) #Change Timeframe e.g. 5 minutes go back in time
        self.pastiso = past.strftime("%Y-%m-%dT%H:%M:%SZ")

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

        r = requests.get(self.event_url + '?since={0}&until={1}'.format(self.pastiso,self.nowiso), headers= self.headers)
        evts = r.json()
        return(evts)

    def write(self, evts):
        i = 0

        for event in evts['Events']:
            file = open(self.dir + str(i) + '.json', 'w')
            file.write(json.dumps(event))
            file.close()
            i+=1

if __name__ == '__main__':

    mepo = MEPO()
    mepo.auth()
    events = mepo.events()

    mepo.write(events)
    print(mepo.nowiso + ': Successfully pulled logs from MVISION ePO')