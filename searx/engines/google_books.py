from lxml import html, etree

from searx.url_utils import urlencode


categories = ['books']
paging = True
url_xpath = '//h3[@class="r"]/a/@href'
title_xpath = '//h3[@class="r"]/a/text()'
author_xpath = '//div[@class="rc"]//div[@class="slp f"]/text()'
content_xpath = '//div[@class="rc"]/div[@class="s"]//span[@class="st"]/text()'
thumbnail_xpath = '//img[contains(@id, "bksthumb")]/@src'


def request(query, params):
    pageno = params['pageno'] * 10
    params['url'] = 'https://google.com/search?{query}&tbm=bks'.format(query=urlencode({'q': query,
                                                                                        'start': pageno}))
    return params


def response(resp):
    results = []

    dom = html.fromstring(resp.text)
    result_elements = zip(dom.xpath(url_xpath), dom.xpath(title_xpath), dom.xpath(author_xpath),
                          dom.xpath(content_xpath), dom.xpath(thumbnail_xpath))
    print(dom.xpath(thumbnail_xpath))
    for url, title, author, content, thumbnail in result_elements:
        print(thumbnail)
        results.append({'title': title,
                        'url': url,
                        'author': author,
                        'content': content,
                        'thumbnail': thumbnail,
                        'template': 'books.html'})

    return results
