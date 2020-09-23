from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from id_list import find_list
import csv
import time
import re

id_list = find_list()
i = id_list[300]
print('PMID:',i)
print('---------------------------------')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
url = service_url + i
print('url:',url)
print('---------------------------------')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup.find('h1', class_='heading-title')
title = tags.text
title = title.strip()
print('title:',title)
print('---------------------------------')

tags = soup.find('span', class_='identifier doi')
if tags is not None:
    doi = tags.text
    doi = doi.strip()
    doi = doi.split()
    doi = doi[1]
else:
    doi = ''
print('doi:',doi)
print('---------------------------------')


tags = soup.find(id='enc-abstract')
if tags is not None:
    abst = tags.text
    abst = abst.strip()
else:
    tags = soup.find('i', class_='empty-abstract')
    abst = tags.text
    abst = abst.strip()
print('abst:',abst)
print('---------------------------------')

tags = soup.find('span', class_='cit')
if tags is not None:
    year = tags.text
    #year = year.strip()
    #year = year.split()
    #year = year[0]
    year = re.findall('[0-9]+',year)
    year = year[0]
    year=''.join(year)
    year = year.strip()
else:
    year = ''
print('year:',year)
print('---------------------------------')

tags = soup.find_all('a', class_='full-name')
authors = []
for tag in tags:
    name = tag.text
    authors.append(name)
authors = ', '.join(authors)
print('authors:',authors)
