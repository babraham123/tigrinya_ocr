#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script to crawl the Eritrean newspaper archive. Saves the results to a csv
# Add an output folder and max_files to download from an existing csv

# python crawler.py
# python crawler.py ../train/ 100

# sudo apt-get install python-bs4
# sudo pip3 install beautifulsoup4

import urllib2, csv, requests, sys, os.path
from bs4 import BeautifulSoup
from datetime import datetime
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

# omit www.
main_urls = [
    'http://shabait.com/eritrea-haddas',
    'http://shabait.com/haddas-ertra'
]
domain = ''
path = '/'
output_csv = 'newspaper_urls.csv'
output_dir = ''
# ordered sets, ignore dict value
pdf_urls = {}
visited_urls = {}
visited = 0
max_visited = 10000
chunk_size = 1000000  # 1 MB

def parse_url(url):
    global visited, visited_urls, pdf_urls, domain, path

    visited += 1
    if not url or visited > max_visited:
        return []
    
    url = url.lower()
    if url in visited_urls:
        return []

    visited_urls[url] = True
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    except:
        return []

    if not soup or not soup.body:
        return []

    next_urls = {}
    for link in soup.find_all('a'):
        link_url = link.get('href')
        next_url = None
        # print(link_url)
        try:
            link_parts = urlsplit(link_url)
        except:
            continue

        if link_parts.path.endswith('.pdf'):
            # newspaper url
            pdf_urls[link_url] = True
        elif link_parts.netloc in [domain, 'www.' + domain]:
            # absolute url in domain
            next_url = link_url
        elif link_parts.path.startswith(path):
            # relative url in subdomain
            next_url = 'http://' + domain + link_url

        if next_url and next_url not in visited_urls:
            next_urls[next_url] = True

    return list(next_urls.keys())


def parser_runner(url):
    try:
        next_urls = parse_url(url)
    except:
        return
    for next_url in next_urls:
        parser_runner(next_url)


def walk_sequentially(url, param, increment):
    global pdf_urls

    i = 0
    last_num_pdfs = len(pdf_urls)
    while True:
        next_url = url + '?' + param + '=' + str(i)
        links = parse_url(next_url)
        num_pdfs = len(pdf_urls)
        if i > max_visited or (num_pdfs - last_num_pdfs) < 1:
            break

        last_num_pdfs = num_pdfs
        i += increment


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


def download_pdf_file(url, index, num_urls):
    parts = urlsplit(url)
    prefix = extract_time(parts.path)
    base_name = os.path.splitext(os.path.basename(parts.path))[0]
    filename = str(index).zfill(len(str(num_urls))) + '_' + prefix + '_' + base_name + '.pdf'
    filename = os.path.join(output_dir, filename)

    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def discovery():
    global domain, path

    for url in main_urls:
        parts = urlsplit(url)
        domain = parts.netloc
        path = parts.path
        # parser_runner(url)  # too hard, doesn't work
        walk_sequentially(url, 'start', 7)

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


def download(output_dir, num_pdfs):
    urls = []
    with open(output_csv) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')    
        for row in readCSV:
            urls.append(row[2])

    j = 0
    num_urls = len(urls)
    increment = num_urls // num_pdfs
    for i in range(0, num_urls, increment):
        try:
            download_pdf_file(url, i, num_urls)
            j += 1
        except:
            continue
        print('Number of pdfs downloaded: ', j)


def main():
    if len(sys.argv) == 3:
        output_dir = sys.argv[1]
        num_pdfs = sys.argv[2]
        if not os.path.isdir(output_dir):
            print('Folder doesnt exist!')
            exit()
        download(output_dir, num_pdfs)
    else:
        discovery()


if __name__ == '__main__':
    main()
