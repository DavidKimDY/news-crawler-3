# -*- coding: utf-8 -*-
import re
import string
import json
from datetime import datetime
from random import randrange

import requests
from bs4 import BeautifulSoup as bs

#from NewsCrawler3.util import *
from util import *
# from util import *

class Website():

    def crawler(self):
        page_number = 1
        all_meta_data = []
        while True:
            menu_url = self.base_page.format(page_number=page_number)
            soup = get_soup(menu_url)
            meta_data = self.data_maker(soup)
            all_meta_data.extend(meta_data)
            stop_sign = time_check(meta_data, self.input_date)
            if stop_sign:
                break
            page_number += 1

        return all_meta_data

    def crawler_by_category(self, category, input_date):
        page_number = 1
        category_meta_data = []
        while True:
            menu_url = self.base_page.format(page_number=page_number, category=category)
            soup = get_soup(menu_url)
            meta_data = self.data_maker(soup)
            category_meta_data.extend(meta_data)
            stop_sign = time_check(meta_data, input_date)
            if stop_sign:
                break
            page_number += 1

        return category_meta_data

# Tested
class Vrn(Website):

    def __init__(self, input_date):
        self.corp = 'VRN'
        self.base_page = 'http://www.vrn.co.kr/news/articleList.html?page={page_number}&sc_order_by=E&view_type=sm'
        self.page_head = 'http://www.vrn.co.kr'
        self.input_date = input_date
        self.meta_data = []

    def parse_title(self, _title):
        return _title.text

    def parse_url(self, _url):
        url = _url.attrs['href']
        url = self.page_head + url
        return url

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['style']
        thumb = thumb.split('./')[-1].strip(')')
        thumb = self.page_head + '/news/' + thumb
        return thumb

    def parse_day(self, _day):
        day = _day.text.split()
        day = day[-2]
        return day

    def parse_cat(self, _cat):
        cat = _cat.text.split()
        cat = cat[0]
        return cat

    def parse_time(self, _time):
        time = _time.text.split()
        time = time[-1]
        return time

    def data_maker(self, soup):

        meta_data = []

        title = soup.select('.list-titles')
        day = soup.select('.list-dated')
        url = soup.select('.list-titles a')
        time = soup.select('.list-dated')
        thumb = soup.select('.list-image')
        category = soup.select('.list-dated')

        for tt, da, ur, ti, th, ca in zip(title, day, url, time, thumb, category):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['time'] = self.parse_time(ti)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data





# Tested
class Besuccess(Website):

    def __init__(self, input_date):
        self.corp = 'besuccess'
        self.base_page = 'https://besuccess.com/page/{page_number}/'
        self.page_head = 'https://besuccess.com'
        self.input_date = input_date
        

    def parse_url(self, _url):
        return self.page_head + _url.attrs['href']

    def parse_title(self, _title):
        return _title.text

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['style']
        thumb = re.sub('.*\(', '', thumb)
        thumb = thumb.strip(')')
        return thumb

    def parse_cat(self, _cat):
        cats = _cat.find_all('div')
        cats = [cat.text for cat in cats]
        return cats

    def parse_day(self, _day):
        day = _day.text
        day = day.strip(string.whitespace)
        day = re.sub('[^0-9 ]*', '', day)
        day = day.replace('  ', '')
        day = day.replace(' ', '-')
        return day

    def data_maker(self, soup):

        meta_data = []

        title = soup.find_all('a', {'id': 'title'})
        day = soup.find_all('div', {'id': 'writer'})
        url = soup.find_all('a', {'id': 'title'})
        thumb = soup.find_all('div', {'id': 'image'})
        category = soup.find_all('div', {'id': 'tag_container'})

        for tt, da, ur, th, ca in zip(title, day, url, thumb, category):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data


