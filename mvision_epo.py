# written by mohlcyber - v.0.2 - 16.04.2021
# Script to pull Events from MVISION EPO

import json
import requests
import getpass
import logging
import sys

from datetime import datetime, timedelta
from argparse import ArgumentParser, RawTextHelpFormatter


class MEPO():

    def __init__(self):
        self.logger = logging.getLogger('logs')
        self.logger.setLevel('DEBUG')
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.auth_url = 'https://iam.mcafee-cloud.com/iam/v1.0/token'
        if args.region == 'US':
            self.base = 'arevents.mvision.mcafee.com'
        elif args.region == 'SI':
            self.base = 'areventssgp.mvision.mcafee.com'
        elif args.region == 'EU':
            self.base = 'areventsfrk.mvision.mcafee.com'
        elif args.region == 'SY':
            self.base = 'areventssyd.mvision.mcafee.com'

        self.user = args.user
        self.pw = args.pw

        # Login to the MVISION EPO console and open a new tab
        # go to https://auth.ui.mcafee.com/support.html to retrieve your client_id
        self.client_id = '0oae8q9q2y0IZOYUm0h7'

        self.scope = 'epo.evt.r dp.im.r'

        headers = {'Accept': 'application/json'}

        self.session = requests.Session()
        self.session.headers = headers

        self.auth()

    def auth(self):
        data = {
            "username": self.user,
            "password": self.pw,
            "client_id": self.client_id,
            "scope": self.scope,
            "grant_type": "password"
        }

        res = requests.post(self.auth_url, data=data)
        if res.ok:
            token = res.json()['access_token']
            self.session.headers.update({'Authorization': 'Bearer ' + token})
            self.logger.info('Successfully authenticated.')
        else:
            self.logger.error('Could not authenticate. {0} - {1}'.format(str(res.status_code), res.text))
            sys.exit()

    def events(self):
        now = datetime.utcnow()
        nowiso = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

        past = now - timedelta(minutes=args.minutes)
        pastiso = past.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

        params = {
            'type': 'all',  # threats, incidents (dlp), all
            'since': pastiso,
            'until': nowiso,
            'limit': str(args.limit)
        }

        res = self.session.get('https://{0}/eventservice/api/v2/events'.format(self.base), params=params)

        if res.ok:
            self.logger.info('Successfully retrieved MVISION EPO Events.')
            self.logger.info(json.dumps(res.json()))
            return res.json()
        else:
            self.logger.error('Could not retrieve MVISION EPO Events. {0} - {1}'.format(str(res.status_code), res.text))
            sys.exit()

    def write(self, evts):
        i = 0
        for event in evts['Events']:
            file = open(str(i) + '.json', 'w')
            file.write(json.dumps(event))
            file.close()
            i += 1

    def main(self):
        evt = self.events()
        if args.file == 'Y':
            self.write(evt)


if __name__ == '__main__':

    usage = """python3 mvision_epo.py -R <Region> -U <User> -M <Minutes> -L <Limit> -F <File>"""
    title = 'McAfee MVISION EPO Events Pull'
    parser = ArgumentParser(description=title, usage=usage, formatter_class=RawTextHelpFormatter)

    parser.add_argument('--region', '-R',
                        required=True, type=str, choices=['US', 'SI', 'EU', 'SY'],
                        help='McAfee MVISION Tenant Region')

    parser.add_argument('--user', '-U',
                        required=True, type=str,
                        help='McAfee MVISION EPO Username')

    parser.add_argument('--pw', '-P',
                        required=False, type=str,
                        help='McAfee MVISION EPO Password')

    parser.add_argument('--minutes', '-M',
                        required=True, type=int, default=None,
                        help='Pull MVISION EPO Events from the last x Minutes')

    parser.add_argument('--limit', '-L', required=True,
                        type=int, help='Maximum Events to retrieve')

    parser.add_argument('--file', '-F', required=False,
                        type=str, default='N', choices=['Y', 'N'],
                        help='Write output to file')

    args = parser.parse_args()
    if not args.pw:
        args.pw = getpass.getpass(prompt='McAfee MVISION EPO Password: ')

    MEPO().main()
