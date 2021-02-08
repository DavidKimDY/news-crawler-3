import json
import os
import random
from datetime import datetime
import requests
import asyncio
from bs4 import BeautifulSoup as bs
from NewsCrawler3.text_extractor import text_extractor


def get_soup(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
    }
    html = requests.get(url, headers=headers)
    if html.status_code != 200:
        print(' html.status_code : ', html.status_code)
        bypass_url, headers = bypassed_url(url)
        html = requests.get(url, headers=headers)
    soup = bs(html.content, 'html.parser')
    return soup


def post_soup(url, params):
    html = requests.post(url, data=params)
    if html.status_code != 200:
        print(url, ' is ', html.status_code)
        return html.status_code
    soup = bs(html.content, 'html.parser')
    return soup


def trim_text(text):
    for a in ['\n', u'\xa0', '\t', '\r', '  ']:
        if a == u'\xa0':
            text = text.replace(a, ' ')
        else:
            text = text.replace(a, '')
    return text


def time_check(meta, input_date):
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    for m in meta:
        new_date = datetime.strptime(m['day'], '%Y-%m-%d')
        if input_date > new_date:
            return True
    return False


def bypassed_url(url):
    with open('../NewsCrawler3/api_key.txt', 'r') as f:
        api_key = f.read()
    crawler_url = "https://crawler.roa.ai/html/requests/" + str(random.randrange(1, 6))
    headers = {
        "url": url,
        "api-key": api_key
    }
    return crawler_url, headers


def sync_get(meta):
    corp = meta['corp']
    day = meta['day']
    url = meta['url']
    soup = get_soup(url)
    text = text_extractor(corp, soup)
    text = trim_text(text)
    return {'url': url, 'day': day, 'text': text}


async def sync_to_async_request(metadata):
    tasks = []
    loop = asyncio.get_event_loop()
    for data in metadata:
        task = loop.run_in_executor(None, sync_get, data)
        tasks.append(task)
    return await asyncio.gather(*tasks)


def text_crawler(metadata):
    all_text = []
    start = 0
    end = start + 100
    while start < len(metadata):
        hundred_of_meta = metadata[start: end]
        print(end)
        try:
            text_data = asyncio.run(sync_to_async_request(metadata=hundred_of_meta))
        except:
            end -= 10
            if end - start == 0:
                raise Exception('Async Error maybe I do not know')
        else:
            all_text.extend(text_data)
            start = end
            end = start + 100

    return all_text


def get_rid_of_outdated(meta, input_date):
    new_data = []
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    for m in meta:
        new_date = datetime.strptime(m['day'], '%Y-%m-%d')
        if new_date < input_date:
            continue
        else:
            new_data.append(m)
    return new_data


def get_rid_of_duplicated(meta):
    new_data = []
    set_of_urls = set([m['url'] for m in meta])
    for url in set_of_urls:
        for m in meta:
            if m['url'] == url:
                new_data.append(m)
                break
    return new_data


def save_meta(meta, corp):
    for m in meta:
        day = m['day']
        file_name = day + '.json'
        if os.path.isfile(f'new_dataset/{corp}/{file_name}'):
            with open(f'new_dataset/{corp}/{file_name}', 'r', encoding='utf-8') as f:
                meta_file = json.load(f)
        else:
            meta_file = []
        meta_file.append(m)
        meta_data = get_rid_of_duplicated(meta_file)
        with open(f'new_dataset/{corp}/{file_name}', 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, ensure_ascii=False, indent='\t')

def save_error_text(wrong_text, news_site):
    path = f'data/{news_site}_error.json'
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            error_data = json.load(f)
    else:
        error_data = []
    error_data.extend(wrong_text)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(error_data, f, ensure_ascii=False, indent='\t')

def check_text_validity(text_data, news_site):
    wrong_text = []
    for t in text_data:
        text = t['text']
        if len(text) < 10:
            wrong_text.append(t)
    for s in wrong_text:
        text_data.remove(s)
    save_error_text(wrong_text, news_site)
    return text_data

