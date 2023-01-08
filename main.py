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


def write_header_csv(path):
    with open(path, 'w', encoding='utf-8-sig') as file:
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


def write_row_csv(path, row):
    with open(path, 'a', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row)


def exist_mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def get_data(url, folder_name, part):
    # корневая папка с файлами данных
    exist_mkdir('data')

    # папка для общих файлов по разделу
    all_folder_name = f'data/{folder_name}_all'
    exist_mkdir(all_folder_name)

    # папка для детальных файлов по разделу
    details_folder_name = f'data/{folder_name}_details'
    exist_mkdir(details_folder_name)

    headers = {
        'Accept': '*/*',
        'User-Agent': UserAgent().random
    }

    # запишем заголовок для общей таблицы CSV
    write_header_csv(f'{all_folder_name}/all_poems_details.csv')

    poems_on_part = {}
    page_number = 1
    while url != None:
        print(f'...Обрабатывается страница: {page_number}')

        page_folder_name = f'{details_folder_name}/{folder_name}_page{page_number}'
        exist_mkdir(page_folder_name)

        response = r.get(url, headers=headers)
        src = response.text

        # запишем структуру HTML страницы
        with open(f'{page_folder_name}/page{page_number}.html', 'w', encoding='utf-8') as file:
            file.write(src)

        soup = BeautifulSoup(src, 'lxml')

        # собираем все ссылки на стихотворения
        poems_on_page = {}
        contents_on_page = soup.find_all(class_='entry-title')
        for content_on_page in contents_on_page:
            item = content_on_page.findNext('a')
            poems_on_page[item.get('href')] = item.text
            poems_on_part[item.get('href')] = item.text

        # запишем информацию по странице в отдельный файл JSON
        with open(f'{page_folder_name}/page{page_number}.json', 'w', encoding='utf-8') as file:
            json.dump(poems_on_page, file, indent=4, ensure_ascii=False)

        # запишем заголовок для таблицы деталей CSV
        write_header_csv(f'{page_folder_name}/page{page_number}.csv')

        # обходим каждую ссылку и собираем информацию о стихотворении
        row_list = []
        poem_count = 0
        all_count = len(poems_on_page)
        for poem_href, poem_name in poems_on_page.items():
            row = get_poem_data(poem_href, poem_name, part, headers)
            write_row_csv(f'{page_folder_name}/page{page_number}.csv', row)
            row_list.append(row)
            poem_count += 1
            print(f'...Обработано стихотворений: {poem_count} из {all_count} = {100 * poem_count / all_count}%')

        # ищем следующую страницу
        next_page = soup.find('a', class_='next page-numbers')
        url = None if next_page == None else next_page.get('href')
        page_number += 1

        # аварийный выход из цикла
        if page_number == 5000:
            break

    # запишем информацию в общий файл JSON
    with open(f'{all_folder_name}/all_poems.json', 'w', encoding='utf-8') as file:
        json.dump(poems_on_part, file, indent=4, ensure_ascii=False)

    # запишем строки в общую таблицу CSV
    for row in row_list:
        write_row_csv(f'{all_folder_name}/all_poems_details.csv', row)


def get_poem_data(url, poem_name, part, headers):
    response = r.get(url, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')

    author = get_author(poem_name)
    name = get_name(poem_name)
    text = soup.find('div', class_='poem-text').find('p').text[:15] + '...'

    category_list = []
    all_category = soup.find('ul', class_='post-categories').find_all('a')
    for category in all_category:
        category_list.append(category.text)
    category = ','.join(category_list)

    return (
        part,
        author,
        name,
        url,
        text,
        category
    )


def main():
    for key, value in DATA.items():
        get_data(url=value['url'], folder_name=key, part=value['part'])


if __name__ == '__main__':
    main()
