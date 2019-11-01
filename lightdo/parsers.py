import os
import re
import time
import json
import codecs
import shutil
import operator
import requests
import argparse
import collections
import urllib.request

from opencc import OpenCC
from fuzzywuzzy import fuzz
from lightdo.logger import logger
from bs4 import BeautifulSoup as bs
from lightdo.utils import txt2epub, download_file_from_google_drive, download_file_from_mega_drive

import multiprocessing as mp
import http.cookiejar as cookielib

loc = os.path.dirname(__file__)


class ARGParser:
    def parser(self):
        parser = argparse.ArgumentParser()
        main_group = parser.add_mutually_exclusive_group()
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
        parser.add_argument('--wenku',
                            dest='wenku_seacher',
                            default='online',
                            help='set wenku searcher to online/local')

        # wenku local data parser
        main_group.add_argument(
            '--redata',
            dest='wenku_redata',
            type=int,
            default=0,
            help=
            'reget all wenku local data, please enter the latest you want renew'
        )
        main_group.add_argument('--renew',
                                dest='wenku_renew',
                                action='store_true',
                                default=False,
                                help='renew wenku local data')

        # wenku account、password set
        parser.add_argument('--clean',
                            dest='clean_wenku_account',
                            action='store_true',
                            default=False,
                            help='clean your wenku account')
        parser.add_argument('--wenku_account',
                            '-wa',
                            dest='wenku_account',
                            help='set your wenku account')
        parser.add_argument('--wenku_password',
                            '-wp',
                            dest='wenku_password',
                            help='set your wenku password')
        parser.add_argument('--anonymous',
                            '-am',
                            dest='is_anonymous',
                            action='store_true',
                            default=False,
                            help='this will not store your account')

        # set download opintion
        parser.add_argument('--path',
                            dest='save_path',
                            default='.',
                            help='set download path')

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

        # check download path is true
        if not os.path.isdir(args.save_path):
            logger.error('Please enter a correct path')
            exit(-1)

        # check wenku renew data's end
        # if args.wenku_redata < 2700:
        #     args.wenku_redata = 2700
        #     logger.warn('The end is to small, system has alreay change it to 2700')

        return args


class WENKUParser:
    def __init__(self, account, password):
        self.base_url = 'https://www.wenku8.net/index.php'
        self.login_url = 'https://www.wenku8.net/login.php'
        self.main_page = 'https://www.wenku8.net/book/$.htm'
        self.search_url = 'https://www.wenku8.net/modules/article/search.php?searchtype=articlename&searchkey=$'
        self.download_url = 'http://dl.wenku8.com/packtxt.php?aid=$&vid=*&charset=big5'
        self.wenku_session = requests.Session()
        self.data = {}
        self.config = {}

        # lode data
        with open(os.path.join(loc, 'data/wenku/data.json'),
                  'r',
                  encoding='utf8') as fp:
            self.data = json.load(fp)

        # load config
        with open(os.path.join(loc, 'data/config.json'), 'r') as fp:
            self.config = json.load(fp)

    def login(self):
        # login into wenku
        postData = {
            'username': self.config['wenku']['account'],
            'password': self.config['wenku']['password'],
            'usecookie': '315360000',
            'action': 'login'
        }
        self.wenku_session.cookies = cookielib.LWPCookieJar(
            filename=os.path.join(loc, 'data/wenku/cookie.txt'))
        try:
            # use cookie login
            self.wenku_session.cookies.load()
            resp = self.wenku_session.get(self.base_url)
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')
            not_login = soup.find('caption')
            if not_login:
                # use account logging
                if not self.config['wenku']['account'] or not self.config[
                        'wenku']['password']:
                    logger.error('You need to login wenku then you can search')
                    return -1
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

    def re_get_data(self, end=2700):
        for i in range(1, end):
            result = self.get_main_page(i)
            if result:
                self.data.update(result)
                with open(os.path.join(loc, 'data/wenku/data.json'),
                          'w',
                          encoding='utf8') as fp:
                    json.dump(self.data, fp, ensure_ascii=False)

    def renew(self):
        # get lastes number from data
        page = int(max(self.data, key=int)) + 1
        while True:
            result = self.get_main_page(page)
            page += 1
            if result:
                self.data.update(result)
                with open(os.path.join(loc, 'data/wenku/data.json'),
                          'w',
                          encoding='utf8') as fp:
                    json.dump(self.data, fp, ensure_ascii=False)
            else:
                logger.info('It\'s already renewed wenku\'s data to lastest')
                break

    def local_searcher(self, key):
        result = {}
        rating = 0
        key = OpenCC('tw2s').convert(key)
        for idx in self.data.keys():
            result[idx] = fuzz.partial_token_set_ratio(self.data[idx], key)
        result = collections.OrderedDict(
            sorted(result.items(), key=operator.itemgetter(1), reverse=True))
        for idx in result:
            if result[idx] < 50:
                break
            logger.info("%4s : %s" % (idx, self.data[idx]['title']))

    def online_searcher(self, key):
        try:
            logger.info('======= wenku =======')
            self.login()
            key = OpenCC('tw2s').convert(key)
            resp = self.wenku_session.get(url=self.search_url.replace(
                '$', requests.utils.quote(key, encoding='gbk')))
            resp.encoding = 'gbk'
            soup = bs(resp.text, 'html.parser')

            # get search result
            if soup.find('caption', text=re.compile('搜索结果')):
                # multi search result
                max_page = int(soup.find('a', class_='last').text)
                for i in range(2, max_page + 2):
                    novels = soup.find_all('a', text=re.compile(key))
                    for novel in novels:
                        logger.info('%4s : %s' % (re.findall(
                            r'[/][0-9]+', novel['href'])[0].replace(
                                '/', ''), novel.text))
                    if (i == max_page + 1):
                        break
                    time.sleep(5)
                    url = self.search_url.replace(
                        '$', requests.utils.quote(
                            key, encoding='gbk')) + '&page=' + str(i)
                    resp = self.wenku_session.get(url=url)
                    resp.encoding = 'gbk'
                    soup = bs(resp.text, 'html.parser')
            else:
                # singal search
                aid = re.findall(r'=[0-9]+',
                                 soup.find('a',
                                           text='加入书架')['href'])[0].replace(
                                               '=', '')
                title = self.get_main_page(aid)[str(aid)]['title']
                logger.info('%4s : %s' % (aid, title))
        except Exception as e:
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
                'title':
                OpenCC('s2tw').convert(soup.find('div', id='title').text),
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

    def downloader(self, data, process_count, save_path):
        # path = 'lightdo/data/novels/' + data['title']

        # template download function
        def download():
            resp = requests.get(url, allow_redirects=True)
            with open(os.path.join(save_path, content['vid'][0] + '.lightdo'),
                      'w',
                      encoding='utf-8') as fp:
                fp.write(resp.text)

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
        txt2epub(data, save_path)

        # delete other file unless
        for file in os.listdir(save_path):
            if file.endswith('lightdo'):
                os.remove(os.path.join(save_path, file))


