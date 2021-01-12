from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import time
import re
import csv

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

ID_set = []
url_o='https://pubmed.ncbi.nlm.nih.gov/?term=(((Drosophila%20melanogaster%5BTitle%2FAbstract%5D)%20OR%20(Drosophila%5BTitle%2FAbstract%5D))%20OR%20(D.%20melanogaster%5BTitle%2FAbstract%5D)&size=200&page='
page = 1

w = csv.writer(open("ID_set.csv", "w", newline='', encoding='utf-8'))

while True:
    page_str = str(page)
    url = url_o + page_str
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all('a', class_='docsum-title')
    time.sleep(3)
    if len(tags) != 0:
        print('*************page',page,'*************')
        for tag in tags:
            PMID = tag.get('href')
            PMID = re.findall('[0-9]+',PMID)
            PMID = PMID[0]
            print(PMID)
            ID_set.append(PMID)
            csv_row = [PMID]
            w.writerow(csv_row)
        page = page + 1
        time.sleep(1)
    else:
        print('*************end*************')
        break

print('total length',len(ID_set))
