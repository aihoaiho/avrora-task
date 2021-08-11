import pandas as pd
from bs4 import BeautifulSoup
import requests
import os

URL = "https://zakup.kbtu.kz"
PAGE_URL = "/zakupki/sposobom-zaprosa-cenovyh-predlozheniy&page="


def find_ads_anchor_tag_url(soup):
    all_anchor_tags = soup.find_all('a', 'btn-outline-secondary')
    ads_url = [tag.get('href') for tag in all_anchor_tags]

    return ads_url


def change_page():
    for page_index in range(1, 43):
        page = requests.get(f"{URL}{PAGE_URL}{page_index}").text
        soup = BeautifulSoup(page, 'html.parser')
        get_ads_items(find_ads_anchor_tag_url(soup))


def get_ads_items(all_ads_url: list):
    attr = {
        'style': ['margin-left:5px;', 'color:#6c757d;margin-left:5px;font-weight: bold;'],
    }
    for url in all_ads_url:
        page = requests.get(f"{URL}{url}").text
        soup = BeautifulSoup(page, 'html.parser')

        ads_names = soup.find('h4').text.strip()
        ads_items = [s.getText().strip() for s in soup.find_all('span', attrs=attr)]

        ads_items.append(ads_names)

        check_csv(ads_items)


def check_csv(ads_items):
    df = pd.DataFrame([ads_items])
    if not os.path.isfile('All_ADS.csv'):
        df.to_csv('All_ADS.csv', index=False, encoding='utf-8-sig', header=['Организатор', 'Начало', 'Окончание', 'Статус', 'Название'])
    else:
        df.to_csv('All_ADS.csv', index=False, mode='a', encoding='utf-8-sig', header=False, index_label=False)


change_page()
