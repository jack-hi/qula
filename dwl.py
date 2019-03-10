#/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import socket
import time
import codecs
import logging
from lxml import etree
import argparse


# argparse
parser = argparse.ArgumentParser()
parser.add_argument("url", help="Url for downloading.")
parser.add_argument("-f", "--file", default="/tmp/dwl.txt", help="The file for store.")
parser.add_argument("-l", "--logging", default="/tmp/dwl.log", help="The logging file.")
args = parser.parse_args()

ssl._create_default_https_context = ssl._create_unverified_context

base_url = "https://www.qu.la"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.109 Safari/537.36"}
logging.basicConfig(format="%(asctime)s: %(message)s",
                    level=logging.DEBUG,
                    filename=args.logging)


def get_page_xpath(url, retries=10):
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
        raise Exception("Timeout, stop.")
    return etree.HTML(html)


def get_page_element(url, retries=10, select="/"):
    return get_page_xpath(url, retries).xpath(select)


chapter_list = get_page_element(args.url, select="//div[@class='box_con'][2]/div[@id='list']/dl/dd/a")
with codecs.open(args.file, 'w') as file:
    for c in chapter_list:
        chapter_url = c.xpath('./@href')[0]
        if not chapter_url.startswith('/book'):
            continue
        chapter_url = base_url + chapter_url
        chapter_name = c.xpath('./text()')[0].strip()
        file.write(chapter_name + '\n\n')
        chapter_content = get_page_element(chapter_url, select='//div[@id="content"]/text()')
        for cnt in chapter_content:
            scnt = cnt.strip()
            if len(scnt) is 0: continue
            file.write(scnt + '\n')
        file.write('\n\n\n\n')
        logging.info(chapter_name + ': ' + chapter_url + ', download ok.')
        time.sleep(2)

