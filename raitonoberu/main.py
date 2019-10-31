from __future__ import unicode_literals, print_function
from parsers import *

epubsite_parser = EPUBSITEParser()
wenku_parser = WENKUParser()
arg_parser = ARGParser()


def main():
    opt = arg_parser.parser()
    if opt.wenku_redata is not 0:
        wenku_parser.re_get_data()
    elif opt.wenku_renew:
        wenku_parser.renew()
    elif opt.search_key is not None:
        if opt.wenku_seacher == 'online':
            wenku_parser.online_searcher(opt.search_key)
        else:
            wenku_parser.local_searcher(opt.search_key)
        epubsite_parser.searcher(opt.search_key)
    elif opt.search_detail is not None:
        search_detail = opt.search_detail.split(':')
        source = search_detail[0]
        _id = search_detail[1]
        if source == 'wenku':
            wenku_parser.show_detail(wenku_parser.detail(_id))
    elif opt.download_datail is not None:
        download_datail = opt.download_datail.split(':')
        source = download_datail[0]
        _id = download_datail[1]
        if source == 'wenku':
            wenku_parser.downloader(wenku_parser.detail(_id),
                                    opt.process_count)
        elif source == 'epub':
            epubsite_parser.downloader(_id)


if __name__ == '__main__':
    main()