# Tested
class Bikorea(Website):

    def __init__(self, input_date):
        self.base_page='http://www.bikorea.net/news/articleList.html?page={page_number}&total=27604&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=I&view_type=sm'
        self.page_head='http://www.bikorea.net/news/'
        self.corp='BI KOREA'
        self.input_date = input_date
        

    def parse_title(self, _title):
        return _title.text

    def parse_day(self, _day):
        return _day.text

    def parse_url(self, _url):
        url = str(_url).split('\"')[1]
        url = self.page_head + url
        return url

    def parse_thumb(self, _thumb):
        try:
            thumb = _thumb.previous_sibling.previous_sibling.select('img')
        except AttributeError:
            return None
        thumb = str(thumb)
        thumb = thumb.split('\"')[1].strip('./')
        thumb = self.page_head + thumb
        return thumb

    def parse_cat(self, _cat):
        return _cat.previous_sibling.previous_sibling.text

    def data_maker(self, soup):

        meta_data = []

        title = soup.select('.ArtList_Title a')
        day = soup.select('.FontEng')
        url = soup.select('.ArtList_Title a')
        thumb = soup.select('.ArtList_Title')
        category = soup.select('.ArtList_Title a')

        for tt, da, ur, th, ca in zip(title, day, url, thumb, category):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data


# Tested (Bypassed ip worked well)
class Bizwatch(Website):

    def __init__(self, input_date):
        self.base_page='http://news.bizwatch.co.kr/search/news/{page_number}'
        self.corp='bizwatch'
        self.input_date = input_date

    def parse_title(self, _title):
        return _title.text

    def parse_cat(self, _cat):
        category = {'finance': '경제',
                    'market': '증권',
                    'mobile': '모바일경제',
                    'real_estate': '부동산',
                    'industry': '산업',
                    'consumer': '생활경제',
                    'opinion': '사설',
                    'policy': '정책',
                    'tax': '세금'}

        cat = _cat.attrs['href']
        cat = cat.split('/')[4]
        return category.get(cat, 'No need')

    def parse_url(self, _url):
        url = _url.next
        url = url.attrs['href']
        url = 'http:' + url
        return url

    def parse_day(self, _day):
        day = _day.text
        day = day.split('(')[0]
        day = day.replace('.', '-')
        return day

    def parse_time(self, _time):
        return _time.text

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['src']
        thumb = 'http:' + thumb
        return thumb

    def data_maker(self, soup):

        meta_data = []

        title = soup.select('.all_news .title')
        day = soup.select('.date')
        url = soup.select('.all_news .title')
        time = soup.select('.time')
        thumb = soup.select('.all_news img')
        category = soup.select('.all_news a')

        for tt, da, ur, th, ca, ti in zip(title, day, url, thumb, category, time):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['time'] = self.parse_title(ti)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data




# Tested (Bypassed ip workded well)
class Hellodd(Website):

    def __init__(self, input_date):
        self.base_page = 'https://www.hellodd.com/news/articleList.html?page={page_number}&view_type=sm'
        self.page_head = 'https://www.hellodd.com'
        self.corp = '헬로디디'
        self.input_date = input_date

    def parse_thumb(self, source):
        img_tag = source.a.img
        if img_tag is None:
            return ''
        elif img_tag.attrs['src'] is None:
            return ''
        else:
            return img_tag.attrs['src']

    def parse_title(self, source):
        source.find_all('h4', {'class': 'titles'})
        return source.text

    def parse_url(self, source):
        return self.page_head + source.a.attrs['href']

    def parse_time(self, source):
        date_time = source.find_all('em')[-1].text
        date, time = date_time.split()
        return time

    def parse_day(self, source):
        date_time = source.find_all('em')[-1].text
        date, time = date_time.split()
        date = date.replace('.', '-')
        return date

    def parse_cat(self, source):
        cat = source.find_all('em')[0].text
        return cat

    def data_maker(self, soup):

        source = soup.find('section', {'id': "section-list"})
        meta_data = []

        title = source.find_all('h4', {'class': 'titles'})
        day = source.find_all('span', {'class': 'byline'})
        url = source.find_all('h4', {'class': 'titles'})
        time = source.find_all('span', {'class': 'byline'})
        thumb = source.find_all('li')
        category = source.find_all('span', {'class': 'byline'})

        for tt, da, ur, th, ca, ti in zip(title, day, url, thumb, category, time):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['time'] = self.parse_title(ti)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data


