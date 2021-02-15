# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from dateutil.parser import parse
import re
import unicodedata


class Aving:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '에이빙'
        self.cate_dic = {'모바일/컴퓨팅': '01', '전자/가전': '02', '라이프': '03', '자동차': '04', '산업': '05',
            '헬스케어': '08', '리뷰': '06', '포커스': '07'}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'http://kr.aving.net/news/?mn_name=news&cateId={val}&page={num}')
                soup = bs(res.content, 'lxml')

                article_list = soup.select('div.news_sub_list > table > tr')[0:30]

                for article in article_list:
                    title = article.find('div', class_='title').find('a').text
                    url = 'http://kr.aving.net' + article.find('div', class_='title').find('a')['href']
                    thumb = article.find('img')['src']
                    day = article.find('span', class_='f_9_gray6').text

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": None,
                                  "category": key}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Betanews:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '베타뉴스'
        self.cate_dict = {"하드웨어": "1", "소프트웨어": "3", "엔터프라이즈": "4", "윈도우": "5", "모바일": "6", "소셜/인터넷": "7", "모빌리티": "8",
           "과학": "9", "가전": "10", "종합": "12"}

    def crawler(self):

        meta_data = []
        for key, val in self.cate_dict.items():
            num = 1
            while True:
                res = requests.get(f'http://www.betanews.net/bbs/list.html?page={num}&tkind=1&lkind={val}')
                soup = bs(res.content, 'lxml')

                article_section = soup.find('div', class_='list_vt').find('ul')
                article_list = article_section.find_all('li', class_='vtl')

                for article in article_list:

                    try:
                        thumb = 'http://www.betanews.net' + article.find('img')['src']
                    except:
                        thumb = None

                    title = article.find('dl').find('dt').find('a').text
                    url = "http://www.betanews.net" + article.find('dl').find('dt').find('a')['href']
                    day_time = parse(article.find('dl').find('dt').find('span', class_="date").text)
                    day = datetime.strftime(day_time, "%Y-%m-%d")
                    time = datetime.strftime(day_time, "%H:%M")

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day, "url": url,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Bloter:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '블로터'
        self.cate_dic = {"비즈니스": "business", "콘텐츠": "contents", "플랫폼": "platform", "소사이어티": "society",
                         "엔터테인먼트": "entertainment", "퓨처": "future", "스타트업": "start-up", "블록체인": "blockchain"}

    def crawler(self):

        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'http://www.bloter.net/archives/category/{val}/page/{num}')
                soup = bs(res.content, 'lxml')

                article_section = soup.find('div', class_='category--body--main')
                article_list = article_section.find_all('article', class_='general-article')

                for article in article_list:

                    try:
                        thumb = article.find('img')['src']
                    except:
                        thumb = None

                    title = article.find('h1').find('a').text
                    url = article.find('h1').find('a')['href']
                    day = datetime.strptime(article.find('span', class_='publish').text, "%Y년 %m월 %d일")
                    day = datetime.strftime(day, "%Y-%m-%d")

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "time": None, "title": title, "day": day, "url": url,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Boannews:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '보안뉴스'
        self.cate_dic = {"SECURITY": "1", "IT": '2', "SATETY": "4"}

    def crawler(self):

        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                #res = requests.get(f'https://www.boannews.com/media/list.asp?Page={num}&mkind={val}', verify=False)
                res = requests.get(f'https://www.boannews.com/media/list.asp?Page={num}&mkind={val}')
                soup = bs(res.content, 'lxml')

                article_section = soup.find('div', id='news_area')
                article_list = article_section.find_all('div', class_='news_main') + soup.find_all('div', class_='news_list')


                for article in article_list:

                    try:
                        thumb = "https://www.boannews.com/" + article.find('div', class_='news_main_txt').find('img')['src']
                    except:
                        thumb = None

                    try:
                        title = article.find('div', class_='news_main_title').text
                    except:
                        title = article.find('span', class_="news_txt").text

                    try:
                        url = "https://www.boannews.com/" + article.find('div', class_='news_main_title').find('a')['href']
                    except:
                        url = "https://www.boannews.com/" + article.find('a')['href']

                    try:
                        day_time = datetime.strptime(article_list[3].find('span', class_="news_writer").text.split('| ')[1],
                                                     '%Y년 %m월 %d일 %H:%M')
                        day = datetime.strftime(day_time, "%Y-%m-%d")
                        time = datetime.strftime(day_time, "%H:%M")
                    except:
                        #res = requests.get(url, verify=False)
                        res = requests.get(url)
                        soup = bs(res.content, 'lxml')

                        day_time = parse(soup.find('div', id="news_util01").text.strip().split(': ')[1])
                        day = datetime.strftime(day_time, "%Y%m%d")
                        time = datetime.strftime(day_time, "%H:%M")

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": time,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class BylineNetwork:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '바이라인네트워크'

    def crawler(self):

        # 이 사이트는 작가별로 구분되어 있음.
        authors = {}
        res = requests.get('https://byline.network/')
        soup = bs(res.content, 'lxml')

        temp = soup.find('ul', id='et-menu').find_all('li')
        for i in temp:
            authors[i.a.text.strip()] = i.a['href']
        del authors['Contributor']

        meta_date = []
        for key, val in authors.items():
            num = 1
            while True:
                res = requests.get(val + f'page/{num}')
                soup = bs(res.content, 'lxml')

                article_section = soup.find('div', class_='paginated_content')
                article_list = article_section.find_all('article')

                for article in article_list:

                    try:
                        thumb = article.find('img')['src']
                    except:
                        thumb = None

                    title = article.find('h2').text
                    url = article.find('h2').find('a')['href']

                    categorys = article.find_all('a', rel='tag')
                    category = []
                    for i in categorys:
                        category.append(i.text)

                    day = parse(article.find('span', class_='updated').text.replace('년', '-').replace('월', '-').replace('일', ''))
                    day = datetime.strftime(day, '%Y-%m-%d')
                    time = None

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day, "url": url,
                                  "category": category}
                        meta_date.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_date


