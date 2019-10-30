from __future__ import unicode_literals, print_function
import os
import requests
from mega import Mega
from logger import logger
from ebooklib import epub


def txt2epub(data, path):
    for name in data['content']:
        book = epub.EpubBook()
        book.set_title(data['title'])
        book.add_author(data['author'])
        chapter_list = []
        toc_list = []
        for content in data['content'][name]:
            chapter = epub.EpubHtml(title=content['title'],
                                    file_name=content['vid'][0] + '.xhtml')
            with open(path + '/' + content['vid'][0] + '.txt',
                      'r',
                      encoding='utf-8') as fp:
                chapter.content = fp.read()
            book.add_item(chapter)
            chapter_list.append(chapter)
            toc_list.append(
                epub.Link(content['vid'][0] + '.xhtml', content['title'],
                          content['vid'][0]))
        book.toc = tuple(toc_list)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav'] + chapter_list
        epub.write_epub(path + '/' + name + '.epub', book, {})


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

def download_file_from_mega_drive(url, path, name):
    mega = Mega()
    m = mega.login()
    logger.info('Use anonymous login meag success')
    logger.info('Starting download file')
    m.download_url(url, path, name)
