#/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import socket
import time
import codecs
import logging
from lxml import etree
import threading
from urllib.parse import urlparse


ssl._create_default_https_context = ssl._create_unverified_context
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.109 Safari/537.36"}
logging.basicConfig(format="%(asctime)s: <%(thread)d> [%(levelname)s] %(message)s",
                    level=logging.DEBUG,
                    filename="download-booklist.log")


def get_html(url, retries=10):
    request = urllib.request.Request(url=url, headers=headers)
    while retries > 0:
        try:
            with urllib.request.urlopen(request, timeout=5) as f:
                html = f.read()
                break
        except (urllib.error.URLError, socket.timeout):
            logging.warning("try again: " + url)
            retries -= 1
            time.sleep(1)
            continue

    if retries is 0:
        raise RuntimeWarning(f"Open URL:{url} timeout, drop it.")
    return etree.HTML(html)


class CrawBqgBook(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.book_name = None
        self.book_url = url
        p = urlparse(url)
        self.base_url = p.scheme + '://' + p.netloc
        self.save_path = ''
        self.book_info_select = None
        self.chapter_list_select = None
        self.chapter_content_select = None

    def set_save_path(self, path):
        self.save_path = path
        return self

    def set_book_info_select(self, select):
        self.book_info_select = select
        return self

    def set_chapter_list_select(self, select):
        self.chapter_list_select = select
        return self

    def set_chapter_content_select(self, select):
        self.chapter_content_select = select
        return self

    def get_book_info(self):
        try:
            html = get_html(self.book_url)
        except Exception as e:
            logging.error(e)
            return None, None
        self.book_name = html.xpath(self.book_info_select)[0].strip()
        return self.book_name, self.book_url

    def get_chapter_list(self):
        try:
            html = get_html(self.book_url)
        except Exception as e:
            logging.error(e)
            return None
        alist = html.xpath(self.chapter_list_select)
        for a in alist:
            chapter_url = a.xpath('./@href')[0].strip()
            if not chapter_url.startswith('/book'): continue
            chapter_url = self.base_url + chapter_url
            chapter_name = a.xpath('./text()')[0].strip()
            yield chapter_name, chapter_url

    def get_chapter_content(self, cname, curl):
        ret = list()
        ret.append(cname + '\n\n')
        try:
            html = get_html(curl)
        except Exception as e:
            logging.error(e)
            ret.append("Download failed.\n")
            return ret
        contents = html.xpath(self.chapter_content_select)
        for c in contents:
            scnt = c.strip()
            if len(scnt) is 0: continue
            ret.append(scnt + '\n')
        ret.append('\n\n')
        return ret

    def run(self):
        self.book_name, self.book_url = self.get_book_info()
        if self.book_name is None:
            return
        chapter_list = self.get_chapter_list()
        if chapter_list is None:
            return
        logging.info(f"Start to download {self.book_name}:{self.book_url}.")
        with codecs.open(self.save_path+self.book_name+'.txt', 'w') as file:
            for cname, curl in chapter_list:
                contents = self.get_chapter_content(cname, curl)
                file.writelines(contents)
                logging.info(f"{self.book_name}:{cname}:{curl} download ok.")
                time.sleep(3)

    def download(self):
        self.start()


def get_bqg_booklist():
    home = get_html('https://www.qu.la/wanbenxiaoshuo/')
    bl = home.xpath('//div[@id="tabData_1"]/div[1]/ul/li/a/@href')
    return ['http://www.qu.la' + l for l in bl]


if __name__ == '__main__':

    booklist = get_bqg_booklist()
    max_thread = 3 + 1

    while True:
        if len(booklist) is 0:
            break
        if threading.active_count() is max_thread:
            time.sleep(10)
            continue
        CrawBqgBook(booklist.pop()) \
            .set_save_path('/tmp/book/')\
            .set_book_info_select('//head/title/text()') \
            .set_chapter_list_select('//div[@class="box_con"][2]/div[@id="list"]/dl/dd/a') \
            .set_chapter_content_select('//div[@id="content"]/text()') \
            .download()



