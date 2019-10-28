from __future__ import unicode_literals, print_function
from parsers import *

wenku_parser = WENKUParser()
arg_parser = ARGParser()


def main():
    opt = arg_parser.parser()
    if opt.search_key is not None:
        wenku_parser.searcher(opt.search_key)
    elif opt.search_detail is not None:
        search_detail = opt.search_detail.split(':')
        source = search_detail[0]
        _id = search_detail[1]
        if source == 'wenku':
            wenku_parser.detail(_id)


if __name__ == '__main__':
    main()
