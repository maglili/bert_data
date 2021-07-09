import requests
from bs4 import BeautifulSoup
import csv
import time
import pickle
import random
import re
import pandas as pd
from fake_useragent import UserAgent

random.seed(0)
ua = UserAgent()

proxy_list = [
    "165.227.11.196:80",
    "54.159.195.75:80",
    "18.218.92.184:80",
    "104.131.109.66:8080",
    "4.79.109.100:80",
    "63.249.67.70:53281",
    "161.35.97.206:80",
    "54.156.164.61:80",
    "164.90.148.162:8080",
    "159.65.171.69:80",
    "65.160.224.144:80",
    "74.143.245.221:80",
    "165.227.108.19:80",
]

try:
    aleady_parse = pd.read_csv(
        "./csv_data/bgee_gene-combine.csv", encoding="utf-8", header=None
    )[0].to_list()
except:
    aleady_parse = []
    print("bgee_gene-combine.csv is empty.\n")

with open("./pickles/gene_data.pickle", "rb") as handle:
    gene_data = pickle.load(handle)

error_list = []

# crawler data
with open(
    "./csv_data/bgee_gene-part-5.csv", "w", newline="", encoding="utf-8"
) as csvfile:
    writer = csv.writer(csvfile)
    count = 0

    for fbid in gene_data.keys():
        if fbid in aleady_parse:
            # print(fbid,'already existing.')
            continue

        service_url = "https://bgee.org/?page=gene&gene_id="  # target url
        url = service_url + fbid

        # ==================if error, retry 3 times======================
        retry = 0
        fail_frag = False
        while True:
            try:
                proxy_ip = random.choice(proxy_list)
                proxies = {"http": proxy_ip}
                head = {"User-Agent": ua.random}
                resp = requests.get(url, headers=head, proxies=proxies)
                print("proxy:", proxies)
                print("user-agent:", head)
                resp.encoding = "utf-8"
                soup = BeautifulSoup(resp.text, "lxml")
                break
            except:
                if retry == 3:
                    print("************ERROR!***************")
                    print("fbid:", fbid, "Can't connect.")
                    print("************ERROR!***************")
                    print("=" * 30)
                    fail_frag = True
                    break
                retry += 1
                time.sleep(30)
        if fail_frag:
            error_list.append(fbid)
            continue
        # =============================================================

        # ==========Retrieve all of the anchor tags====================
        Name = soup.find("td", attrs={"property": "bs:name"})
        if Name == None:
            print(fbid, "error! name not found!")
            print("=" * 30)
            error_list.append(fbid)
            continue
        print("\nName:", Name.text)

        Synonyms_list = []
        Synonyms_tags = soup.find_all("span", attrs={"property": "bs:alternateName"})
        if Synonyms_tags == None:
            print(fbid, "error! Synonyms_tags == None")
            print("=" * 30)
            error_list.append(fbid)
            continue

        for i in range(len(Synonyms_tags)):
            Synonyms_list.append(Synonyms_tags[i].text)
        print("\nSynonyms_list:\n", Synonyms_list)

        # ===========================================================

        # waiting some time
        # wait_time = random.randint(1,2)
        time.sleep(0.1)

        count += 1
        print("\n[No.{} finished]".format(count))
        print("-" * 30)

        # write to csv
        writer.writerow([fbid, Name.text, ", ".join(Synonyms_list)])

print("len of error_list:", len(error_list))

with open("./pickles/bgee/error_list.pkl", "wb") as c:
    pickle.dump(error_list, c)

# with open('./pickles/bgee/error_list.pkl', 'rb') as f:
#     error_list = pickle.load(f)