class Cionet:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '씨아이오넷'
        self.cate_dic =  {"리더십|조직관리": "27", "빅데이터": "2996", "신기술|미래": "557", "클라우드": "32", "IoT": "13931", "AI": "22000",
            "디지털 트랜스포메이션": "21996", "개발자": "21999", "마케팅": "13932"}

    def get_date(self, str):
        now_date = datetime.now()
        if '일' in str:
            date = now_date - timedelta(days=int(re.search('\d+', str).group()))
            date = datetime.strftime(date, '%Y-%m-%d')
        elif '시간' in str:
            date = now_date - timedelta(hours=int(re.search('\d+', str).group()))
            date = datetime.strftime(date, '%Y-%m-%d')
        elif '분' in str:
            date = now_date - timedelta(minutes=int(re.search('\d+', str).group()))
            date = datetime.strftime(date, '%Y-%m-%d')
        else:
            date = str
        return date

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'https://www.ciokorea.com/t/{val}/{key}?page={num}')
                soup = bs(res.content, 'lxml')

                article_sec = soup.find('div', class_='contents-body').find('div')
                article_list = article_sec.find_all('div', class_='list_')

                for article in article_list:
                    try:
                        thumb = 'https://www.ciokorea.com' + article.find('div', class_='list_image').find('img')['src']
                    except:
                        thumb = None
                    title = article.find('div').find('h4').find('a').text
                    url = 'https://www.ciokorea.com' + article.find('div').find('h4').find('a')['href']
                    day = article.find('div', class_='list_time').text.strip().replace('.', '-')
                    day = self.get_date(day)

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": None,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Cnet:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '씨넷코리아'
        self.header = {'User-Agent':'Mozilla/5.0', 'Referer': 'https://www.cnet.co.kr/news/'}

    def crawler(self):
        meta_data = []
        num = 0
        while True:
            data = {'pagenum': num, 'listcode': 'newsall'}
            res = requests.post('https://www.cnet.co.kr/news/ajax_list.php', headers = self.header, data = data)

            datas = res.json()

            for data in datas['lists']:
                title = unicodedata.normalize("NFKD", data['title'])
                thumb = data['frImage']
                url = 'https://www.cnet.co.kr/view/?no=' + data['publish_key']
                day = data['publish_key'][0:8]
                day = datetime.strptime(day, "%Y%m%d")
                day = datetime.strftime(day, "%Y-%m-%d")
                category = data['codeName']

                if day >= self.time_standard:
                    result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": None,
                              "category": [category]}
                    meta_data.append(result)

            if day < self.time_standard:
                break

            num += 1

        return meta_data


