from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from id_list import findid

ind = findid()
print(ind[0])


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://pubmed.ncbi.nlm.nih.gov/23063364/'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

# Retrieve all of the anchor tags
tags = soup.find('h1')
title = tags.string
title = title.strip()
print(title)

tags = soup.find(id='enc-abstract')
abst = tags.text
abst = abst.strip()
print(abst)
