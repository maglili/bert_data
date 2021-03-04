import pandas as pd
songs_pmid = pd.read_csv('./song_id.csv', encoding='utf-8', index_col=0, squeeze=True)
songs_pmid = songs_pmid.to_list()
#print(len(songs_pmid))

# neg_data = pd.read_csv('../csv_data/output_neg_all.csv', encoding='iso-8859-1', header=None, dtype=str)
# neg_data = neg_data[1]
# neg_data = neg_data.to_list()
#print(len(neg_data))

# count = 0
# for id in songs_pmid:
#     if id in neg_data:
#         count += 1
#print(count)
#==========================================================================================================
import pickle
import random
import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from fake_useragent import UserAgent

random.seed(0)
ua = UserAgent()

proxy_list = [
'54.211.23.200:80',
'34.203.142.175:80',
'165.227.11.196:80',
'74.143.245.221:80',
'206.189.189.81:3128',
'198.211.109.14:80',
'52.27.65.162:80',
'12.186.206.85:80',
'138.68.60.8:8080',
'191.96.42.80:8080',
'3.17.223.220:8080',
'198.199.86.11:3128'
]

try:
    aleady_parse = pd.read_csv('./csv_data/pubmed-combine.csv',encoding='utf-8',header=None)[0].to_list()
except:
    aleady_parse=[]
    print('pubmed-combine.csv is empty.\n')

error_list=[]

with open('./sons_neg_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    count=0

    for pmid in songs_pmid:
        if pmid in aleady_parse:
            #print(fbid,'already existing.')
            continue
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
                print('proxy:',proxies)
                print('user-agent:',head)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, "lxml")
                break
            except:
                print('************ERROR!***************')
                print('retry:',retry)
                print('************ERROR!***************')
                if retry == 3:
                    print('************ERROR!***************')
                    print('pmid:',fbid, "Can't connect.")
                    print('************ERROR!***************')
                    print('='*30)
                    fail_frag = True
                    break
                retry += 1
                time.sleep(30)
        if fail_frag:
            error_list.append(fbid)
            continue
        #=============================================================

        #==========Retrieve all of the anchor tags====================
        tags = soup.find('h1',class_='heading-title')
        if tags == None:
            print(fbid,'error! name not found!')
            print('='*30)
            error_list.append(fbid)
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
            authors = ', '.join(authors)
        else:
            authors = ''
        #===========================================================
        csv_row = [title, str(pmid), doi, abst, year, authors]
        writer.writerow(csv_row)
        time.sleep(0.1)

        count += 1
        print('Processing',count)
        print('year:',year)
        print('='*20)

print('len of error_list',len(error_list))

with open('./error_list.pkl', 'wb') as c:
    pickle.dump(error_list, c)
