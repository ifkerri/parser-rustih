from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests as r
import csv
import json
import pymorphy2


def get_author(text):
    pos = text.find('—')
    author_list = text[:pos].strip().split()
    author_list.reverse()
    author = ' '.join(author_list)
    # print(author)
    return (author)


def get_name(text):
    pos = text.find('—')
    name = text[pos+1:].strip()
    # print(name)
    return (name)


# def get_author_gent(author, morph):
#     parse_author = morph.parse(author)[0]
#     gent = parse_author.inflect({'gent'})
#     print(gent.word)
#     return gent.word

# morph = pymorphy2.MorphAnalyzer()
input_data = {
    'rus_poet_klassik': {
        'url': 'https://rustih.ru/stihi-russkih-poetov-klassikov/',
        'part': 'Русские'
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

    with open(f'data/{key}.csv', 'w', encoding='utf-8') as file:
        row = ['Раздел', 'Автор', 'Автор2', 'Название', 'Стих', 'Категории', 'Ссылка']
        writer = csv.writer(file, delimiter='|')
        writer.writerow(row)

    count = 0
    for text, href in hrefs.items():
        response = r.get(url=href, headers=headers)
        src = response.text
        soup = BeautifulSoup(src, 'lxml')

        author = get_author(text)
        author2 = author
        poem_name = get_name(text)

        poem_text = []
        all_part_poem_text = soup.find('div', class_='poem-text').findChildren()
        for part_poem_text in all_part_poem_text:
            class_adsbygoogle = part_poem_text.get('class')
            if class_adsbygoogle == ['adsbygoogle']:
                break
            poem_text.append(str(part_poem_text))
        poem_text_ = ' '.join(poem_text)

        category_list = []
        all_category = soup.find('ul', class_='post-categories').find_all('a')
        for category in all_category:
            category_list.append(category.text)
        category_text = ','.join(category_list)
        # print(category_text)

        poem_href = href

        with open(f'data/{key}.csv', 'a', encoding='utf-8') as file:
            row = [value.get('part'), author, author2, poem_name, poem_text_, category_text, poem_href]
            writer = csv.writer(file, delimiter='|')
            writer.writerow(row)

        # poem_text =
        # author2 = get_author_gent(author, morph)
        # break
        count+=1
        if count > 1:
            break
        # row = [
        #     value.get('part'),
        #
        # ]
        # with open(f'data/{key}.csv', 'a', encoding='utf-8') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(row)
