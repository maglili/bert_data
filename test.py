
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
#from id_list import find_list
import csv
import time
import re
import pandas as pd

df = pd.read_csv('ID_set.csv',squeeze=True,header=None)  #預設使用者輸入檔案叫input.xlsx
id_list = df.tolist()


i = id_list[4508+2115-1-1+1050-1+2535-1+412-1+654-1+14928-1]


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
url = service_url + str(i)
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

print('PMID:',i)
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


'''
import urllib.request
from urllib.error import HTTPError

req = urllib.request.Request(url='https://pubmed.ncbi.nlm.nih.gov/21415126/')
try:
    handler = urllib.request.urlopen(req)
    print('1')
except HTTPError as e:
    content = e.read()
    print('2')
'''

'''
import requests
from bs4 import BeautifulSoup

r = requests.get("https://pubmed.ncbi.nlm.nih.gov/21415126/") #將網頁資料GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
tags = soup.find('h1', class_='heading-title')
print(tags)
title = tags.text
title = title.strip()
print('title:',title)
#print('---------------------------------')
'''