# Tested
class Itchosun(Website):

    def __init__(self, input_date):
        self.base_page = 'http://it.chosun.com/svc/list_in/list.html?pn={page_number}'
        self.page_head = 'http://it.chosun.com'
        self.corp = 'IT CHOSUN'
        self.input_date = input_date

    def parse_title(self, _title):
        title = str(_title)
        title = title.split('\">')[-1].split('<')[0]
        return title

    def parse_thumb(self, _thumb):
        thumb = _thumb.previous.previous.attrs
        thumb = thumb.get('src', None)
        return thumb

    def parse_url(self, _url):
        url = _url.find('a').attrs['href']
        return url

    def new_date(self, url_soup):
        datetime = url_soup.select('.news_date')[0].text
        day = datetime.split()[1].replace('.', '-')
        time = datetime.split()[2].strip('\r\n')
        return day, time

    def parse_day_time(self, soup):

        if not soup.title:
            return None, None
        published_time = soup.find('meta', property='dd:published_time')
        if not published_time:
            published_time = soup.find('meta', property='article:published_time')
            if not published_time:
                day, time = self.new_date(soup)
                return day, time

        time = str(published_time.attrs['content'])
        time = time.split('T')[1].split('+')[0]

        day = str(published_time.attrs['content'])
        day = day.split('T')[0].split('+')[0].split('+')[0]

        return day, time


    def parse_tag(self, _tag):
        tag = _tag.find('div', class_='right')
        if tag:
            tag = str(tag.text)
            tag = tag.strip().replace('#', '').split('\n')
            return tag
        else:
            return None

    def parse_cat(self, soup):

        if not soup.head:
            return ['', '']

        categories = soup.head.title.text.split(' > ')
        cat1 = categories[-2]
        cat2 = categories[-1]

        if cat2 in ['동영상', '전체 기사', '기업', '자동차', '기술', '게임·라이프', '사람', '칼럼·해설', '뉴스']:
            category = [cat2, '']
        else:
            category = [cat1, cat2]

        return category

    def data_maker(self, soup):

        meta_data = []

        title = soup.select('.tt')
        url = soup.find_all('div', class_='txt_wrap')
        thumb = soup.find_all('div', class_='txt_wrap')
        tag = soup.find_all('div', class_='info')

        for tt, ur, th, tg in zip(title, url, thumb, tag):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['tag'] = self.parse_tag(tg)
            soup = get_soup(data['url'])
            day, time = self.parse_day_time(soup)
            data['day'] = day
            data['time'] = time
            data['category'] = self.parse_cat(soup)
            meta_data.append(data)

        return meta_data


# Tested
class Itdonga(Website):

    def __init__(self, input_date):
        self.base_page = 'https://it.donga.com/news/?page={page_number}'
        self.page_head = 'https://it.donga.com'
        self.corp = "IT동아"
        self.input_date = input_date

    def parse_title(self, _title):
        title = str(_title.text)
        title = title.split('\n')[1].strip()
        return title

    def parse_thumb(self, _thumb):
        thumb = str(_thumb)
        thumb = thumb.split('\"')[5]
        thumb = self.page_head + thumb
        return thumb

    def parse_day(self, _day):
        day = _day.text
        day = day.replace('.', '-').rstrip('-')
        return day

    def parse_url(self, _url):
        url = _url.attrs['href']
        url = self.page_head + url
        return url

    def data_maker(self, soup):

        meta_data = []

        title = soup.select('.mt-0')
        day = soup.find_all('time')
        url = soup.find_all('a', class_='media')
        thumb = soup.select('.media img')

        for tt, da, ur, th in zip(title, day, url, thumb):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            meta_data.append(data)

        return meta_data


