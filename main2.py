from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


options = Options()
options.add_argument("--disable-notifications")

brower = webdriver.Chrome('./chromedriver', chrome_options=options)
brower.get("https://pubmed.ncbi.nlm.nih.gov/?term=(((Drosophila%20melanogaster%5BTitle%2FAbstract%5D)%20OR%20(Drosophila%5BTitle%2FAbstract%5D))%20OR%20(D.%20melanogaster%5BTitle%2FAbstract%5D)&filter=years.1906-1917&page=1")
time.sleep(3)

brower.find_element_by_css_selector('button.load-button.next-page').click()

soup = BeautifulSoup(brower.page_source, 'html.parser')
tags = soup.find_all('a', class_='docsum-title')
for tag in tags:
    print(tag.get('href'))
