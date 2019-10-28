import re
import json
import operator
import requests
import argparse
import collections
from logger import logger
from opencc import OpenCC
from fuzzywuzzy import fuzz
from urllib.parse import quote
import http.cookiejar as cookielib
from bs4 import BeautifulSoup as bs
from config import WENKU_USERNAME, WENKU_PASSWORD


class ARGParser:
    def parser(self):
        parser = argparse.ArgumentParser()
        main_group = parser.add_mutually_exclusive_group(required=True)
        # search parser
        main_group.add_argument('--search',
                                dest='search_key',
                                help='Search keyword')
        main_group.add_argument('--detail',
                                dest='search_detail',
                                help='get the book\'s detail')
        args = parser.parse_args()
        return args


class WENKUParser:
    def __init__(self):
        self.base_url = 'https://www.wenku8.net/index.php'
        self.login_url = 'https://www.wenku8.net/login.php'
        self.main_page = 'https://www.wenku8.net/book/$.htm'
        self.search_url = 'https://www.wenku8.net/modules/article/search.php?searchtype=articlename&searchkey=$'
        self.download_url = 'dl.wenku8.com/packtxt.php?aid=$&vid=*&charset=big5'
        self.wenku_session = requests.Session()
        # self.data = {}

        # lode data
        # with open('../data/wenku/data.json', 'r', encoding='utf8') as fp:
        #     self.data = json.load(fp)

    def login(self):
        # login into wenku
        postData = {
            'username': WENKU_USERNAME,
            'password': WENKU_PASSWORD,
            'usecookie': '315360000',
            'action': 'login'
        }
        self.wenku_session.cookies = cookielib.LWPCookieJar(
            filename='../data/wenku/cookie.txt')
        try:
            # use cookie login
            self.wenku_session.cookies.load()
            resp = self.wenku_session.get(self.base_url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            not_login = soup.find('caption')
            if not_login:
                # use account logging
                resp = self.wenku_session.post(self.login_url, data=postData)
                resp.encoding = 'gbk'
                self.wenku_session.cookies.save()
                logger.info('use account login wenku')
            else:
                logger.info('use cookie login wenku')
            return 1
        except:
            logging.error('Fail to login wenku, plz try later')
            return -1

    def get_main_page(self, aid):
        try:
            url = self.main_page.replace('$', str(aid))
            resp = requests.get(url=url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            title = soup.find('span').find('b').text
            author = soup.find('td', text=re.compile('小说作者')).text.replace(
                '小说作者：', '').strip()
            content_table_url = soup.find('a', text='小说目录')['href']
            # logger.info('Renew {} successful'.format(aid))
            return {
                str(aid): {
                    "title": title,
                    "author": author,
                    "content_table_url": content_table_url
                }
            }
        except:
            logger.warn('Can\'t find novel {}'.format(str(aid)))

    # def re_get_data(self, end=2700):
    #     for i in range(1, end):
    #         result = self.get_main_page(i)
    #         if result:
    #             self.data.update(result)
    #             with open('../data/wenku/data.json', 'w',
    #                       encoding='utf8') as fp:
    #                 json.dump(self.data, fp, ensure_ascii=False)

    # def renew(self):
    #     # get lastes number from data
    #     page = int(max(self.data, key=int)) + 1
    #     while True:
    #         result = self.get_main_page(page)
    #         page += 1
    #         if result:
    #             self.data.update(result)
    #             with open('../data/wenku/data.json', 'w',
    #                       encoding='utf8') as fp:
    #                 json.dump(self.data, fp, ensure_ascii=False)
    #         else:
    #             logger.info('It\'s already renewed wenku\'s data to lastest')
    #             break

    # def local_searcher(self, key):
    #     result = {}
    #     rating = 0
    #     key = OpenCC('tw2s').convert(key)
    #     print(key)
    #     for idx in self.data.keys():
    #         result[idx] = fuzz.partial_token_set_ratio(self.data[idx], key)
    #     result = collections.OrderedDict(
    #         sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    #     for idx in result:
    #         if result[idx] < 50:
    #             break
    #         logger.info("%4s : %s" % (idx, self.data[idx]['title']))

    def searcher(self, key):
        try:
            self.login()
            key = OpenCC('tw2s').convert(key)
            resp = self.wenku_session.get(url=self.search_url.replace(
                '$', requests.utils.quote(key, encoding='gbk')))
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            if soup.find('caption', text=re.compile('搜索结果')):
                # multi search result
                novels = soup.find_all('a', text=re.compile(key))
                for novel in novels:
                    logger.info(
                        '%4s : %s' %
                        (re.findall(r'[/][0-9]+', novel['href'])[0].replace(
                            '/', ''), novel.text))
            else:
                # singal search
                aid = re.findall(r'=[0-9]+',
                                 soup.find('a',
                                           text='加入书架')['href'])[0].replace(
                                               '=', '')
                title = self.get_main_page(aid)[str(aid)]['title']
                logger.info('%4s : %s' % (aid, title))
        except:
            logger.error('Fail to search wenku')

    def detail(self, aid):
        try:
            url = self.main_page.replace('$', str(aid))

            # get the content table of book's link
            resp = requests.get(url=url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            content_table_url = soup.find('a', text='小说目录')['href']

            # get main page
            data = {}
            resp = requests.get(url=content_table_url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            author = soup.find('div', id='info').text.replace('作者：', '')
            title = ''
            table = soup.find('table').find_all('tr')
            for body in table:
                contents = body.find_all('td')
                for content in contents:
                    if content['class'][0] == 'vcss':
                        title = content.text
                        data[title] = []
                        logger.info('    ' + title)
                    else:
                        if content.text != u'\xa0':
                            data[title].append(content.text)
                            logger.info(content.text)
        except Exception as e:
            logger.warn('Can\'t find detail of {} \n {}'.format(aid, e))