# Tested
class Klnews(Website):

    def __init__(self, input_date):
        self.base_page = 'http://www.klnews.co.kr/news/articleList.html?page={page_number}&total=57525&&sc_order_by=E&view_type=sm'
        self.page_head = 'http://www.klnews.co.kr'
        self.corp = '물류신문'
        self.input_date = input_date

    def parse_title(self, source):
        title = source.text
        for x in [u'\xa0', u'\u200b']:
            title = title.replace(x, '')
        return title

    def parse_thumb(self, _thumb):
        try:
            thumb = _thumb.img['src']
            thumb = thumb
            return thumb
        except:
            return None

    def parse_url(self, _url):
        url = _url.attrs['href']
        url = self.page_head + url
        return url

    def parse_time(self, source):
        return source.find_all('em')[-1].text.split()[-1]

    def parse_cat(self, source):
        return source.find('em').text

    def parse_day(self, source):
        return source.find_all('em')[-1].text.split()[0].replace('.', '-')


    def data_maker(self, soup):
        soup = soup.find('section', {'id': 'section-list'})
        meta_data = []

        title = soup.find_all('h4', {'class': 'titles'})
        day = soup.find_all('span', {'class': 'byline'})
        url = soup.find_all('a', {'class': 'thumb'})
        thumb = soup.find_all('a', {'class': 'thumb'})
        category = soup.find_all('span', {'class': 'byline'})
        time = soup.find_all('span', {'class': 'byline'})

        for tt, da, ur, th, ca, ti in zip(title, day, url, thumb, category, time):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['time'] = self.parse_time(ti)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data


# Tested
class Sciencetimes(Website):

    def __init__(self, input_date):
        self.base_page = 'https://www.sciencetimes.co.kr/category/sci-tech/page/{page_number}/'
        self.corp = 'sciencetimes'
        self.input_date = input_date
        self.no_cat = []

    def parse_thumb(self, _thumb):
        thumb = _thumb.previous.previous
        thumb = thumb.previous.previous
        try:
            thumb = thumb.attrs['style']
            thumb = re.sub('.*\(\'', '', thumb)
            thumb = thumb.strip('\');')
        except Exception as e:
            thumb = ''
        return thumb

    def parse_cat(self, _cat):
        cat_list = {'133': '자연,환경,에너지', '128': '기초,응용과학',
                    '16933': 'ICT,로봇', '130': '보건,의학',
                    '132': '항공,우주', '134': '신소재,신기술'}
        cat = _cat.previous.previous
        cat = cat.find('a')
        cat = cat.attrs['href']
        cat = cat.split('cat=')[-1]
        try:
            cat = cat_list[cat]
        except Exception as e:
            title = self.parse_title(_cat)
            obj = {'title': title, 'cat': cat}
            self.no_cat.append(obj)
        return cat

    def parse_url(self, _url):
        url = _url.previous.previous
        url = url.find('a')
        url = url.attrs['href']
        return url

    def parse_title(self, _title):
        title = _title.previous.previous
        title = title.find('strong').text
        return title

    def parse_day_time(self, url):
        html = requests.get(url)
        soup = bs(html.content, 'html.parser')
        day_time = soup.find('em', {'class': 'date'}).text
        day = day_time.split()[0].replace('.', '-')
        time = day_time.split()[1]
        return day, time

    def data_maker(self, soup):
        meta_data = []

        title = soup.find_all('span', {'class': 'cate'})
        url = soup.find_all('span', {'class': 'cate'})
        thumb = soup.find_all('span', {'class': 'cate'})
        category = soup.find_all('span', {'class': 'cate'})

        for tt, ur, th, ca in zip(title, url, thumb, category):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            day, time = self.parse_day_time(data['url'])
            data['day'] = day
            data['time'] = time
            meta_data.append(data)

        return meta_data


# Tested
class Venturesquare(Website):
    def __init__(self, input_date):
        self.base_page = 'https://www.venturesquare.net/news/page/{page_number}'
        self.corp = '벤처스퀘어'
        self.input_date = input_date

    def parse_title(self, _title):
        title = _title.attrs['title']
        return title

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['src']
        return thumb

    def parse_url(self, _url):
        url = _url.attrs['href']
        return url

    def parse_cat(self, _cat):
        return _cat.text

    def parse_day_time(self, _datetime):
        datetime = _datetime.attrs['datetime']
        day = datetime.split('T')[0]
        time = datetime.split('T')[1].split('+')[0]
        return day, time

    def parse_day(self, source):
        day, time = self.parse_day_time(source)
        return day

    def parse_time(self, source):
        day, time = self.parse_day_time(source)
        return time

    def data_maker(self, soup):
        meta_data = []

        title = soup.select('.post-wrap img')
        day = soup.find_all('time')
        url = soup.select('.image-link')
        thumb = soup.select('.post-wrap img')
        category = soup.find_all('span', class_="cat-title")
        time = soup.find_all('time')

        for tt, da, ur, th, ca, ti in zip(title, day, url, thumb, category, time):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['time'] = self.parse_time(ti)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data


