import json
import os
import random
from datetime import datetime
import requests
import asyncio
from bs4 import BeautifulSoup as bs

from text_extractor import text_extractor


def get_soup(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
    }
    html = requests.get(url, headers=headers)
    if html.status_code != 200:
        print('html.status_code : ', html.status_code)
        bypass_url, headers = bypassed_url(url)
        html = requests.get(bypass_url, headers=headers)
        soup = bs(json.loads(html.content), 'html.parser')
        return soup

    soup = bs(html.content, 'html.parser')
    return soup


def post_soup(url, data):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
    }
    html = requests.post(url, data=data, headers=headers)
    if html.status_code != 200:
        print(url, ' is ', html.status_code)
        return html.status_code
    soup = bs(html.content, 'html.parser')
    return soup


def trim_text(text):
    if text is None:
        return None
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


def sync_get(meta, post_data):
    corp = meta['corp']
    day = meta['day']
    url = meta['url']
    if post_data is None:
        soup = get_soup(url)
    else:
        soup = post_soup(url, post_data)
    text = text_extractor(corp, soup)
    text = trim_text(text)
    return {'url': url, 'day': day, 'text': text}


async def sync_to_async_request(metadata, post_data):
    tasks = []
    loop = asyncio.get_event_loop()
    for meta in metadata:
        task = loop.run_in_executor(None, sync_get, meta, post_data)
        tasks.append(task)
    return await asyncio.gather(*tasks)


def text_crawler(metadata, post_data):
    all_text = []
    start = 0
    end = start + 100
    while start < len(metadata):
        hundred_of_meta = metadata[start: end]
        print(end)
        try:
            text_data = asyncio.run(sync_to_async_request(metadata=hundred_of_meta, post_data=post_data))
        except:
            end -= 10
            if end - start <= 50:
                print('!!!! Sync crawling !!!!')  # delete
                all_text = text_crawler_sync(metadata, post_data)
        else:
            all_text.extend(text_data)
            start = end
            end = start + 100

    return all_text

def text_crawler_sync(metadata, post_data):
    text_data_list = []
    for meta in metadata:
        text_data = sync_get(meta, post_data)
        text_data_list.append(text_data)
    return text_data_list


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


def save_data(meta, news_site, text=False):
    if not os.path.isdir(f'data/news_data/{news_site}'):
        os.mkdir(f'data/news_data/{news_site}')
    if text:
        surfix = '_text.json'
    else:
        surfix = '.json'
    for m in meta:
        day = m['day']
        file_name = day + surfix
        if os.path.isfile(f'data/news_data/{news_site}/{file_name}'):
            with open(f'data/news_data/{news_site}/{file_name}', 'r', encoding='utf-8') as f:
                meta_file = json.load(f)
        else:
            meta_file = []
        meta_file.append(m)
        meta_data = get_rid_of_duplicated(meta_file)
        with open(f'data/news_data/{news_site}/{file_name}', 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, ensure_ascii=False, indent='\t')


def merge_error_data(wrong_meta, wrong_text):
    wrong_data = []

    for m in wrong_meta:
        meta_url = m['url']
        for t in wrong_text:
            text_url = t['url']
            if meta_url == text_url:
                m['text'] = t['text']
                wrong_data.append(m)
                break
    return wrong_data


def save_error_data(wrong_meta, wrong_text, news_site):
    if len(wrong_text) == 0:
        return None
    path = f'data/error_data/{news_site}_error.json'
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            error_data = json.load(f)
    else:
        error_data = []
    wrong_data = merge_error_data(wrong_meta, wrong_text)
    error_data.extend(wrong_data)
    error_data = get_rid_of_duplicated(error_data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(error_data, f, ensure_ascii=False, indent='\t')


def filter_wrong_data(meta_data, text_data, news_site):

    wrong_text, text_data = filter_wrong_text(text_data)
    wrong_meta, meta_data = filter_wrong_meta(meta_data, wrong_text)

    save_error_data(wrong_meta, wrong_text, news_site)

    return meta_data, text_data


def filter_wrong_meta(meta_data, wrong_text):
    wrong_meta = []
    for t in wrong_text:
        url = t['url']
        for m in meta_data:
            if url == m['url']:
                wrong_meta.append(m)
                break
    for w in wrong_meta:
        meta_data.remove(w)
    return wrong_meta, meta_data


def filter_wrong_text(text_data):
    wrong_text = []
    for t in text_data:
        text = t['text']
        if text is None or len(text) < 20:
            wrong_text.append(t)
    for s in wrong_text:
        text_data.remove(s)
    return wrong_text, text_data


def update_time_stamp(meta_data, time_stamp, news_site):
    if len(meta_data) == 0:
        return None
    latest_day = sorted([m['day'] for m in meta_data])[-1]
    time_stamp[news_site] = latest_day
    with open('time_stamp.json', 'w') as f:
        json.dump(time_stamp, f, indent='\t')

