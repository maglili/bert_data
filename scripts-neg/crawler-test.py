import pickle
import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import pandas as pd
from fake_useragent import UserAgent
import random
random.seed(0)

ua = UserAgent()
proxy_list = [
'12.20.241.112','138.68.60.8','209.97.150.167','191.96.42.80', '198.199.86.11', '45.33.79.26', '138.68.227.152', '45.79.39.147', '167.71.120.46', '69.65.65.178', '35.239.155.190', '52.149.152.236', '142.93.50.179'
]

service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
url = service_url + str(823263)

proxy_ip = random.choice(proxy_list)
proxies = {'http': proxy_ip}
head = {'User-Agent':ua.random}
resp = requests.get(url, headers = head, proxies=proxies)
print('proxy:',proxies)
print('user-agent:',head)

resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, "lxml")

tags = soup.find('h1',class_='heading-title')
if tags == None:
    print(pmid,'error! name not found!')
    print('='*30)
    error_list.append(pmid)
title = tags.text
title = title.strip()
#--------------------------------------------------
tags = soup.find('span', class_='identifier doi')
if tags is not None:
    doi = tags.text
    doi = doi.strip()
    doi = doi.split()
    doi = doi[1]
else:
    doi = ''
#--------------------------------------------------
if soup.find(id='enc-abstract') is not None:
    tags = soup.find(id='enc-abstract')
    abst = tags.text
    abst = abst.strip()
    abst = abst.split()
    abst = ' '.join(abst)
elif soup.find(class_='empty-abstract') is not None:
    tags = soup.find(class_='empty-abstract')
    abst = tags.text
    abst = abst.strip()
elif soup.find('div',class_='abstract') is not None:
    tags = soup.find('div',class_='abstract').find('p')
    abst = tags.text
    abst = abst.strip()
    abst = abst.split()
    abst = ' '.join(abst)
#--------------------------------------------------
tags = soup.find('span', class_='cit')
if tags is not None:
    year = tags.text
    year = re.findall('[0-9]+',year)
    year = year[0]
    year=''.join(year)
    year = year.strip()
else:
    year = ''
#--------------------------------------------------
tags = soup.find_all('a', class_='full-name')
if tags is not None:
    authors = []
    for tag in tags:
        name = tag.text
        authors.append(name)
    authors = list(set(authors))
    authors = ', '.join(authors)
else:
    authors = ''


print('title:',title)
print('doi:',doi)
print('year:',year)
print('authors:',authors)
print('abst:',abst)