# Need to test!! (categorical)
class Platum(Website):

    def __init__(self, input_date):
        
        self.base_page='https://platum.kr/{category}/page/{page_number}'
        self.corp='platum'
        self.category=['entrepreneur', 'startup', 'china', 'trends', 'workinsight', 'marketing', 'business',
                  'event', 'all-tech-korea', 'report', 'blockchain', 'startup-3']

        self.category_to_input = {
            'entrepreneur': 'Entrepreneur', 'startup': 'Startup', 'china': 'China', 'trends': 'Trends',
            'workinsight': 'Workinsight', 'marketing': 'Marketing', 'business': 'Business',
            'event': 'Event', 'all-tech-korea': 'ALL TECH KOREA', 'report': 'Report',
            'blockchain': 'Blockchain', 'startup-3': 'Main'
        }
        self.input_date = input_date

    def parse_title(self, _title):
        return _title.text

    def parse_url(self, _url):
        return _url.attrs['href']

    def parse_day(self, _day):
        day = _day.text.split()
        day = day[-1]
        day = day.replace('/', '-')
        return day

    def parse_thumb(self, _thumb):
        try:
            thumb = _thumb.find('div', class_='post_img').img.attrs['src']
        except AttributeError:
            thumb = None

        return thumb

    def parse_cat(self, _cat):
        return [cat.text for cat in _cat.find_all('a')]

    def data_maker(self, soup):
        meta_data = []

        title = soup.select('.post_header_title h5 a')
        day = soup.select('.post_info_date')
        url =  soup.select('.post_header_title h5 a')
        thumb = soup.find_all(class_='post_header')
        category = soup.select('.post_info_cat')[1:]

        for tt, da, ur, th, ca in zip(title, day, url, thumb, category):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = self.parse_cat(ca)
            meta_data.append(data)

        return meta_data

    def crawler(self):
        all_meta_data = []
        for cat in self.category:
            input_date = self.input_date
            category_meta_data = self.crawler_by_category(cat, input_date)
            all_meta_data.extend(category_meta_data)
        return all_meta_data


# Need to test!! (categorical)
class Clo(Website):
    def __init__(self, input_date):
        
        self.base_page = 'http://clomag.co.kr/magazine?category={category}&page={page_number}'
        self.category = ['CAST', 'INSIGHT']
        self.corp = 'CLO'
        self.CLO_THUMB = '/assets/article_sample-df281dcfbf04fe603f349f9cca65bea16660bc88ff86e733a4ccc53a9e3faf07.png'
        self.input_date = input_date

    def parse_title(self, _title):
        title = _title.text
        title = title.replace('\u200b', '')
        return title

    def parse_tag(self, _tag):
        tags = _tag.text
        tags = tags.split('\n')[2::3]
        tag = [tag.strip() for tag in tags]
        return tag

    def parse_url(self, _url):
        url = _url.attrs['href']
        return url

    def parse_day(self, _day):
        day = _day.text
        pieces = day.split()
        y = pieces[0][:4]
        m = pieces[1][:2]
        d = pieces[2][:2]
        return f'{y}-{m}-{d}'

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['src']
        if thumb == self.CLO_THUMB:
            return None
        else:
            return 'http:' + thumb

    def data_maker(self, soup, category):
        meta_data = []

        title = soup.select('.title')
        day = soup.select('.date')
        url = soup.select('.cover a')
        thumb = soup.select('.img-responsive')
        tag = soup.select('.tags')

        for tt, da, ur, th, tg in zip(title, day, url, thumb, tag):
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(tt)
            data['day'] = self.parse_day(da)
            data['url'] = self.parse_url(ur)
            data['thumb'] = self.parse_thumb(th)
            data['category'] = category
            data['tag'] = self.parse_tag(tg)
            meta_data.append(data)

        return meta_data

    def crawler_by_category(self, category, input_date):
        page_number = 1
        category_meta_data = []
        while True:
            menu_url = self.base_page.format(page_number=page_number, category=category)
            soup = get_soup(menu_url)
            meta_data = self.data_maker(soup, category)
            category_meta_data.extend(meta_data)
            stop_sign = time_check(meta_data, input_date)
            if stop_sign:
                break
            page_number += 1

        return category_meta_data

    def crawler(self):
        all_meta_data = []
        for cat in self.category:
            category_meta_data = self.crawler_by_category(cat, self.input_date)
            all_meta_data.extend(category_meta_data)
        return all_meta_data

