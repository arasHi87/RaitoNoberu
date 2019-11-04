from __future__ import unicode_literals, print_function
import json
from lightdo.parsers import *
from lightdo.logger import logger

arg_parser = ARGParser()
opt = arg_parser.parser()
loc = os.path.dirname(__file__)

############## pre deal action ##############
# wenku login option
if not opt.is_anonymous:
    config = {}

    # open and load config
    with open(os.path.join(loc, 'data/config.json'), 'r') as fp:
        config = json.load(fp)

    # change config
    if opt.wenku_account:
        config['wenku']['account'] = opt.wenku_account
    if opt.wenku_password:
        config['wenku']['password'] = opt.wenku_password

    # save config
    with open(os.path.join(loc, 'data/config.json'), 'w') as fp:
        json.dump(config, fp)

epubsite_parser = EPUBSITEParser()
# xbook_parser = XBOOKParser()
wenku_parser = WENKUParser(opt.wenku_account, opt.wenku_password)

# clean wenku account
if opt.clean_wenku_account:
    with open(os.path.join(loc, 'data/config.json'), 'w') as fp:
        json.dump({}, fp)
    logger.info('Already clean your login information')


############### main function ###############
# main function
def main():
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
    elif opt.search_id is not None:
        if opt.is_wenku:
            wenku_parser.show_detail(wenku_parser.detail(opt.search_id))
    elif opt.download_id is not None:
        if opt.is_wenku:
            wenku_parser.downloader(wenku_parser.detail(opt.download_id),
                                    opt.process_count, opt.save_path, opt.download_number)
        elif opt.is_epubsite:
            epubsite_parser.downloader(opt.download_datail, opt.save_path)


if __name__ == '__main__':
    main()