class EPUBSITEParser:
    def __init__(self):
        self.base_url = 'http://epubln.blogspot.com/'
        self.search_url = 'http://epubln.blogspot.com/search/'
        self.download_url = 'https://docs.google.com/uc?export=download'

    def searcher(self, key):
        logger.info('===== epub site =====')
        resp = requests.get(url=self.search_url, params={'q': key})
        resp.encoding = 'utf-8'
        soup = bs(resp.text, 'html.parser')
        if '找不到與查詢字詞' in soup.find('h2', class_='pagetitle').text:
            logger.warn('epub site can\'t find the match result')
        else:
            results = soup.find_all('a', rel='bookmark', text=re.compile(key))
            for result in results:
                logger.info('%13s : %s' % (result['href'].replace(
                    self.base_url, '').replace('.html', ''), result.text))

    def downloader(self, _id, save_path):
        # get main page
        resp = requests.get(url=self.base_url + _id + '.html')
        resp.encoding = 'utf-8'
        soup = bs(resp.text, 'html.parser')
        title = soup.find('a', rel='bookmark').text
        google_url = soup.find('a', text='google')
        mega_url = soup.find('a', text='mega')
        if google_url:
            google_url = google_url['href']
            try:
                logger.info('Strating download use google drive')
                _id = google_url.replace(
                    'https://drive.google.com/file/d/', '').replace(
                        '/view?usp=sharing',
                        '').replace('https://drive.google.com/open?id=', '')
                download_file_from_google_drive(
                    _id, os.path.join(save_path, title + '.epub'))
                logger.info('Download successful')
            except Exception as e:
                logger.warn(
                    'There are some error when download, please try later \n {}'
                    .format(e))
        elif mega_url:
            mega_url = mega_url['href']
            try:
                logger.info('Strating download use mega drive')
                download_file_from_mega_drive(mega_url, save_path + '/',
                                              title + '.epub')
                logger.info('Download successful')
            except Exception as e:
                logger.warn(
                    'There are some error when download, please try later \n {}'
                    .format(e))
        else:
            logger.warn('There has no source can download')


class XBOOKParser:
    def __init__(self):
        self.base_url = 'https://x.book100.com/'
        self.search_url = 'https://x.book100.com/search/result/'

    def searcher(self, key):
        logger.info('======= xbook =======')
        resp = requests.get(url=self.search_url, params={'key': key})
        resp.encoding = 'utf-8'
        soup = bs(resp.text, 'html.parser')
        books = soup.find('div', class_='items').find_all('li')
        for book in books:
            result = book.find('a')
            logger.info('{} : {}'.format(
                re.findall(r'[0-9]+', result['href'])[0],
                result.text.replace('\n', '')))