# Need to test!! (categorical)
class Ainews(Website):

    def __init__(self, input_date):
        
        self.corp='인공지능신문'
        self.base_page='http://www.aitimes.kr/news/articleList.html?page={page_number}&total=971&sc_section_code=S1N{category}&sc_order_by=E&view_type=sm'
        self.page_head='http://www.aitimes.kr'
        self.category=[2, 3, 4, 5, 6]
        self._category = {2: 'AI Tech', 3: 'Focus', 4: 'AI Industry', 5: 'Today', 6: 'Opinion'}
        self.input_date = input_date

    def parse_title(self, _title):
        title = _title.find('h4', {'class': 'titles'}).text.replace(u'\xa0', '')
        return title

    def parse_url(self, _url):
        url = _url.a.attrs['href']
        url = self.page_head + url
        return url

    def parse_thumb(self, _thumb):
        thumb = _thumb.img.attrs['src']
        thumb = self.page_head + '/news' + thumb
        return thumb

    def parse_cat(self, _cat, category):
        cat = _cat.span.find_all('em')
        cat = cat[0].text
        main_category = self._category[category]
        return [main_category, cat]

    def parse_day(self, url):
        soup = get_soup(url)
        date = soup.find('meta', {'property' : "article:published_time"}).attrs['content']
        date = date.split('T')[0]
        return date

    def parse_time(self, _time):
        time = _time.span.find_all('em')
        time = time[2].text.split()[1]
        return time

    def data_maker(self, soup, category):
        meta_data = []
        base = soup.find('section', {'id': 'section-list'}).find_all('li')

        for bs in base:
            data = {}
            data['corp'] = self.corp
            data['title'] = self.parse_title(bs)
            data['url'] = self.parse_url(bs)
            data['day'] = self.parse_day(data['url'])
            data['thumb'] = self.parse_thumb(bs)
            data['category'] = self.parse_cat(bs, category)
            meta_data.append(data)

        return meta_data

    def crawler_by_category(self, category, input_date):
        page_number = 1
        category_meta_data = []
        while True:
            menu_url = self.base_page.format(page_number=page_number, category=category)
            soup = get_soup(menu_url)
            meta_data = self.data_maker(soup, category)
            category_meta_data.extend(meta_data)
            stop_sign = time_check(meta_data, input_date)
            if stop_sign:
                break
            page_number += 1

        return category_meta_data

    def crawler(self):
        all_meta_data = []
        for cat in self.category:
            category_meta_data = self.crawler_by_category(cat, self.input_date)
            all_meta_data.extend(category_meta_data)
        return all_meta_data


