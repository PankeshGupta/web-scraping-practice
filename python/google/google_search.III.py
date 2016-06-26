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
from HTMLParser import HTMLParser

from PySocks import socks
from PySocks import sockshandler


class GoogleSearch:

    def __init__(self, query, port):

        self.query = query.encode('utf-8')
        self.url = u"http://www.google.com/search?" + urlencode({'q': self.query})
        self.header = 'Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101'
        self.port = int(port)

    def get_html_source(self):
        html_source = ''

        try:
            socks.set_default_proxy(socks.SOCKS5, "localhost", self.port)
            socket.socket = socks.socksocket
            request = urllib2.Request(self.url)
            request.add_header("User-Agent", self.header)
            html_source = urllib2.urlopen(request).read()
        except Exception as e:
            print e

        return html_source

    def get_html_source_2(self):
        html_source = ''

        try:
            opener = urllib2.build_opener(sockshandler.SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1234))
            opener.addheaders = [('User-agent', self.header)]
            html_source = opener.open(self.url).read()

        except Exception as e:
            print e

        return html_source


class GoogleParser(HTMLParser):
    a_flag = False
    b_flag = False
    h3_flag = False
    title_part = ''

    def __init__(self):
        HTMLParser.__init__(self)
        self.result_info = []
        self.link = ''
        self.title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h3' and attrs == [('class', 'r')]:
            self.h3_flag = True

        if tag == 'a' and self.h3_flag:
            self.a_flag = True

        if tag == 'b' and self.a_flag:
            self.b_flag = True

        if self.a_flag:
            for (key, value) in attrs:
                if key == 'href':
                    if value.startswith("/url?"):
                        m = match('/url\?(url|q)=(.+?)&', value)
                        if m and len(m.groups()) == 2:
                            href = urllib2.unquote(m.group(2))
                            self.link = href
                    else:
                        self.link = value

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.h3_flag = False
        if tag == 'a' and self.a_flag:
            self.a_flag = False
            self.result_info.append({
                'title': self.title_part,
                'href': self.link
            })
            self.title_part = ''

    def handle_data(self, data):
        if self.a_flag:
            self.title_part += data


def search(query, port=1234):
    google_search = GoogleSearch(query, port)
    # page_source = google_search.get_html_source()
    page_source = google_search.get_html_source_2()

    google_parser = GoogleParser()
    google_parser.feed(page_source)
    google_parser.close()

    results = google_parser.result_info

    return results

if __name__ == '__main__':
    result_info = search('flask', 1234)
    print result_info