class Datanet:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '데이터넷'

    def crawler(self):
        num = 1
        meta_data = []
        while True:
            res = requests.get(f'http://www.datanet.co.kr/news/articleList.html?page={num}&sc_section_code=S1N1&view_type=sm')
            soup = bs(res.content, 'html.parser')

            article_section = soup.find('section', class_='article-list-content type-sm text-left')
            article_list = article_section.find_all('div', class_='list-block')

            for article in article_list:
                title = article.find('div', 'list-titles').text
                url = "http://www.datanet.co.kr/" + article.find('div', 'list-titles').find('a')['href']

                try:
                    thumb = "http://www.datanet.co.kr/news/" + article.find('div', 'list-image')['style'].split('./')[1].replace(')', '')
                except:
                    thumb = None

                category = article.find('div', "list-dated").text.split('|')[0].strip()

                day_time = parse(article.find('div', "list-dated").text.split('|')[2].strip())
                day = datetime.strftime(day_time, "%Y-%m-%d")
                time = datetime.strftime(day_time, "%H:%M")

                if day >= self.time_standard:
                    result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day, "url": url,
                              "category": [category]}
                    meta_data.append(result)

            if day < self.time_standard:
                break

            num += 1

        return meta_data


class Datanews:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '데이터뉴스'
        self.cate_dic = {"종합": "all", "정치/사회": "112", "경제/금융": "59", "산업": "118", "IT": "116", "라이프": "117"}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                if key == '종합':
                    res = requests.get(f'http://www.datanews.co.kr/news/article_list_all.html?page={num}')
                else:
                    res = requests.get(f'http://www.datanews.co.kr/news/section.html?sec_no={val}&page={num}')

                soup = bs(res.text, 'html.parser')

                article_section = soup.find('div', class_='c011_ara')
                article_list = article_section.find_all('table', style='padding:10px 0;')

                for article in article_list:
                    try:
                        thumb = 'http://www.datanews.co.kr' + article.find('img')['src']
                    except:
                        thumb = None

                    title = article.find('td', class_="news1").find('a').text.strip()
                    url = 'http://www.datanews.co.kr/news/' + article.find('a')['href']
                    day_time = parse(article.find('span').text.strip())
                    day = datetime.strftime(day_time, "%Y-%m-%d")
                    time = datetime.strftime(day_time, "%H:%M")

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "title": title, "day": day, "time": time, "url": url,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Ddaily:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '디지털데일리'
        self.cate_dic = {"IT정책": "60", "통신/방송": "61", "e비즈/솔루션": "62", "보안": "127", "금융IT": "94", "콘텐츠": "63",
                         "기업문화": "65", "산업": "64", "국제": "126", "피플": "145","칼럼": "153"}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'http://www.ddaily.co.kr/news/section_list_all/?sec_no={val}&page={num}')
                soup = bs(res.content, 'lxml')

                article_section = soup.find('div', class_="m01_ara")
                article_list = article_section.find_all('dl')

                for article in article_list:

                    title = article.find('dt').text
                    url = "http://www.ddaily.co.kr/" + article.find('dt').find('a')['href']

                    try:
                        thumb = article.find('dd').find('img')['src']
                    except:
                        thumb = None

                    day_time = article.find('dd').find('span').text.split(' ')[-2:]
                    day_time = parse(day_time[0] + ' ' + day_time[1])
                    day = datetime.strftime(day_time, '%Y-%m-%d')
                    time = datetime.strftime(day_time, '%H:%M')

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day, "url": url,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Dailysecu:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '데일리시큐'

    def crawler(self):
        meta_data = []
        num = 1
        while True:
            res = requests.get(f'https://www.dailysecu.com/news/articleList.html?page={num}&total=90311&box_idxno=&view_type=sm')
            soup = bs(res.content, 'html.parser')

            article_section = soup.find('section', class_='article-list-content type-sm text-left')
            article_list = article_section.find_all('div', class_='list-block')

            for article in article_list:
                try:
                    thumb = 'https://www.dailysecu.com/news/' + article.find('div', 'list-image')['style'].split('./')[1].replace(')', '')
                except:
                    thumb = None

                title = article.find('div', class_='list-titles').find('a').text
                url = 'https://www.dailysecu.com' + article.find('div', class_='list-titles').find('a')['href']
                category = article.find('div', 'list-dated').text.split(' |')[0]

                day_time = parse(article.find('div', 'list-dated').text.split(' |')[2].strip())
                day = datetime.strftime(day_time, "%Y-%m-%d")
                time = datetime.strftime(day_time, "%H:%M")

                if day >= self.time_standard:
                    result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day, "url": url,
                              "category": [category]}
                    meta_data.append(result)

            if day < self.time_standard:
                break

            num += 1

        return meta_data


