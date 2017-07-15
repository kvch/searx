from lxml import html, etree

from searx.url_utils import urlencode


categories = ['books']
paging = True
url_xpath = '//a[@class="bookTitle"]/@href'
title_xpath = '//a[@class="bookTitle"]/span/text()'
author_xpath = '//a[@class="authorName"][1]/span[@itemprop="name"]/text()'
content_xpath = '//div//span[@class="greyText smallText uitext"]/text()'
thumbnail_xpath = '//img[@class="bookSmallImg"]/@src'


def request(query, params):
    params['url'] = 'https://goodreads.com/search?{query}'.format(query=urlencode({'query': query,
                                                                                   'page': params['pageno']}))
    return params


def response(resp):
    results = []

    dom = html.fromstring(resp.text)
    result_elements = zip(dom.xpath(url_xpath), dom.xpath(title_xpath), dom.xpath(author_xpath),
                          dom.xpath(content_xpath), dom.xpath(thumbnail_xpath))
    for url, title, author, content, thumbnail in result_elements:
        results.append({'title': title,
                        'url': 'https://goodreads.com' + url,
                        'author': author,
                        'content': content.strip(),
                        'thumbnail': thumbnail, 
                        'template': 'books.html'})
    return results
