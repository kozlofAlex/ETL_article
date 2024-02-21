from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
from dateutil.parser import parse


# Получение вакансий с HH
def pars_hh():
    spec = {
        # 'text': 'Тестировщик',  # Текст фильтра
        'professional_role': 124,  # 124 - Спецализация: Тестировщик
        'schedule': 'remote',  # Формат работы: Удаленный
        'order_by': 'publication_time',  # Сортировка по Дате публикации
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    url = 'https://api.hh.ru/vacancies'
    r = requests.get(url, params=spec)

    if r.status_code == 200:
        try:
            data = r.json()
            vacancies = data.get("items", [])
            json_file = []
            for v in vacancies:
                json_file.append({
                    'ИД': int(v.get("id")),
                    'Источник': 'Headhunter',
                    'Дата публикации': parse(v.get('published_at')).strftime('%Y-%m-%d %H:%M:%S'),
                    'Вакансия': v.get("name"),
                    'Ссылка': v.get("alternate_url"),
                    'ЗП мин': v.get("salary", {}).get("from") if v.get("salary") is not None else None,
                    'ЗП макс': v.get("salary", {}).get("to") if v.get("salary") is not None else None,
                    'Валюта': v.get("salary", {}).get("currency") if v.get("salary") is not None else None,
                    'Компания': v.get("employer", {}).get("name"),
                    'Компания_ссылка': v.get("employer", {}).get("alternate_url"),
                    'Картинка': v.get("employer", {}).get("logo_urls", {}).get('original') if v.get("employer", {}).get(
                        "logo_urls", {}) is not None else None,
                    'Описание': v.get("snippet", {}).get("requirement"),
                    'Требования': v.get("snippet", {}).get("responsibility"),
                    'Опыт': v.get("experience", {}).get("name")
                })
            return json_file
        except Exception as E:
            return 'HH ---', E
    else:
        return f"Request failed with status code: {r.status_code}"


def pars_habr_vacancies():
    try:
        json_file = []
        url = ('https://career.habr.com/vacancies/rss?currency=RUR&remote=1s[]=12&s[]=10&s[]=13&s[]=11&s[]=87&s['
               ']=14&s[]=15&s[]=16&s[]=107&sort=date&type=all')

        r = requests.get(url)
        bs = BeautifulSoup(r.content, features="lxml-xml")
        article = bs.find_all('item')
        for name in article:
            json_file.append({
                'ИД': name.find('guid').text,
                'Источник': 'Хабр карьера',
                'Дата публикации': parse(name.find('pubDate').text).strftime('%Y-%m-%d %H:%M:%S'),
                'Вакансия': name.find('title').text,
                'Ссылка': name.find('link').text,
                'ЗП мин': None,
                'ЗП макс': None,
                'Валюта': None,
                'Компания': name.find('author').text,
                'Компания_ссылка': None,
                'Картинка': name.find('image').text,
                'Описание': name.find('description').text,
                'Требования': None,
                'Опыт': None,
            })
        return json_file
    except Exception as E:
        return 'Хабр карьера ---', E


def all_pars_vac():
    all_vac = pars_hh() + pars_habr_vacancies()
    return all_vac
