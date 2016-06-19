# -*- coding: utf-8 -*-

"""
    google_search
    ~~~~~~~~~~~~~~

    Get google search results based on search keyword.

    :copyright: (c) 2016 by Ethan.
    :license: BSD, see LICENSE for more details.
"""

import urllib2
from urllib import urlencode
from re import match
import socket

from bs4 import BeautifulSoup
from SocksiPy import socks


class GoogleSearch:

    def __init__(self, query, port):

        self.query = query.encode('utf-8')
        self.url = u"http://www.google.com/search?" + urlencode({'q': self.query})
        self.header = 'Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101'
        self.port = int(port)

    def get_search_results(self):
        search_results = list()
        html_source = ''

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", self.port)
        socket.socket = socks.socksocket

        try:
            request = urllib2.Request(self.url)
            request.add_header("User-Agent", self.header)
            html_source = urllib2.urlopen(request).read()
        except Exception as e:
            print e

        if not html_source:
            return search_results

        soup = BeautifulSoup(html_source, "html.parser")
        divs = soup.find_all('div', {'class': 'g'})
        for div in divs:
            link, title = [''] * 2
            try:
                link = div.find('a').get('href')
                title = div.find('a').text

                if link.startswith("/url?"):
                    m = match('/url\?(url|q)=(.+?)&', link)
                    if m and len(m.groups()) == 2:
                        link = urllib2.unquote(m.group(2))
            except:
                pass

            if link and title:
                search_info = {
                    'query': self.query,
                    'title': title,
                    'link': link
                }

                search_results.append(search_info)

        return search_results


def search(query, port=1234):
    google_search = GoogleSearch(query, port)
    results = google_search.get_search_results()
    return results


if __name__ == '__main__':
    query = 'react'
    search_results = search(query)
    print search_results

