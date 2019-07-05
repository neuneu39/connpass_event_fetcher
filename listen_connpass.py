# -*- coding: utf-8 -*-
import requests
import time

CONNPASS_API = 'https://connpass.com/api/v1/event/'


class ConnpassEvent:

    def __init__(self, started_month: int, keyword: list, count=15):
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
        print('getting event data from connpass')
        time.sleep(2)
        if response_data.status_code == 200:
            events = response_data.json()['events']
            print('対象のイベントは', response_data.json()['results_returned'])
            return events
