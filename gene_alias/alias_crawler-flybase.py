import requests
from bs4 import BeautifulSoup
import csv
import time
import pickle
import random
import re
import pandas as pd
random.seed(0)

aleady_parse = pd.read_csv('./csv_data/flybase_gene-combine.csv',encoding='utf-8',header=None)[0].to_list()

with open('./pickles/gene_data.pickle', 'rb') as handle:
    gene_data = pickle.load(handle)

error_list=[]

# crawler data
with open('./csv_data/flybase_gene-part-1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    count = 0

    for fbid in gene_data.keys():
        if fbid in aleady_parse:
            continue

        service_url = 'http://flybase.org/reports/' # target url
        url = service_url + fbid
        #===================if error, retry 3 times====================
        retry = 0
        fail_frag = False
        while True:
            try:
                resp = requests.get(url)
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, "lxml")
                break
            except:
                if retry == 3:
                    print('************ERROR!***************')
                    print('fnid:',fbid, "Can't connect.")
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

        #=====================save pages===============================
        page_html = soup.prettify()
        file_name = './htmls/'+fbid+'.txt'
        with open(file_name,'w',encoding="utf-8") as file:
            file.write(page_html)
        #=============================================================

        #=========== Retrieve all of the anchor tags===================
        aka_frag = soup.find('div',string=re.compile("Also Known As")) #check if aka exist
        table = soup.find_all('div',class_='col-sm-3 col-sm-height')

        if table == []:
            error_list.append(fbid)
            print('************ERROR!***************')
            print('fbid:',fbid,'table = [], table not exists.!')
            print('Fbid may changed!')
            print('************ERROR!***************')
            print('='*30)
            continue

        symbol = table[0].text
        name = table[2].text
        CG_id = table[3].text

        print('symbol:',symbol)
        print('name:',name)
        print('CG_id',CG_id)

        if aka_frag != None:
            aka_tag = soup.find('div',class_='col-xs-8')
            aka = aka_tag.text
            print('Aka:',aka)
        else:
            aka = ''
            print('Aka: ***** No alias! *****')
        #=============================================================

        # ============waiting some time===============================
        wait_time = random.randint(3,5)
        time.sleep(wait_time)

        count += 1
        print('\n[No.{} finished]'.format(count))
        print('='*30)

        # write to csv
        writer.writerow([fbid, name, CG_id, symbol, aka])

print('len of error_list',len(error_list))

with open('./pickles/flybase/error_list.pkl', 'wb') as f:
    pickle.dump(error_list, f)

# with open('./pickles/flybase/error_list.pkl', 'rb') as f:
#     error_list = pickle.load(f)
