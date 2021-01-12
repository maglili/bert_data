"""
crawl target and find its all alias
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from find_target import target_list #import from my own script
import ssl
import random
import time
import pickle
import re

random.seed(0)

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

id_list=[]
alias_list=[]
for id,alias in target_list.items():
    id_list.append(id)
    alias_list.append(alias)


gene_list=[]
aka_list=[]
error_list=[]

# crawler data
with open('id_and_its_alias.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # for all id, list
    count=0
    for id,alias in zip(id_list,alias_list):
        print('Working on:',id,alias)

        service_url = 'https://flybase.org/reports/' #target url
        url = service_url + id

        # if error, retry 3 times
        #=============================================================
        retry = 0
        fail_frag = False
        while True:
            try:
                html = urlopen(url, context=ctx).read()
                soup = BeautifulSoup(html, "html.parser")
                break
            except:
                if retry == 3:
                    fail_frag = True
                    break
                retry += 1
                time.sleep(5)
        if fail_frag:
            error_list.append(id)
            continue
        #=============================================================

        # Retrieve all of the anchor tags
        #=============================================================
        aka_frag = soup.find('div',string=re.compile("Also Known As"))

        symbol = soup.find('div',class_='col-sm-3 col-sm-height')
        if symbol == None:
            print('error!')
            print('='*30)
            error_list.append(id)
            continue
        gene_list.append(symbol.text)
        print('Symbol:',symbol.text)

        if aka_frag != None:
            aka_tag = soup.find('div',class_='col-xs-8')
            if aka_tag == None:
                print('error!')
                print('='*30)
                error_list.append(id)
                continue
            aka = aka_tag.text
            aka_list.append(aka)
            print('Aka:',aka)
        else:
            aka = ''
            aka_list.append(aka)
            print('Aka: ***** No alias! *****')
        #=============================================================

        # waiting some time
        wait_time = random.randint(4,6)
        time.sleep(wait_time)

        count += 1
        print('\n[No.{} finished]'.format(count))
        print('-'*30)

        # write to csv
        writer.writerow([id, symbol.text, aka])

print('gene_list:',gene_list)
with open('./alias_data/gene_list.pkl', 'wb') as a:
    pickle.dump(gene_list, a)

print('aka_list:',aka_list)
with open('./alias_data/aka_list.pkl', 'wb') as b:
    pickle.dump(aka_list, b)

print('error_list:',error_list)
with open('./alias_data/error_list.pkl', 'wb') as c:
    pickle.dump(error_list, c)
