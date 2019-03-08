#/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import ssl
import socket
from bs4 import BeautifulSoup
import codecs

from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context

file = codecs.open("/home/beaver/Desktop/test.txt", "w")

url = "https://www.qu.la"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/72.0.3626.109 Safari/537.36"}

req = urllib.request.Request(url=url, headers=headers)
with urllib.request.urlopen(req) as uf:
    hx = etree.HTML(uf.read())
    booklist = hx.xpath('//div[@id="hotcontent"]//div[@class="image"]//@href')

    for b in booklist[:1]:
        burl = url + b
        req = urllib.request.Request(url=burl, headers=headers)
        with urllib.request.urlopen(req) as buf:
            dom = etree.HTML(buf.read())
            div = dom.xpath('//div[@class="box_con"]')[1]
            al = div.xpath('//dd/a')
            for a in al:
                curl = a.xpath('./@href')[0]
                if not curl.startswith('/book'):
                    continue
                curl = url + curl
                cn = a.xpath('./text()')[0]

                print(cn + ": " + curl)
                req = urllib.request.Request(url=curl, headers=headers)
                with urllib.request.urlopen(req, timeout=5) as cuf:
                    try:
                        dom = etree.HTML(cuf.read())
                    except (socket.timeout, urllib.error.URLError):
                        continue

                    # write chapter
                    file.write(cn.encode('utf-8').decode().strip() + "\n")
                    content = dom.xpath('//div[@id="content"]/text()')
                    for c in content:
                        c = c.encode('utf-8').decode().strip()
                        if len(c) is 0:
                            continue
                        elif len(c) > 0:
                            c += '\n'
                        file.write(c)
                    file.write("\n\n\n")

            file.close()



