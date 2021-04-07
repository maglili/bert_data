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
import numpy as np
np.random.seed(0)

df = pd.read_csv('../csv_data/ID_set.csv',squeeze=True,header=None,dtype=str)
id_list = df.tolist()
print('len of id_list:',len(id_list))

ua = UserAgent()
# https://www.us-proxy.org/
proxy_list = [
'24.193.59.8',
'191.96.42.80',
'209.97.150.167',
'138.68.60.8',
'167.172.14.115',
'207.244.230.146',
'65.57.240.121',
'52.9.37.116',
'161.35.60.153',
'161.35.177.153'
]

try:
    aleady_parse = pd.read_csv('./neg_all-combine-modify.csv',encoding='utf-8',header=None,dtype=str)[1].to_list()
    print('len of aleady_parse:', len(aleady_parse))
except:
    aleady_parse=[]
    print('neg_all-combine.csv is empty.\n')

error_list=[]

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('./') if isfile(join('./', f))]
version = 0
while True:
    filename = 'temp_'+str(version)+'.csv'
    if filename in onlyfiles:
        version += 1
    else:
        break
print('filename:', filename)
path_ = './' + filename

with open(path_, 'w', newline='', encoding='utf-8') as csvfile: #<------------------------------------------change file name--------------
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
        print('='*20)

print('len of error_list', len(error_list))
#
# with open('./error_list.pkl', 'wb') as c:
#     pickle.dump(error_list, c)
