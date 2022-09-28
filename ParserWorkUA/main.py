# Плохо работает запись в файл и результат по одной странице!

import csv

import requests
from bs4 import BeautifulSoup

URL = 'https://www.work.ua/ru/jobs-инженер-схемотехник/'
vacancies = []


def get_url(url):
    r = requests.get(url)
    return r


def save_file():
    with open('jobs.csv', 'w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вакансия', 'Компания', 'Город', 'Зарплата'])
        for item in vacancies:
            writer.writerow([item['name'], item['company'], item['city'], item['salary']])


def get_salary(html):
    salary = html.find('b').get_text()
    if 'грн' in salary:
        return salary
    else:
        return 'З/п не указана'


def get_content(html):
    global vacancies
    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')
    for job in jobs:
        discription = job.find('div', class_='flex-gap-rl')
        vacancies.append(dict(name=job.find('h2').get_text(strip=True),
                              company=discription.find_all('span')[0].get_text(),
                              city=discription.find_all('span')[2].get_text(),
                              salary=get_salary(job)))

    save_file()


def main():
    html = get_url(URL)
    get_content(html.text)


if __name__ == '__main__':
    main()
