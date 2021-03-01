import pickle
import pandas as pd
import csv
import re
from tqdm import tqdm

with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

reverse_data_dict_biogrid_lower = {} # lower case version of reverse_data_dict_biogrid

for key, value in reverse_data_dict_biogrid.items():
    key = key.lower()
    if key not in reverse_data_dict_biogrid_lower:
        reverse_data_dict_biogrid_lower[key] = value

df = pd.read_csv('../csv_data/output_pos.csv', header=None, encoding='utf-8')
df = df[[0,2]]

with open('labeling.tsv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')

    for idx in tqdm(range(len(df))):
        pmid, text_1 = df.iloc[idx]
        text_1 = text_1.lower()
        text_1 = ' '.join(text_1.split())
        #print(text_1)

        writer.writerow([text_1])
        writer.writerow(['index', 'article_pmid','entity_text','entity_fbid','start_position','end_position'])

        # rule 1: scan the alias that comtaining white space.
        # e.g. T beta h,  Dm Rg3
        save_range=[]
        for key,value in reverse_data_dict_biogrid.items():
            if ' ' in key:
                if key in text_1:
                    start_position = text_1.find(key)
                    end_position = start_position + len(key)
                    if text_1[start_position:end_position] != key:
                        print('Position Error!')
                        quit()
                    # print('pmid:',pmid)
                    # print('key:',key)
                    # print('start_position:',start_position)
                    # print('end_position:',end_position)
                    # print('-'*20)
                    save_range.append(range(start_position, end_position))
                    writer.writerow([idx, pmid, key, reverse_data_dict_biogrid[key], start_position, end_position])
            else:
                continue

        # rule 2: scan the alias that only 1 word.
        # e.g. olfD, sbl, bss
        text_1_split = re.split('\s|/',text_1)
        #text_1_split = text_1.split()
        start_position = 0
        end_position = 0
        for word in text_1_split:
            skip_frag = False
            end_position = start_position + len(word)
            for range_ in save_range:
                if start_position in range_: # Guarantee alias won't be add redundantly
                    skip_frag = True
                    continue
            if word in reverse_data_dict_biogrid and skip_frag == False:
                if text_1[start_position:end_position] != word:
                    print('Position Error!')
                    quit()
                # print('pmid:',pmid)
                # print('word:',word)
                # print('start_position:',start_position)
                # print('end_position:',end_position)
                # print('-'*20)
                writer.writerow([idx, pmid, word,reverse_data_dict_biogrid[word], start_position, end_position])
            start_position = end_position + 1
        #print('='*20)

        writer.writerow([])
        writer.writerow(['-'*20])
        writer.writerow([])
