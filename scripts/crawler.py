#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to crawl the Eritrean newspaper archive
# sudo apt-get install python-bs4
# sudo pip3 install beautifulsoup4

import urllib2, csv
from bs4 import BeautifulSoup
from datetime import datetime
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

main_urls = [
    'http://shabait.com/eritrea-haddas',
    'http://shabait.com/haddas-ertra'
]
domain = ''
output_csv = 'newspaper_urls.csv'
# ordered sets, ignore dict value
pdf_urls = {}
visited_urls = {}
visited = 0

def parse_url(url):
    global visited
    global visited_urls
    global pdf_urls

    visited += 1
    if url in visited_urls:
        return {}

    visited_urls[url] = True
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    next_urls = {}

    for link in soup.find_all('a'):
        link_url = link.get('href')
        print(link_url)
        if link_url.endswith('.pdf'):
            pdf_urls[link_url] = True
        elif domain in link_url:
            next_urls[link_url] = True

    return list(next_urls.keys())


def parser_runner(url):
    next_urls = parse_url(url)
    for next_url in next_urls:
        parser_runner(next_url)


def extract_time(path):
    blank = '-'
    name = path.split('.')[-1]
    if len(name) < 8:
        return blank
    time_str = name[-8:]
    if not time_str.isnumeric():
        return blank
    try:
        datetime_obj = datetime.strptime(time_str, '%m%d%Y')
        return datetime_obj.strftime('%Y_%m_%d')
    except ValueError:
        return blank


def main():
    global domain

    for url in main_urls:
        parts = urlsplit(url)
        domain = parts.netloc
        parser_runner(url)

    print('Number of urls visited: ', len(visited_urls))
    print('  out of ', visited, ' steps')
    print('Number of pdfs found: ', len(pdf_urls))
    pdf_domains = {}

    with open(output_csv, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for url in pdf_urls:
            parts = urlsplit(url)
            pdf_domains[parts.netloc] = True
            time_str = extract_time(parts.path)
            writer.writerow([time_str, parts.netloc, url])

    print('Domains found (', len(pdf_domains), '): ', list(pdf_domains.keys()))


if __name__ == '__main__':
    main()
