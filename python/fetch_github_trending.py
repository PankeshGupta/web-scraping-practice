# -*- coding: utf-8 -*-

"""
    github_trend
    ~~~~~~~~~~~~~~

    fetch github trending list.

    :copyright: (c) 2016 by Ethan.
    :license: BSD, see LICENSE for more details.
"""

import requests
from lxml.html import fromstring


class GitHubTrend:
    def __init__(self):
        self.url = 'https://github.com/trending'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.records = []

    def _get_page_source(self, url):
        r = requests.get(url, headers=self.headers)
        page_source = r.text
        return page_source

    @staticmethod
    def _get_trend_info(repo):
        name, desc, lang, stars, url = [''] * 5
        name_xpath = "./h3[@class='repo-list-name']/a"
        desc_xpath = "./p[@class='repo-list-description']"
        meta_xpath = "./p[@class='repo-list-meta']"
        try:
            name = repo.xpath(name_xpath)[0].xpath('string(.)')
            name = ''.join(name.split())
            url = 'https://github.com/' + name
        except:
            pass

        try:
            meta = repo.xpath(meta_xpath)[0].xpath('string(.)').strip()
            meta_list = [elem.strip() for elem in meta.split(u'\u2022')]
            if len(meta_list) > 2:
                lang = meta_list[0]
                stars = int(meta_list[1].split()[0])
            elif len(meta_list) > 1:
                stars = int(meta_list[0].split()[0])
        except:
            pass

        try:
            desc = repo.xpath(desc_xpath)[0].xpath('string(.)').strip()
        except Exception as e:
            print e

        repo_info = {
            'desc': desc,
            'lang': lang,
            'repo_name': name,
            'stars': stars,
            'url': url
        }

        return repo_info

    def get_trend_list(self):
        page_source = self._get_page_source(self.url)
        root = fromstring(page_source)
        repo_list = root.xpath("//li[@class='repo-list-item']")

        for repo in repo_list:
            repo_info = self._get_trend_info(repo)
            self.records.append(repo_info)

        return self.records


if __name__ == '__main__':
    gh_trend_list = GitHubTrend().get_trend_list()
    print gh_trend_list

