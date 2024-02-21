from dateutil.parser import parse
from bs4 import BeautifulSoup
import requests
import re
import lxml


def pars_software():
    try:
        json_file = []
        url = 'http://feeds.feedburner.com/RussianTestingBlogs50'
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ("
                                                     "KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
                                       })
        bs = BeautifulSoup(r.content, features="lxml-xml")
        article = bs.find_all('item')
        for name in article:
            json_file.append({
                'Источник': 'Software-testing',
                'Дата публикации': parse(name.find('pubDate').text).strftime('%Y-%m-%d %H:%M:%S'),
                'Статья': name.find('title').text,
                'Ссылка': name.find('link').text,
                'Картинка': name.find('img').get('src') if name.find('img') is not None
                else None
            })
        return json_file
    except Exception as E:
        return 'Хабр ---', E


def pars_habr():
    try:
        json_file = []
        url = 'https://habr.com/ru/hub/it_testing/'
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ("
                                                     "KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
                                       })
        bs = BeautifulSoup(r.text, "lxml")
        article = bs.find_all('article', class_='tm-articles-list__item')
        for name in article:
            json_file.append({
                'Источник': 'Хабр',
                'Дата публикации': parse(name.span.time['datetime']).strftime('%Y-%m-%d %H:%M:%S'),
                'Статья': name.h2.a.span.text,
                'Ссылка': 'https://habr.com' + name.h2.a['href'],
                'Картинка': name.find_next('img', class_='tm-article-snippet__lead-image').get('src') if name.find('img', class_='tm-article-snippet__lead-image') is not None
                else None
            })
        return json_file
    except Exception as E:
        return 'Хабр ---', E


def pars_test_engineer():
    try:
        json_file = []
        url = 'https://testengineer.ru/'
        r = requests.get(url)
        bs = BeautifulSoup(r.text, "lxml")
        article = bs.find_all('div',
                              class_='td_module_flex td_module_flex_5 td_module_wrap td-animation-stack td-cpt-post')
        for name in article:
            json_file.append({
                'Источник': 'Testengineer',
                'Дата публикации': parse(name.span.time['datetime']).strftime('%Y-%m-%d %H:%M:%S'),
                'Статья': name.h3.a.text,
                'Ссылка': name.h3.a['href'],
                'Картинка': re.findall(r'http(?:s)?://\S+', name.find_next('span', class_='entry-thumb').get('style'))[
                    0]
            })
        return json_file
    except Exception as E:
        return 'Testengineer ---', E


def pars_tproger():
    try:
        json_file = []
        url = 'https://tproger.ru/tag/testing/'
        r = requests.get(url)
        bs = BeautifulSoup(r.text, "lxml")
        article = bs.find_all('div', attrs={"type": "card"})
        for name in article:
            json_file.append({
                'Источник': 'Tproger',
                'Дата публикации': parse(name.time['datetime']).strftime('%Y-%m-%d %H:%M:%S'),
                'Статья': name.h2.a.text,
                'Ссылка': 'https://tproger.ru' + name.h2.a['href'],
                'Картинка': name.find_next('img', class_='tp-image__image').get('src') if name.find_next('img',
                                                                                                         class_='tp-image__image') is not None
                else None
            })
        return json_file
    except Exception as E:
        return 'Tproger ---', E


def pars_otus():
    try:
        json_file = []
        url = 'https://otus.ru/journal/tag/testirovanie/'
        r = requests.get(url)
        bs = BeautifulSoup(r.text, "lxml")
        article = bs.find_all('article', class_='post')
        for name in article:
            json_file.append({
                'Источник': 'Otus',
                'Дата публикации': parse(name.find_next('time').get('datetime')).strftime('%Y-%m-%d %H:%M:%S'),
                'Статья': name.h2.text,
                'Ссылка': name.h2.a['href'],
                'Картинка': name.find('img', class_='wp-post-image').get('src')
            })
        return json_file
    except Exception as E:
        return 'Otus ---', E


def all_pars_site():
    all_site = pars_habr() + pars_tproger() + pars_test_engineer() + pars_otus() + pars_software()
    return all_site
