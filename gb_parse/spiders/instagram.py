# -*- coding: utf-8 -*-
import re
import json
import scrapy
from copy import deepcopy
from urllib.parse import urlencode

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    start_urls = ['https://www.instagram.com/']
    graphql_url = 'https://www.instagram.com/graphql/query/'

    parse_users = ['realdonaldtrump', ]

    query = {
        'query_hash': '',
        'variables': '',
    }

    query_hash = {
        'profile': 'b7b84d884400bc5aa7cfe12ae843a091',
        'followers': 'c76146de99bb02f6415203be841dd25a',
        'followings': '',
        'posts': '',
        'post_detail': '',
    }

    variables = {
        'id': '',
        'include_reel': True,
        'fetch_mutual': False,
        'first': 100,
    }

    def __init__(self, login: str, passwd: str, user_list: list, **kwargs):
        self.parse_users = user_list
        self.__login = login
        self.__password = passwd
        super().__init__(**kwargs)

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method='POST',
            callback=self.main_login_parse,
            formdata={'username': self.__login, 'enc_password': self.__password},
            headers={'X-CSRFToken': csrf_token},
        )

    def main_login_parse(self, response):
        resp_data = json.loads(response.text)
        if resp_data['authenticated']:
            for user_name in self.parse_users:
                yield response.follow(
                    f'{self.start_urls[0]}{user_name}/',
                    callback=self.user_parse,
                    cb_kwargs={'user_name': user_name}
                )

    def user_parse(self, response, user_name):
        variables = deepcopy(self.variables)
        variables['id'] = self.fetch_user_id(response.text, user_name)
        followers_url = self.make_graphql_url(self.query_hash['followers'], variables)
        yield response.follow(
            followers_url,
            callback=self.followers_parse,
            cb_kwargs={'user_name': user_name, 'variables': variables}
        )

    def followers_parse(self, response, user_name, variables):
        data = json.loads(response.text)
        print(1)
        for itm in data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('edges', []):
            if itm.get('node'):
                yield itm.get('node')
        if data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('page_info', {}).get('has_next_page'):
            variables['after'] = data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('page_info', {}).\
                get('end_cursor')
            yield response.follow(
                self.make_graphql_url(self.query_hash['followers'], variables),
                callback=self.followers_parse,
                cb_kwargs={'user_name': user_name, 'variables': variables}
            )


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, user_name):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % user_name, text
        ).group()
        return json.loads(matched).get('id')

    def make_graphql_url(self, query_hash, variables):
        return f'{self.graphql_url}?query_hash={query_hash}&{urlencode(variables)}'
