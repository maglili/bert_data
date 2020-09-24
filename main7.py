import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import pandas as pd

df = pd.read_csv('ID_set.csv',squeeze=True,header=None)  #預設使用者輸入檔案叫input.xlsx
id_list = df.tolist()

w = csv.writer(open("output7.csv", "w", newline='', encoding='utf-8'))
count = 0
year_set=dict()

for i in range(4508+2115-1-1+1050-1+2535-1,len(id_list)):
    service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    url = service_url + str(id_list[i])
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    time.sleep(1)
    # Retrieve all of the anchor tags
    tags = soup.find('h1',class_='heading-title')
    time.sleep(1)
    if tags is None:
        for i in range(20):
            time.sleep(5)
            tags = soup.find('h1',class_='heading-title')
            print('***retry',i,'***')
            time.sleep(10)
            if tags is not None:
                break
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
    pmid = id_list[i]
    csv_row = [title, pmid, doi, abst, year, authors]
    w.writerow(csv_row)

    count += 1
    print('Processing',count)
    print('year:',year)
