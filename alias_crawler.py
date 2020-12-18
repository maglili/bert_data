from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re

id_list = find_list() # all PMID
id_list.sort()