# Need to test!! (Post)
class Itnews(Website):

    def __init__(self, input_date):
        self.input_date = input_date
        self.log = ['coredottoday', 'coredottoday2']
        self.ID_PARAMS = {'log': self.log[1],
                     'pwd': 'core.today',
                     'redirect_to': '',
                     'a': 'login',
                     'rememberme': 'forever',
                     'Submit': '로그인'}

        self.corp = 'IT NEWS'
        self.url = 'http://www.itnews.or.kr/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=8.0'
        td_block_id = ['td_uid_2_5fbeeb6592823', 'td_uid_1_5f6d6002399b8']
        self.params = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'action': 'td_ajax_block',
            'td_atts': {"limit": "5", "category_id": "1162", "show_child_cat": 30,
                        "ajax_pagination": "next_prev", "td_column_number": 3,
                        "td_ajax_filter_type": "td_category_ids_filter",
                        "td_filter_default_txt": "All",
                        "class": "td_uid_1_5f6d6002399b8_rand",
                        "tdc_css_class": "td_uid_1_5f6d6002399b8_rand"
                        },
            'td_block_id': td_block_id[0],
            'td_column_number': 3,
            'td_current_page': 2,
            'block_type': 'td_block_mega_menu'
        }
        self.page_key = 'td_current_page'

    def get_url_list(self, page_num):
        self.params[self.page_key] = page_num
        soup = post_soup(self.url, self.params)
        url_list = []
        divisnone = False
        while not divisnone:
            if soup.div is None:
                divisnone = True
            else:
                divclass = soup.attrs.setdefault('class', None)
                if divclass is not None:
                    if 'td-module-thumb' in divclass[0]:
                        url = soup.a.attrs['href'].replace('\\"', '').replace('\\', '')
                        url_list.append(url)
                    else:
                        pass
                soup = soup.div

        return url_list

    def get_data(self, url, soup):
        title = soup.title.text
        try:
            thumb = soup.find('img', {'class': 'aligncenter'}).attrs['src']
        except:
            thumb = ''
        datetime = soup.find('time', {'class': 'entry-date'}).attrs['datetime'].split('T')
        day = datetime[0]
        time = datetime[1][:5]
        try:
            cat = soup.find('li', {'class': 'entry-category'}).text
        except:
            cat = ''
        return [self.corp, url, title, thumb, day, time, cat]

    def crawler(self):
        page_num = 1
        metadata_list = []
        while True:
            urls = self.get_url_list(page_num)
            meta_data = self.__crawler(urls)
            metadata_list.extend(meta_data)
            stop_sign = time_check(meta_data, self.input_date)
            if stop_sign:
                return metadata_list
            page_num += 1

    def __crawler(self, urls: list):
        metadata = []
        for page in urls:
            bin = {}
            soup = post_soup(page, self.ID_PARAMS)
            data = self.get_data(page, soup)
            bin['corp'], bin['url'], bin['title'], bin['thumb'], bin['day'], bin['time'], bin['category'] = data
            metadata.append(bin)
            return metadata

        return metadata