class Kbench:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '케이벤치'
        self.cate_dic = {'컴퓨팅': '92', '스마트폰/모바일': '94', '라이프': '93'}
        self.header = {'User-Agent': 'Mozilla/5.0'}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'https://kbench.com/?q=taxonomy/term/{val}&page={num}', headers = self.header)
                soup = bs(res.content, 'lxml')

                article_list = soup.find('div', class_='view-content').find_all('div', class_='views-row')
                for article in article_list:
                    title = article.find('div', class_='text_tit').find('a').text
                    url = 'https://kbench.com' + article.find('div', class_='text_tit').find('a')['href']
                    thumb = article.find('img')['src']
                    day = article.find_all('div', class_='text_news')[1].text.split(' ')[0].replace('/', '-')
                    time = article.find_all('div', class_='text_news')[1].text.split(' ')[1][0:5]
                    sub_cate = article.find_all('div', class_='text_news')[1].text.split(' ')[3]

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": time,
                                  "category": [key, sub_cate]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Kinews:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '키뉴스'
        self.cate_dic = {"종합": "S1N1", "소재": "S1N2", "5G": "S1N3", "반도체": "S1N4", "디스플레이": "S1N5", "자동차": "S1N6",
            "모바일": "S1N7", "이머징": "S1N8", "데이터서비스": "S1N10", "인사이트": "S1N11"}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'https://www.kinews.net/news/articleList.html?sc_section_code={val}&view_type=sm&page={num}')
                soup = bs(res.content, 'lxml')

                article_sec = soup.find('section', class_='article-list-content')
                article_list = article_sec.find_all('div', class_='list-block')

                for article in article_list:
                    try:
                        thumb = 'https://www.kinews.net' + article.find('div', class_='list-image').find('a')['href']
                    except:
                        thumb = None
                    title = article.find('div', class_='list-titles').text
                    url = 'https://www.kinews.net' + article.find('div', class_='list-titles').find('a')['href']
                    date = article.find('div', class_='list-dated').text.split(' | ')[2]
                    day = date.split(' ')[0]
                    time = date.split(' ')[1]

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": time,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Koit:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '정보통신신문'

    def crawler(self):
        meta_data = []
        num = 1
        while True:
            res = requests.get(f'http://www.koit.co.kr/news/articleList.html?sc_section_code=S1N25&view_type=sm&page={num}')
            soup = bs(res.content, 'lxml')

            article_sec = soup.find('section', class_='article-list-content')
            article_list = article_sec.find_all('div', class_='list-block')

            for article in article_list:
                try:
                    thumb = 'http://www.koit.co.kr' + article.find('div', class_='list-image').find('a')['href']
                except:
                    thumb = None
                title = article.find('div', class_='list-titles').text
                url = 'http://www.koit.co.kr/' + article.find('div', class_='list-titles').find('a')['href']
                date = article.find('div', class_='list-dated').text.split(' | ')[2]
                day = date.split(' ')[0]
                time = date.split(' ')[1]
                category = article.find('div', class_='list-dated').text.split(' | ')[0]

                if day >= self.time_standard:
                    result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": time,
                              "category": [category]}
                    meta_data.append(result)

            if day < self.time_standard:
                break

            num += 1

        return meta_data


