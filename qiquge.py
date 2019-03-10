#/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import socket
import time
import codecs

from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.qu.la"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.109 Safari/537.36"}


def get_page_xpath(url, retries=10):
    request = urllib.request.Request(url=url, headers=headers)
    while retries > 0:
        try:
            with urllib.request.urlopen(request, timeout=5) as f:
                html = f.read()
                break
        except (urllib.error.URLError, socket.timeout):
            print("ry again: " + url)
            retries -= 1
            time.sleep(1)
            continue

    if retries is 0:
        raise Exception("Timeout, stop.")
    return etree.HTML(html)


def get_page_element(url, retries=10, select="/"):
    return get_page_xpath(url, retries).xpath(select)


main_page = get_page_xpath(url)
booklist = main_page.xpath('//div[@class="l"]/div/dl//a')

# booklist = get_page_element(url, select='//div[@class="l"]/div/dl//a/text() | //div[@class="l"]/div/dl//a/@href')
# print(booklist)
# exit(0)

for book in booklist[1:]:
    book_name = book.xpath('./text()')[0].strip()
    book_url = url + book.xpath('./@href')[0].strip()
    with codecs.open(f"/home/beaver/Desktop/{book_name}.txt", "w") as file:
        print("Write: " + file.name)
        book_page = get_page_xpath(book_url)
        div = book_page.xpath('//div[@class="box_con"]')[1]
        al = div.xpath('//dd/a')
        for a in al:
            curl = a.xpath('./@href')[0]
            if not curl.startswith('/book'):
                continue
            curl = url + curl
            cn = a.xpath('./text()')[0]

            print(cn + ": " + curl)
            chapter_page = get_page_xpath(curl)
            file.write(cn.encode('utf-8').decode().strip() + "\n")
            content = chapter_page.xpath('//div[@id="content"]/text()')
            for c in content:
                c = c.encode('utf-8').decode().strip()
                if len(c) is 0:
                    continue
                elif len(c) > 0:
                    c += '\n'
                file.write(c)
            file.write("\n\n\n")
            print(cn + ": download OK.")
            time.sleep(2)