# Need to test!! (Post)
class Mobiinside(Website):

    def __init__(self, input_date):
        self.input_date = input_date
        self.BASE_PAGE = 'https://www.mobiinside.co.kr/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=9.7.4'
        self.HOME_PAGE = 'https://www.mobiinside.co.kr'
        self.CORP = '모바일 인사이드'

        self.page_key = 'td_current_page'

        self.obj = {'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'action': 'td_ajax_block',
               'td_atts': {"category_id": "52",
                           "limit": "100",
                           "image_height": "65",
                           "modules_on_row": "eyJhbGwiOiI1MCUiLCJwaG9uZSI6IjEwMCUifQ==",
                           "modules_gap": "eyJhbGwiOiIxLjYlIiwicG9ydHJhaXQiOiIyJSJ9",
                           "modules_category": "image",
                           "show_btn": "none",
                           "ajax_pagination": "next_prev",
                           "show_cat": "none",
                           "td_filter_default_txt": "All",
                           "all_modules_space": "36",
                           "modules_border_color": "#eaeaea",
                           "modules_divider_color": "#eaeaea",
                           "image_alignment": "50",
                           "excerpt_col": "1",
                           "art_audio_size": "1.5",
                           "meta_info_border_color": "#eaeaea",
                           "modules_category_radius": "0",
                           "show_author": "inline-block",
                           "show_date": "inline-block",
                           "show_review": "inline-block",
                           "show_com": "block",
                           "show_excerpt": "block",
                           "show_audio": "block",
                           "f_header_font_title": "Block header",
                           "f_ajax_font_title": "Ajax categories",
                           "f_more_font_title": "Load more button",
                           "f_title_font_title": "Article title",
                           "f_cat_font_title": "Article category tag",
                           "f_meta_font_title": "Article meta info",
                           "f_ex_font_title": "Article excerpt",
                           "f_btn_font_title": "Article read more button",
                           "shadow_shadow_title": "Module Shadow",
                           "shadow_m_shadow_title": "Meta info shadow",
                           "td_column_number": 2,
                           "class": "td_uid_8_5f6bf4f0786c6_rand",
                           "tdc_css_class": "td_uid_8_5f6bf4f0786c6_rand",
                           "tdc_css_class_style": "td_uid_8_5f6bf4f0786c6_rand_style"},

               "td_block_id": '',
               "td_column_number": 2,
               "td_current_page": 1,
               "block_type": "td_flex_block_1",
               "td_magic_token": ''

               }

    def id_pw(self):
        response = requests.get(self.HOME_PAGE)
        soup = bs(response.content, 'html.parser')
        td_block_id = soup.find('div', {'class': 'td_block_inner td-mc1-wrap'}).attrs['id']
        td_magic_token = ''
        for i in soup.find_all('script'):
            if 'tdBlockNonce' in str(i):
                for e in str(i).split(';'):
                    if 'tdBlockNonce' in e:
                        td_magic_token = e.split('=')[-1].replace('\"', '')
                        break
        self.obj['td_block_id'] = td_block_id
        self.obj['td_magic_token'] = td_magic_token

    def parse_cat(self, _cat):
        cat = _cat.attrs['href']
        cat = re.sub('.*category|/|\\\\', '', cat)
        return cat

    def parse_thumb(self, _thumb):
        thumb = _thumb.attrs['style']
        thumb = re.sub('.*\(|\)', '', thumb)
        thumb = thumb.replace('\\', '')
        return thumb

    def parse_url(self, _url):
        url = _url.next.attrs['href']
        url = url.replace('\\', '')
        return url

    def parse_title(self, _title):
        title = _title.attrs['title']
        return title

    def parse_day_time(self, _datetime):
        datetime = _datetime.attrs['datetime']
        day = datetime.split('T')[0]
        time = datetime.split('T')[1][:5]
        return day, time

    def crawler(self):
        page_num = 1
        all_meta_data= []
        self.id_pw()
        while True:
            meta_data = self.__crawler(page_num)
            all_meta_data.extend(meta_data)
            stop_sign = time_check(meta_data, self.input_date)
            if stop_sign:
                break
            page_num += 1

        return all_meta_data

    def __crawler(self, page_num):
        self.obj[self.page_key] = page_num
        my_obj = self.obj
        headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'
        }
        response = requests.post(self.BASE_PAGE, data=my_obj, headers=headers)
        if response.status_code != 200:
            print(f'Error<{self.__name__}> : {response.status_code}')
            raise ConnectionError

        page = response.text.encode('utf-8')
        page = page.decode('unicode_escape')
        soup = bs(page, 'html.parser')

        urls = soup.find_all('h3', {'class': 'entry-title'})
        titles = soup.find_all('a', {'class': 'td-image-wrap'})
        datetimes = soup.find_all('time', {'class': 'entry-date'})
        thumbs = soup.find_all('span', {'class': 'entry-thumb'})
        cats = soup.find_all('a', {'class': 'td-post-category'})

        meta_data = []

        for _title, _url, _thumb, _cat, _datetime in zip(titles, urls, thumbs, cats, datetimes):
            thumb = self.parse_thumb(_thumb)
            title = self.parse_title(_title)
            url = self.parse_url(_url)
            cat = self.parse_cat(_cat)
            day, time = self.parse_day_time(_datetime)

            data = {
                'corp': self.CORP,
                'thumb': thumb,
                'title': title,
                'day': day,
                'time': time,
                'url': url,
                'category': cat}

            meta_data.append(data)

        return meta_data


class All:
    class_list = [Ainews, Besuccess, Bikorea, Bizwatch, Clo, Hellodd, Itchosun, Itdonga, Itnews, Klnews, Mobiinside, Platum, Sciencetimes, Venturesquare, Vrn]
