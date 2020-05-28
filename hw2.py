import requests
from typing import List, Dict
from bs4 import BeautifulSoup


class Vacancy:
    title = ''
    salary = []
    url = ''
    src = ''
    employer = ''
    adr = ''


class HeadHunterParser:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 YaBrowser/20.4.3.145 (beta) Yowser/2.5 Safari/537.36'
    }
    params = {
        'st': 'searchVacancy',
        'area': '2',
        'text': 'аналитик+данных'
    }

    __url = 'https://spb.hh.ru/search/vacancy'
    __base_url = 'https://spb.hh.ru/search/vacancy'

    def __init__(self):
        self.vacancy = []
        self.parse(self.__url)

    def get_page(self, url: str) -> BeautifulSoup:
        resp = requests.get(url, headers=self.headers, params=self.params)
        soup = BeautifulSoup(resp.text, 'lxml')
        return soup

    def get_next_page(self, soup: BeautifulSoup) -> str:
        pass

    def get_vacancy_list(self, soup: BeautifulSoup) -> List[Vacancy]:
        pass

    def parse(self, url: str):
        while url:
            soup = self.get_page(url)
            self.vacancy.extend(self.get_vacancy_list(soup))
            url = self.get_next_page(soup)


if __name__ == '__main__':
    parser = HeadHunterParser()
