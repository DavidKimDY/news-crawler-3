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
    return soup.find('div', {'itemprop': "articleBody"}).text


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


news_map = {
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
    '벤처스퀘어': venture_sqr
}


def text_extractor(news, soup):
    function = news_map[news]
    text = function(soup)
    return text