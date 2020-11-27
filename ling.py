import json
import urllib
import requests
from pprint import pprint as pp


class LinguaLeo:

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password
        self.full_vocabulary = []
        self.groups_names = []

        self.session = requests.Session()

    def logining(self):
        if not (self.login and self.password):
            print('Login and password were not defined yet')
            return
        url ='http://api.lingualeo.com/login'
        params = {"email": self.login, "password": self.password}
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return True
        print('Login and password are incorrect')
        print(f'status code = {response.status_code}')
        return

    def get_full_vocabulary(self):
        url = 'https://api.lingualeo.com/GetWords'
        per_page = 10000
        self.get_groups_names()
        for n, group in enumerate(self.groups_names):
            data = {'perPage': per_page, 'dateGroup': group}
            response = self.session.post(url, data)
            status_code = response.status_code
            if not status_code == 200:
                print(f'Unsuccessful getting full vocabulary')
            self.full_vocabulary += response.json()['data'][n]['words']
            print(f'Successful getting full vocabulary')

    def get_groups_names(self):
        url = 'https://api.lingualeo.com/GetWords'
        response = self.session.post(url)
        status_code = response.status_code
        if not status_code == 200:
            print(f'Unsuccessful getting groups names')
        response = response.json()['data']
        for group in response:
            self.groups_names.append(group['groupName'])
        print(self.groups_names)





#
#
# s = requests.Session()
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
# params = {"email": 'axmarun@mail.ru', "password": 'antonhmarun'}
# url = 'http://api.lingualeo.com/login'
#
# r1 = s.get(url, params=params)
# print(r1)
#
# url2 = 'https://api.lingualeo.com/GetWords'
# r2 = s.post(url2, {'perPage': 200})
# words = r2.json()['data'][0]['words']
#
# list_of_words = []
# for word in words:
#     list_of_words.append(word['nwd'])
#
# print(len(list_of_words))
# print(list_of_words)
#

# response2 = s.get('https://lingualeo.com/ru/dictionary/vocabulary/my', stream=True)
# print(response2.raw)


# print(response2.text)

#
# class Lingualeo:
#     def __init__(self, email, password):
#         self.email = email
#         self.password = password
#
#     def auth(self):
#         url = "http://api.lingualeo.com/api/login"
#         values = {"email": self.email, "password": self.password}
#         return self.get_content(url, values)
#
#     def get_page(self, page_number):
#         url = 'http://lingualeo.com/ru/userdict/json'
#         values = {'filter': 'all', 'page': page_number}
#         return self.get_content(url, values)['userdict3']
#
#     def get_content(self, url, values):
#         data = urllib.urlencode(values)
#         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
#         req = opener.open(url, data)
#         return json.loads(req.read())
#
#     def get_all_words(self):
#         """
#         The JSON consists of list "userdict3" on each page
#         Inside of each userdict there is a list of periods with names
#         such as "October 2015". And inside of them lay our words.
#         Returns: type == list of dictionaries
#         """
#         words = []
#         have_periods = True
#         page_number = 1
#         while have_periods:
#             periods = self.get_page(page_number)
#             if len(periods) > 0:
#                 for period in periods:
#                     words += period['words']
#             else:
#                 have_periods = False
#             page_number += 1
#         return words