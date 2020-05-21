from copy import copy
import requests


class Product:
    name = 'NOT NAME'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name


class Category:
    __code = ''
    __name = ''
    product_list = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('parent_group_code', 'group_code'):
                self.__code = value
            elif key == ('parent_group_name', 'group_name'):
                self.__name = value
            else:
                setattr(self, f'_{key}', value)

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name


class CatalogParser:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.138 YaBrowser/20.4.3.145 (beta) Yowser/2.5 Safari/537.36'
    }

    def __init__(self, start_url, category_list_url=''):
        self.__start_url = start_url
        self.__category_list_url = category_list_url
        self.__category_list = []
        self.__product_list = []

    def parse(self, params={}):
        url = self.__start_url
        product_list = []
        while url:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            url = data.get('next')
            product_list.extend([Product(**itm) for itm in data.get('results')])
        self.__product_list.extend(product_list)
        return product_list

    def parse_by_category(self):
        response = requests.get(self.__category_list_url, headers=self.headers)
        data = response.json()
        for item in data:
            category = Category(**item)
            category.product_list = self.parse({'categories': category.code})
            self.__category_list.append(category)

    @property
    def products(self):
        return copy(self.__product_list)

    @property
    def categories(self):
        return copy(self.__category_list)


if __name__ == '__main__':
    parser = CatalogParser("https://5ka.ru/api/v2/special_offers/", category_list_url='https://5ka.ru/api/v2/categories/')
    parser.parse_by_category()
    print('sdsd')
