import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs


def get_soup(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
    }
    html = requests.get(url, headers=headers)
    if html.status_code != 200:
        print(url, ' is ', html.status_code)
        return html.status_code
    soup = bs(html.content, 'html.parser')
    return soup


def post_soup(url, params):
    html = requests.post(url, data=params)
    if html.status_code != 200:
        print(url, ' is ', html.status_code)
        return html.status_code
    soup = bs(html.content, 'html.parser')
    return soup


def trim_text(_text):
    for a in ['\n', u'\xa0', '\t', '\r', '  ']:
        _text = _text.replace(a, '')
    return _text

def time_check(meta_data, day):
    until_date = datetime.strptime(day, '%Y-%m-%d')
    for m in meta_data:
        new_date = datetime.strptime(m['day'], '%Y-%m-%d')
        if until_date > new_date:
            return True
    return False

