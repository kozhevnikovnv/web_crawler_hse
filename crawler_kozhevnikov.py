from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

import requests
import lxml
import sys

DOMAIN = 'koroteev.site'
HOST = 'http://' + DOMAIN
FILTER = ['#', 'tel:', 'mailto:']
links = set()  # множество всех ссылок
response = requests.get(HOST)
sys.setrecursionlimit(10000)
cnt = 1
f = open('urls.txt', 'w')

# создаем функцию, принимающую url и глубину рекурсии
def add_all_links_recursive(url, maxdepth=4):
    # создаем список ссылок, которые потом будут рекурсивно обрабатываться
    links_to_handle_recursive = []
    global cnt

    # получаем html код страницы
    request = requests.get(url)

    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'lxml')
    f1 = open(f'data/{cnt}.html', mode='w', encoding='utf-8')
    f1.write(str(soup))
    f1.close()
    f.write(f'{cnt} {url}\n')
    cnt += 1

    # рассматриваем все теги <a>, в которых href не пустой
    for tag_a in soup.find_all('a', href=lambda v: v is not None):
        link = tag_a['href']

        # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(part) for part in FILTER):

            # проверяем, относительная ли ссылка, если так - то дополняем ее
            if link.startswith('/') and not link.startswith('//'):
                # преобразуем относительную ссылку в абсолютную
                link = HOST + link

            # проверяем, что ссылка ведёт на нужный домен
            # и что мы ещё не обрабатывали такую ссылку
            if urlparse(link).netloc == DOMAIN and link not in links:
                links.add(link)
                links_to_handle_recursive.append(link)

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            add_all_links_recursive(link, maxdepth=maxdepth - 1)


def main():
    add_all_links_recursive(HOST + '/')


if __name__ == '__main__':
    main()
