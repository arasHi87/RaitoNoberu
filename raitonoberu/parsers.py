import os
import re
import json
import codecs
import shutil
import operator
import requests
import argparse
import collections
import urllib.request
import urllib.request

from logger import logger
from opencc import OpenCC
from fuzzywuzzy import fuzz
from epubmaker import txt2epub

import multiprocessing as mp
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
        main_group.add_argument('--download',
                                dest='download_datail',
                                help='download book')
        parser.add_argument('--cpu',
                            dest='process_count',
                            default=4,
                            type=int,
                            help='set download process count')

        args = parser.parse_args()

        # check process count is illegal
        if args.process_count <= 0:
            args.process_count = 1
            logger.warn(
                'The process you set is too less, system has already change it to 1'
            )
        elif args.process_count > 8:
            args.process_count = 8
            logger.warn(
                'The process you set is too much, system has already change it to 8'
            )

        return args


class WENKUParser:
    def __init__(self):
        self.base_url = 'https://www.wenku8.net/index.php'
        self.login_url = 'https://www.wenku8.net/login.php'
        self.main_page = 'https://www.wenku8.net/book/$.htm'
        self.search_url = 'https://www.wenku8.net/modules/article/search.php?searchtype=articlename&searchkey=$'
        self.download_url = 'http://dl.wenku8.com/packtxt.php?aid=$&vid=*&charset=big5'
        self.wenku_session = requests.Session()

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
            resp = requests.get(url=content_table_url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            title = ''
            data = {
                'content': {},
                'aid': aid,
                'title': soup.find('div', id='title').text,
                'author': soup.find('div', id='info').text.replace('作者：', '')
            }
            table = soup.find('table').find_all('tr')
            for body in table:
                contents = body.find_all('td')
                for content in contents:
                    if content['class'][0] == 'vcss':
                        title = content.text
                        data['content'][title] = []
                        # logger.info('    ' + title)
                    else:
                        if content.text != u'\xa0':
                            data['content'][title].append(
                                dict({
                                    'title':
                                    content.text,
                                    'vid':
                                    re.findall(r'[0-9]+',
                                               content.find('a')['href'])
                                }))
                            # logger.info(content.text)
            return data
        except:
            logger.warn('Can\'t find detail of {}'.format(aid))

    def show_detail(self, data):
        for idx in data['content']:
            logger.info(idx)
            for dict_data in data['content'][idx]:
                logger.info('    ' + dict_data['title'])

    def downloader(self, data, process_count):
        path = '../data/novels/' + data['title']

        # template download function
        def download():
            resp = requests.get(url, allow_redirects=True)
            with open(os.path.join(path, content['vid'][0] + '.txt'),
                      'w',
                      encoding='utf-8') as fp:
                fp.write(resp.text)

        # deal data file
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.warn(
                        'There are some error when delete old novel data, please delete it by yourself'
                    )

        # get content of every chapter
        logger.info('strating download')
        p = mp.Pool(processes=process_count)
        for name in data['content']:
            for content in data['content'][name]:
                url = self.download_url.replace('$', data['aid']).replace(
                    '*', content['vid'][0])
                p.apply_async(download())
        p.close()
        p.join()

        # convert data to epub
        txt2epub(data, path)

        # delete other file unless
        for file in os.listdir(path):
            if file.endswith('txt'):
                os.remove(os.path.join(path, file))
