import os
import requests
from string import punctuation
from bs4 import BeautifulSoup

URL = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'


def get_html(url):
    return requests.get(url).content


def save_content(name, content, path):
    for i in punctuation + ' ':
        name = name.replace(i, '_')
    if name[-1] == '_':
        name = name[:-1]

    full_path = os.path.join(path, name)
    with open(f'{full_path}.txt', 'wb') as file:
        file.write(content.encode('UTF-8'))


def get_content(html, type_articles, page):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')
    print(f"Parse page {page[-1]}...")
    for article in articles:
        article_type = article.find('span', "c-meta__type").text.strip()
        if article_type == type_articles:
            link = article.find('a').get('href')
            content = get_html(f'https://www.nature.com{link}')
            soup = BeautifulSoup(content, 'html.parser')
            name = soup.find('h1').text
            article_text = soup.find('div', class_='c-article-body').text.strip()
            save_content(name, article_text, page)


def main():
    count_of_pages = int(input("Amount of pages to parse: "))
    type_articles = input("Type articles to parse: ")
    print('Start parse')

    for page in range(1, count_of_pages + 1):
        folder_name = f'Page_{page}'
        path = os.path.join(os.getcwd(), folder_name)
        os.mkdir(path)
        get_content(get_html(URL + f'&page={page}'), type_articles, path)

    print('Saved all articles.')


if __name__ == '__main__':
    main()
