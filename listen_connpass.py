# -*- coding: utf-8 -*-
import requests
import json
import datetime
import pprint

CONNPASS_API = 'https://connpass.com/api/v1/event/'


def get_connpass_events(started_month: int, keyword: list, count=10):
    payload_tokyo = {
        'ym': started_month,
        'keyword': keyword,
        'count':count,
    }
    response_data = requests.get(CONNPASS_API, payload_tokyo)

    if response_data.status_code == 200:
        events = response_data.json()['events']
        event_urls = [event['event_url'] for event in events]
        print(event_urls)
        pprint.pprint(events[0])
        start_at = datetime.datetime.strptime(events[0]['started_at'], "%Y-%m-%dT%H:%M:%S+09:00")
        print(start_at)


get_connpass_events(201906, ['東京', 'python'])