class Nextdaily:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '넥스트데일리'
        self.cate_dic = {"IT전자": '01', "경제금융": '14', "산업": '21', "유통": '04', "헬스뷰티": '11', "시사정치": '08',
             "레저": '12', "게임": '10', "라이프": '15', '사회공헌': '40'}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(f'http://www.nextdaily.co.kr/news/section.html?id1={val}&page={num}')
                soup = bs(res.text, 'html.parser')

                article_section = soup.find('ul', class_='section_list bdt2')
                article_list = article_section.find_all('li')

                for article in article_list:
                    title = article.find('strong').text
                    url = 'http://www.nextdaily.co.kr/' + article.find('a')['href']

                    try:
                        thumb = article.find('img')['src']
                    except:
                        thumb = None

                    res_time = requests.get(url)
                    soup_time = bs(res_time.text, 'html.parser')

                    day_time = parse(soup_time.find('div', class_='v_data fr').find('span').text.replace('발행일시 : ', ''))
                    day = datetime.strftime(day_time, "%Y-%m-%d")
                    time = datetime.strftime(day_time, "%H:%M")

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "thumb": thumb, "title": title, "day": day, "time": time, "url": url,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Techholic:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '테크홀릭'

    def get_cate_dic(self):
        res = requests.get('http://www.techholic.co.kr/')
        soup = bs(res.content, 'lxml')
        category_list = soup.find('ul', class_='mega-menu').find_all('li', 'megaline nobr') + soup.find('ul', class_='mega-menu').find_all('li', class_='megaline')
        category_list = list(set(category_list))

        cate_dic = {}
        for category in category_list:
            bot_cat = category.find_all('li')
            if category.find('a', class_='first').text != 'HOME':
                cate_dic[category.find('a', class_='first').text] = {x.text: x.find('a')['href'] for x in bot_cat}

        return cate_dic

    def crawler(self):
        cate_dic = self.get_cate_dic()
        meta_data = []
        for top_key, top_val in cate_dic.items():
            cate_url_list = top_val
            for key, val in cate_url_list.items():
                num = 1
                url_list = []
                while True:
                    res = requests.get(f'{val}&page={num}')
                    soup = bs(res.content, 'lxml')

                    article_list = soup.find('table', style='margin-top:10px;').find_all('td', class_='list-titles')

                    for article in article_list:
                        url = 'http://www.techholic.co.kr/news/' + article.find('a')['href']
                        url_list.append(url)

                    for url in url_list:
                        res = requests.get(url)
                        soup = bs(res.content, 'lxml')

                        try:
                            title = soup.find('font', class_='headline-title').text
                        except:
                            continue

                        try:
                            thumb = 'http://www.techholic.co.kr' + soup.find('img')['src']
                        except:
                            thumb = None

                        day_time = parse(soup.find('li', class_='date').text.replace('승인 ', ''))
                        day = datetime.strftime(day_time, '%Y-%m-%d')
                        time = datetime.strftime(day_time, '%H:%M')

                        if day >= self.time_standard:
                            result = {"corp": self.corp, "title": title, "thumb": thumb, "day": day, "time": time,
                                      "url": url, "category": [[top_key, key]]}
                            meta_data.append(result)

                    if day < self.time_standard:
                        break

                    num += 1

        return meta_data


