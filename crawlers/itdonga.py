base_page='https://it.donga.com/news/?page={page_number}',
page_head='https://it.donga.com',
corp="IT동아"


def parse_title(_title):
    title = str(_title.text)
    title = title.split('\n')[1].strip()
    return title


def parse_thumb(_thumb):
    thumb = str(_thumb)
    thumb = thumb.split('\"')[5]
    thumb = PAGE_HEAD + thumb
    return thumb


def parse_day(_day):
    day = _day.text
    day = day.replace('.', '-').rstrip('-')
    return day


def parse_url(_url):
    url = _url.attrs['href']
    url = PAGE_HEAD + url
    return url


def datadict(soup):
    _datadict['title'] = {'data': soup.select('.mt-0'), 'function': parse_title}
    _datadict['thumb'] = {'data': soup.select('.media img'), 'function': parse_thumb}
    _datadict['day'] = {'data': soup.find_all('time'), 'function': parse_day}
    _datadict['url'] = {'data': soup.find_all('a', class_='media'), 'function': parse_url}

    return _datadict
