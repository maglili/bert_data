from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from id_list import find_list  #import my own function
import csv
import time
import re

id_list = find_list() # all PMID
id_list.sort()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

w = csv.writer(open("output_pos.csv", "w", newline='', encoding='utf-8'))
count = 0
year_set=dict()

for i in id_list:
    service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    url = service_url + i
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup.find('h1',class_='heading-title')
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
    tags = soup.find(id='enc-abstract')
    if tags is not None:
        abst = tags.text
        abst = abst.strip()
    else:
        tags = soup.find('i', class_='empty-abstract')
        abst = tags.text
        abst = abst.strip()
    #--------------------------------------------------
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
    year_set[year]=year_set.get(year,0)+1
    #--------------------------------------------------
    tags = soup.find_all('a', class_='full-name')
    if tags is not None:
        authors = []
        for tag in tags:
            name = tag.text
            authors.append(name)
        authors = ', '.join(authors)
    else:
        authors = ''
    #--------------------------------------------------
    csv_row = [i, title, abst, doi, year, authors]
    w.writerow(csv_row)

    count += 1
    print('Processing',count)
    print('year:',year)
    time.sleep(1)

print(year_set)
