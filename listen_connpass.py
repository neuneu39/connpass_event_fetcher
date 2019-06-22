# -*- coding: utf-8 -*-
import requests
import json
import datetime
import pprint

CONNPASS_API = 'https://connpass.com/api/v1/event/'

class ConnpassEvent:

    def __init__(self, started_month: int, keyword: list, count=10):
        self.started_month = started_month
        self.keyword = keyword
        self.count = count

    def get_connpass_events(self):
        payload_tokyo = {
            'ym': self.started_month,
            'keyword': self.keyword,
            'count': self.count,
        }
        response_data = requests.get(CONNPASS_API, payload_tokyo)

        if response_data.status_code == 200:
            events = response_data.json()['events']
            event_urls = [event['event_url'] for event in events]
            print(event_urls)
            pprint.pprint(events[0])
            start_at = datetime.datetime.strptime(events[0]['started_at'], "%Y-%m-%dT%H:%M:%S+09:00")
            print(start_at)
            return events[0]

# get_connpass_events(201906, ['東京', 'python'])