class Techsuda:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '테크수다'
        self.cate_dic = {"테크수다": "http://www.techsuda.com/archives/category/tech",
           "컬쳐수다": "http://www.techsuda.com/archives/category/culture", "북수다": "http://www.techsuda.com/archives/category/culture/book"}

    def crawler(self):
        meta_data = []
        for key, val in self.cate_dic.items():
            num = 1
            while True:
                res = requests.get(val + f'/page/{num}')
                soup = bs(res.content, 'lxml')

                article_sec = soup.find('div', class_='content').find('div', class_='post-listing')
                article_list = article_sec.find_all('article', class_='item-list')

                for article in article_list:
                    title = unicodedata.normalize("NFKD", article.find('h2', class_='post-box-title').text.strip())
                    try:
                        thumb = article.find('div', class_='post-thumbnail').find('a').find('img')['src']
                    except:
                        thumb = None
                    url = article.find('h2', class_='post-box-title').find('a')['href']
                    day = article.find('p', class_='post-meta').text.strip()
                    day = datetime.strftime(datetime.strptime(day, '%Y년 %m월 %d일'), '%Y-%m-%d')

                    if day >= self.time_standard:
                        result = {"corp": self.corp, "title": title, "thumb": thumb, "url": url, "day": day, "time": None,
                                  "category": [key]}
                        meta_data.append(result)

                if day < self.time_standard:
                    break

                num += 1

        return meta_data


class Brainbox:

    def __init__(self, input_date):
        self.time_standard = input_date
        self.corp = '브레인박스'

    def get_cate_top(self):
        res = requests.get(f'https://www.brainbox.co.kr/bbs/board.php?bo_table=news')
        soup = bs(res.content, 'lxml')

        category_top = soup.find('ul', 'menu').find('ul').find_all('li')
        category_top = {x.find('a').text: x.find('a')['href'] for x in category_top}

        return category_top

    def get_cate_dic(self, category_top):
        cate_dic = {}
        for key, val in category_top.items():
            res = requests.get(f'{val}')
            soup = bs(res.content, 'lxml')

            category_bot = soup.find('div', 'snb').find('ul').find_all('li')
            cate_dic[key] = {x.find('a').text: x.find('a')['href'] for x in category_bot}

        return cate_dic

    def crawler(self):
        category_top = self.get_cate_top()
        cate_dic = self.get_cate_dic(category_top)

        meta_data = []
        for top_key, top_val in category_top.items():
            url_list = cate_dic[top_key]
            for key, val in url_list.items():
                num = 1
                while True:
                    res = requests.get(f'{val}&page={num}')
                    soup = bs(res.content, 'lxml')

                    article_section = soup.find('ul', class_="newslist")
                    article_list = article_section.find_all('li')

                    for article in article_list:
                        try:
                            thumb = article.find('a', class_='cover').find('img')['src']
                        except:
                            thumb = None

                        try:
                            title = article.find('p', class_='title').find('a').text
                        except:
                            continue

                        url = article.find('p', class_='title').find('a')['href']

                        res = requests.get(url)
                        soup = bs(res.content, 'lxml')

                        day_time = datetime.strptime(soup.find('div', class_='writer').find('strong').text, '%y-%m-%d %H:%M')
                        day = datetime.strftime(day_time, '%Y-%m-%d')
                        time = datetime.strftime(day_time, '%H:%M')

                        if day >= self.time_standard:
                            result = {"corp": self.corp, "thumb": thumb, "time": time, "title": title, "day": day,
                                      "url": url, "category": [top_key, key]}
                            meta_data.append(result)

                    if day < self.time_standard:
                        break

                    num += 1

        return meta_data


class All:
    class_list = [
        Aving, Betanews, Bloter, Boannews, BylineNetwork, Cionet, Cnet,
        Datanet, Datanews, Ddaily, Dailysecu, Kbench, Kinews,
        Koit, Nextdaily, Techholic, Techsuda, Brainbox
    ]
