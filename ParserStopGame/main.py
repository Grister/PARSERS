import requests
from bs4 import BeautifulSoup

URL = 'https://stopgame.ru/review/new/stopchoice/'
games = []


def write_in_file():
    with open('games.txt', 'a', encoding='utf-8') as file:
        for game in games:
            file.write(game + '\n')


def get_pagination(html):
    soup = BeautifulSoup(html, 'html.parser')

    pages_block = soup.find('span', class_='pages').find_all('a', class_='item')
    pages_count = [i.get_text() for i in pages_block]
    return int(pages_count[-1])


def get_html(url):
    r = requests.get(url)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item article-summary')
    games_on_page = []
    for item in items:
        games_on_page.append(item.find('div', class_='caption caption-bold').get_text(strip=True))
    return games_on_page


def parse(url):
    global games
    html = get_html(url)
    if html.status_code == 200:
        count_of_pages = get_pagination(html.text)
        for page in range(1, count_of_pages + 1):
            games_on_page = get_content((get_html(url + f'p{page}')).text)
            games.extend(games_on_page)
        write_in_file()
    else:
        print('Error')


if __name__ == '__main__':
    parse(URL)
