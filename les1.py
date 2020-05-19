from copy import copy
import requests


class Product:
    name = 'NOT NAME'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name


class CatalogParser:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 YaBrowser/20.4.3.145 (beta) Yowser/2.5 Safari/537.36'
    }

    def __init__(self, start_url):
        self.__start_url = start_url
        self.__product_list = []

    def parse(self):
        url = self.__start_url
        while url:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            url = data.get('next')
            self.__product_list.extend([Product(**itm) for itm in data.get('results')])

    @property
    def products(self):
        return copy(self.__product_list)


if __name__ == '__main__':
    parser = CatalogParser("https://5ka.ru/api/v2/special_offers/")
    parser.parse()
    print('sdsd')