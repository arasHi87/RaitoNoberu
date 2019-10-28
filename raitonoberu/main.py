from __future__ import unicode_literals, print_function
from parsers import *

wenku_parser = WENKUParser()
arg_parser = ARGParser()


def main():
    opt = arg_parser.parser()
    if opt.search_key is not None:
        wenku_parser.searcher(opt.search_key)


if __name__ == '__main__':
    main()
