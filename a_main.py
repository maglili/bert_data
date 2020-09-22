from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from id_list import find_list  #import my own function
import csv

id_list = find_list() # all PMID

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

w = csv.writer(open("a_output.csv", "w", newline='', encoding='utf-8'))
count = 0

for i in id_list:
    service_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    url = service_url + i
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    tags = soup.find('h1',class_='heading-title')
    title = tags.text
    title = title.strip()

    tags = soup.find('span', class_='identifier doi')
    if tags is not None:
        doi = tags.text
        doi = doi.strip()
        doi = doi.split()
        doi = doi[1]
    else:
        doi = '***No DOI in page!***'


    tags = soup.find(id='enc-abstract')
    if tags is not None:
        abst = tags.text
        abst = abst.strip()
    else:
        tags = soup.find('i', class_='empty-abstract')
        abst = tags.text
        abst = abst.strip()

    csv_row = [title, i, doi, abst]
    w.writerow(csv_row)

    count += 1
    print('Processing',count)
