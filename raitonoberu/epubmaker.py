from __future__ import unicode_literals, print_function
import os
import urllib.request
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
            with open(path + '/' + content['vid'][0] + '.txt', 'r',
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
