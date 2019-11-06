# RAITO NOBERU

Raito Noberu can help you find light novel in every website already make parser, and also can help you convert those novels only have txt to epub.  

Now suppose the following website.  

* [wenku8](https://www.wenku8.net/index.php)

* [epubsite](http://epubln.blogspot.com/)

And expected to suppose following website.  

* [qb](https://www.x23qb.com/book/1230/)

And following are stop suppose for some reason.

* [shencou](http://www.shencou.com/)  
This is cause it's response is too slow, if you want you can see shencou branch and add by yourself.
* [xbook100](http://www.shencou.com/)  
This is cause it's pagination mechanism is too strange, if you want you can help me too fix it.  

## Installation

clone and install by your self.

```bash
git clone https://github.com/arasHi87/RaitoNoberu
cd raitonoberu
python setup.py install
```

Or you can just install by use pip.

```bash
pip install lightdo
```

## Usage

***Important***  
Before search you need to login wenku first, or wenku search will fail, or if you don't want to record you account/passeword then you can use anonymous option and login every time. And the default download folder will be the path where you run the command (CLI path).

***login wenku***  
login in first time, and you don't need to care about login problem after it, or you can add --anonymous to login without save data.

```bash
lightdo -wa your_account -wp your_password
```

***Search keyword***  
The following login you don't need to do that if you have already login and didn't use anonymous option. And there are something special for wenku8 searcher. It has online mode and local mode, the different is that is online search result is over 1 page, every page have limit to wait 5 sec, so if you don't want to wait you can use `--wenku local` to set searcher to local.

```bash
lightdo --search mEOw -wa your_account -wp your_password --anonymous
```

***Get the Detail***  
Now this option just suppose wenku8 (also just wenku8 need it), it will give you all chapter of all season of this book, you need to add `id` which will give you when you search, and in final you need to add `-w` option to choose wenku8 to get detail.

```bash
lightdo --detail 8787 -w
```

***Download novel***  
This will help you download novel, if source is wneku8, it will download it by txt and convert it to epub automatically. If you doesn't set `--number id` to choose the season you want, it will help you download all season. In epubsite it will just download the novel you designation.Finally remember to designation the source where you want to download, we have `-w` to wenku8 and `-e` to epubsite, and there also have cpu option can set, the default is 4 process, if you think is too many or too less you can use `--cpu 87` to set.

```bash
lightdo --download 8787 -w --path novels --number 87
```

***Redata wenku8***  
This option you maybe will never use it, it will try to reget all wenku8 data, so we suggest you don't use this option, if you really want to use it...... just do it!

```bash
# the number is the limit you want to get from wenku8, suggest is 3000
lightdo --redata 3000
```

***Renew wenku8***  
It will renew wenku data, and it will try to get from the lastest you got until it can't, if you just want to renew your local wenku8 data, just ue this, don't use redata.

```bash
lightdo --renew
```

***All options***

```
usage: lightdo [-h] [--search SEARCH_KEY] [--detail SEARCH_ID]
               [--download DOWNLOAD_ID] [--cpu PROCESS_COUNT]
               [--wenku WENKU_SEACHER] [--redata WENKU_REDATA] [--renew]
               [--clean] [--wenku_account WENKU_ACCOUNT]
               [--wenku_password WENKU_PASSWORD] [--anonymous]
               [--path SAVE_PATH] [--number DOWNLOAD_NUMBER] [-w] [-e]

optional arguments:
  -h, --help            show this help message and exit
  --search SEARCH_KEY   Search keyword
  --detail SEARCH_ID    get the book's detail
  --download DOWNLOAD_ID
                        download book
  --cpu PROCESS_COUNT   set download process count
  --wenku WENKU_SEACHER
                        set wenku searcher to online/local
  --redata WENKU_REDATA
                        reget all wenku local data, please enter the latest
                        you want renew
  --renew               renew wenku local data
  --clean               clean your wenku account
  --wenku_account WENKU_ACCOUNT, -wa WENKU_ACCOUNT
                        set your wenku account
  --wenku_password WENKU_PASSWORD, -wp WENKU_PASSWORD
                        set your wenku password
  --anonymous, -am      this will not store your account
  --path SAVE_PATH      set download path
  --number DOWNLOAD_NUMBER
                        set number you want to download, default is download
                        all
  -w                    set type to wenku
  -e                    set type to epubsite
```

## License

This project is licensed under the MIT License - see the [MIT](https://choosealicense.com/licenses/mit/) for details
