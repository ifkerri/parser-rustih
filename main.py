from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests as r
import csv
import json
import os
from input_data import DATA


def get_author(text):
    pos = text.find('—')
    author_list = text[:pos].strip().split()
    author_list.reverse()
    author = ' '.join(author_list)
    return (author)


def get_name(text):
    pos = text.find('—')
    name = text[pos + 1:].strip()
    # print(name)
    return (name)


def get_data(url, folder_name, part):
    if not os.path.exists('data'):
        os.mkdir('data')

    headers = {
        'Accept': '*/*',
        'User-Agent': UserAgent().random
    }

    page_number = 1
    while url != None:
        print(f'Обрабатывается страница: {page_number}')

        page_folder_name = f'data/{folder_name}_page{page_number}'
        if not os.path.exists(page_folder_name):
            os.mkdir(page_folder_name)

        response = r.get(url, headers=headers)
        src = response.text

        with open(f'{page_folder_name}/page{page_number}.html', 'w', encoding='utf-8') as file:
            file.write(src)

        soup = BeautifulSoup(src, 'lxml')

        # собираем все ссылки на стихотворения
        poems_on_page = {}
        contents_on_page = soup.find_all(class_='entry-title')
        for content_on_page in contents_on_page:
            item = content_on_page.findNext('a')
            poems_on_page[item.get('href')] = item.text

        # запишем информацию в файл JSON
        with open(f'{page_folder_name}/page{page_number}.json', 'w', encoding='utf-8') as file:
            json.dump(poems_on_page, file, indent=4, ensure_ascii=False)

        # запишем заголовок таблицы CSV
        with open(f'{page_folder_name}/page{page_number}.csv', 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    'Раздел',
                    'Автор',
                    'Название',
                    'Ссылка',
                    'Стихотворение (отрывок)',
                    'Категории'
                )
            )

        # обходим каждую ссылку и собираем информацию о стихотворении
        # for poem_href, poem_name in poems_on_page.items():
        #     a=1

        # ищем следующую страницу
        next_page = soup.find('a', class_='next page-numbers')
        url = None if next_page == None else next_page.get('href')
        page_number += 1

        # аварийный выход из цикла
        if page_number == 10:
            break
    # for key, details in input_data.items():
    #
    #     response = r.get(details['url'], headers=headers)
    #     src = response.text
    #
    #     with open(f'data/{key}.html', 'w', encoding='utf-8') as file:
    #         file.write(src)
    #
    #     poem_on_page = {}
    #     soup = BeautifulSoup(src, 'lxml')
    #     all_content_block = soup.find_all(class_='entry-title')
    #     for content_block in all_content_block:
    #         item_href = content_block.findNext('a')
    #         text = item_href.text
    #         href = item_href.get('href')
    #         poem_on_page[text] = href
    #
    #     with open(f'data/{key}.json', 'w', encoding='utf-8') as file:
    #         json.dump(poem_on_page, file, indent=4, ensure_ascii=False)

    # with open(f'data/{key}.csv', 'w', encoding='utf-8-sig') as file:
    #     row = ['Раздел', 'Автор', 'Автор2', 'Название', 'Стих', 'Категории', 'Ссылка']
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(row)

    # count = 0
    # all_count = len(poem_on_page)
    # for text, href in poem_on_page.items():
    #     count += 1
    #     response = r.get(url=href, headers=headers)
    #     src = response.text
    #     soup = BeautifulSoup(src, 'lxml')
    #
    #     author = get_author(text)
    #     author2 = author
    #     poem_name = get_name(text)
    #
    #     poem_text = []
    #     all_part_poem_text = soup.find('div', class_='poem-text').findChildren()
    #     for part_poem_text in all_part_poem_text:
    #         class_adsbygoogle = part_poem_text.get('class')
    #         if class_adsbygoogle == ['adsbygoogle']:
    #             break
    #         poem_text.append(str(part_poem_text))
    #     poem_text_ = ' '.join(poem_text)
    #
    #     category_list = []
    #     all_category = soup.find('ul', class_='post-categories').find_all('a')
    #     for category in all_category:
    #         category_list.append(category.text)
    #     category_text = ','.join(category_list)
    #     # print(category_text)
    #
    #     poem_href = href
    #
    #     with open(f'data/{key}.csv', 'a', encoding='utf-8-sig') as file:
    #         row = [value.get('part'), author, author2, poem_name, poem_text_, category_text, poem_href]
    #         writer = csv.writer(file, delimiter=';')
    #         writer.writerow(row)
    #
    #     print(f'...Обработано: {100 * count / all_count}%')
    # poem_text =
    # author2 = get_author_gent(author, morph)
    # break
    # count+=1
    # if count > 3:
    #     break
    # row = [
    #     value.get('part'),
    #
    # ]
    # with open(f'data/{key}.csv', 'a', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(row)


def main():
    for key, value in DATA.items():
        get_data(url=value['url'], folder_name=key, part=value['part'])


if __name__ == '__main__':
    main()
