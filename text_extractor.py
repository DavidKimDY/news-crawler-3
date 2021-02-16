def digital_daily(soup):
    text = soup.find('div', {'class': "cnt_view news_body_area"}).text
    return text


def data_news(soup):
    return soup.find('div', {'id': 'news_body_area'}).text


def kbench(soup):
    return soup.find('table', {'class': "nodeContentTitle"}).text


def koit(soup):
    return soup.find('article', {"class": "article-veiw-body view-page"}).text


def tech_holic(soup):
    return soup.find('div', {"id": "articleBody"}).text


def tech_talk(soup):
    return soup.find('div', {'class': "entry"}).text


def beta_news(soup):
    return soup.find('div', {'id': "articleBody"}).text


def bi_line(soup):
    return soup.find('div', {"class": "post-wrap"}).text


def brain_box(soup):
    return soup.find("section", {'class': "left"}).text


def daily_cq(soup):
    return soup.find('div', {'itemprop': "articleBody"}).text


def next_daily(soup):
    return soup.find('div', {'itemprop': "articleBody"}).text


def bo_an_news(soup):
    text_soup = soup.find('div', {'itemprop': "articleBody"})
    if text_soup is None:
        return None
    else:
        return text_soup.text


def aving(soup):
    return soup.find('div', {'class': "content"}).text


def data_net(soup):
    return soup.find('div', {'itemprop': "articleBody"}).text


def key_news(soup):
    return soup.find('div', {'itemprop': "articleBody"}).text


def cio_net(soup):
    return soup.find('div', {'class': 'node_body cb'}).text


def cnet(soup):
    t = ''
    for a in soup.find('div', {'class': "col-7 article-main-body row"}).find_all('p'):
        t += a.text
    return t


def bloter(soup):
    t = ''
    for a in soup.find('div', {'itemprop': "articleBody"}).find_all('p'):
        t += a.text
    return t


def itchosun(soup):
    t = ''
    for a in soup.find_all('div', {'class': 'par'}):
        t += a.text
    return t


def venture_sqr(soup):
    return soup.find('div', {'class': 'post-content description'}).text


def clo(soup):
    t = ''
    for a in soup.find('div', {'class': 'content'}).find_all('p'):
        t += a.text
    return t


def ai_times(soup):
    t = ''
    for i in soup.find('div', {'class': "article-body"}).find_all('p'):
        t += i.text + ' '
    return t


def hellodd(soup):
    parsed = soup.find('div', {'class': "article-body"})
    return parsed.article.text


def besuccess(soup):
    return soup.find('div', {'itemprop': "articleBody"}).text


def sciencetimes(soup):
    t = ''
    for a in soup.find('div', {'class': "view_content"}).find_all('p'):
        t += a.text
    return t


def klnews(soup):
    return soup.find('article', {'itemprop': "articleBody"}).text


def itnews(soup):
    return soup.find('div', {'class': "td-post-content"}).text


def bizwatch(soup):
    return soup.find('div', {"itemprop": "articleBody"}).text


def itdonga(soup):
    t = ''
    for i in soup.find('div', {'class': "article"}).find_all('p'):
        t += i.text
    return t


def vrn(soup):
    return soup.find('div', {"itemprop": "articleBody"}).text


def bikorea(soup):
    return soup.find('td',{'id' : "articleBody"}).text


def platum(soup):
    t = ''
    for i in soup.find('div', {'class': "post_wrapper"}).find_all('p'):
        t += i.text
    return t


def mobiinside(soup):
    t = ''
    for i in soup.find_all('p'):
        t += i.text
    return t

def irobot(soup):
    t = ''
    for i in soup.find_all('p'):
        t += i.text
    return t

news_map = {
    # key value is corp value

    '디지털데일리': digital_daily,
    '데이터뉴스': data_news,
    '케이벤치': kbench,
    '정보통신신문': koit,
    '테크홀릭': tech_holic,
    '테크수다': tech_talk,
    '베타뉴스': beta_news,
    '바이라인네트워크': bi_line,
    '브레인박스': brain_box,
    '데일리시큐': daily_cq,
    '넥스트데일리': next_daily,
    '보안뉴스': bo_an_news,
    '에이빙': aving,
    '데이터넷': data_net,
    '키뉴스': key_news,
    '씨넷코리아': cnet,
    '씨아이오넷': cio_net,
    '블로터': bloter,
    'IT CHOSUN': itchosun,
    '벤처스퀘어': venture_sqr,
    '인공지능신문': ai_times,
    '헬로디디': hellodd,
    'CLO': clo,
    'besuccess': besuccess,
    'sciencetimes': sciencetimes,
    '물류신문': klnews,
    'IT NEWS': itnews,
    'bizwatch': bizwatch,
    'IT동아': itdonga,
    'VRN': vrn,
    'BI KOREA': bikorea,
    'platum': platum,
    '모바일 인사이드': mobiinside,
    '로봇신문사': irobot
}


def text_extractor(news, soup):
    function = news_map[news]
    text = function(soup)
    return text