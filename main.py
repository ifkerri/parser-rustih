from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests as r
import csv
import json

input_data = {
    'rus_poet_klassik': {
        'url': 'https://rustih.ru/stihi-russkih-poetov-klassikov/'
    }
}

user_agent = UserAgent()
headers = {
    'Accept': '*/*',
    'User-Agent': user_agent.random
}

for key, value in input_data.items():

    response = r.get(url=value.get('url'), headers=headers)
    src = response.text

    with open(f'data/{key}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    hrefs = {}
    soup = BeautifulSoup(src, 'lxml')
    all_content_block = soup.find_all(class_='entry-title')
    for content_block in all_content_block:
        item_href = content_block.findNext('a')
        text = item_href.text
        href = item_href.get('href')
        hrefs[text] = href

    with open(f'data/{key}.json', 'w', encoding='utf-8') as file:
        json.dump(hrefs, file, indent=4, ensure_ascii=False)





