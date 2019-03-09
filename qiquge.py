#/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import socket

import codecs

from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context

file = codecs.open("/home/beaver/Desktop/test.txt", "w")

url = "https://www.qu.la"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.109 Safari/537.36"}

total = 0


def get_page_xpath(url):
    request = urllib.request.Request(url=url, headers=headers)
    while True:
        try:
            with urllib.request.urlopen(request, timeout=5) as f:
                html = f.read()
                break
        except urllib.error.URLError:
            print("URLError:try again: " + url)
            continue
        except socket.timeout:
            print("read timeout: again: " + url)
            continue
    return etree.HTML(html)


main_page = get_page_xpath(url)
booklist = main_page.xpath('//div[@id="hotcontent"]//div[@class="image"]//@href')
for b in booklist[:1]:
    burl = url + b
    book_page = get_page_xpath(burl)
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
        total += 1
        print("count: " + str(total) + cn + ": scratch success")

    file.close()



