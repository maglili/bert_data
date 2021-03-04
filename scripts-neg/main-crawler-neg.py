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

df = pd.read_csv('../csv_data/ID_set.csv',squeeze=True,header=None)  #預設使用者輸入檔案叫input.xlsx
id_list = df.tolist()

ua = UserAgent()
proxy_list = [
'12.20.241.112','138.68.60.8','209.97.150.167','191.96.42.80', '198.199.86.11', '45.33.79.26', '138.68.227.152', '45.79.39.147', '167.71.120.46', '69.65.65.178', '35.239.155.190', '52.149.152.236', '142.93.50.179'
]

try:
    aleady_parse = pd.read_csv('./neg_all-combine.csv',encoding='utf-8',header=None)[1].to_list()
except:
    aleady_parse=[]
    print('neg_all-combine.csv is empty.\n')

error_list=[]

with open('./neg_all-4.csv', 'w', newline='', encoding='utf-8') as csvfile: #<------------------------------------------change file name--------------
    writer = csv.writer(csvfile)
    count = 0

    for pmid in id_list:
        if pmid in aleady_parse:
            #print('{:<10} already existing.'.format(pmid))
            continue
        print(pmid)
        service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
        url = service_url + str(pmid)
        #==================if error, retry 3 times======================
        retry = 0
        fail_frag = False
        while True:
            try:
                proxy_ip = random.choice(proxy_list)
                proxies = {'http': proxy_ip}
                head = {'User-Agent':ua.random}
                resp = requests.get(url, headers = head, proxies=proxies)
                time.sleep(0.1)
                print('proxy:',proxies)
                print('user-agent:',head)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, "lxml")
                time.sleep(0.2)
                break
            except:
                print('************ERROR!***************')
                print('retry:',retry)
                print('************ERROR!***************')
                if retry == 3:
                    print('************ERROR!***************')
                    print('pmid:',pmid, "Can't connect.")
                    print('************ERROR!***************')
                    print('='*30)
                    fail_frag = True
                    break
                retry += 1
                time.sleep(30)
        if fail_frag:
            error_list.append(pmid)
            continue
        #=============================================================

        #==========Retrieve all of the anchor tags====================
        tags = soup.find('h1',class_='heading-title')
        if tags == None:
            print(pmid,'error! name not found!')
            print('='*30)
            error_list.append(pmid)
            continue
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
        #--------------------------------------------------
        csv_row = [title, pmid, doi, abst, year, authors]
        writer.writerow(csv_row)
        time.sleep(0.1)
        count += 1
        print('Processing',count)
        print('pmid:',pmid)
        # print('title:',title)
        # print('doi:',doi)
        # print('year:',year)
        # print('authors:',authors)
        # print('abst:',abst)
        print('='*20)

print('len of error_list',len(error_list))

with open('./error_list.pkl', 'wb') as c:
    pickle.dump(error_list, c)
