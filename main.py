import requests
import os
from bs4 import BeautifulSoup
import lxml
import time
import json
from datetime import datetime
import csv


def get_pages():

    url = 'http://casio-shops.ru/index.php?route=product/category&path=71'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    # req = requests.get(url=url, headers=headers)
    #
    # if not os.path.exists('data'):
    #     os.mkdir('data')
    #
    # with open('data/page_1.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    with open('data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages = soup.find(class_='pagination').find_all('a')
    last_page = int(pages[-1].get('href').split('page=')[1])

    for i in range(1, last_page+1):
        url = f'http://casio-shops.ru/index.php?route=product/category&path=71&page={i}'

        r = requests.get(url=url, headers=headers)

        with open(f'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(r.text)

        time.sleep(2)
    return last_page+1

def collect_data(pages_count):

    cur_date = datetime.now().strftime('%d_%m_%Y')
    data = []

    with open(f'data_{cur_date}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Модель',
                'Ссылка',
                'Цена'
            )
        )

    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        item_cards = soup.find_all(class_='product-layout')

        for item in item_cards:
            product_link = item.find('a').get('href')
            product_name = item.find('img').get('title')
            product_price = item.find(class_='price').text.strip().rstrip(' р.').replace(' ', '')

            data.append(
                {
                    'product_name' : product_name,
                    'product_link' : product_link,
                    'product_price' : product_price
                }
            )

            with open(f'data_{cur_date}.csv', 'a') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_name,
                        product_link,
                        product_price
                    )
                )


        print(f'[INFO] Обработана страница {page} из {pages_count}')

    with open(f'data_{cur_date}.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    pages_count = get_pages()
    collect_data(pages_count)


if __name__ == '__main__':
    main()
