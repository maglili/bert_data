"""
Object: Scan through all positive data(abstracts) and label the gene.
"""
import pickle
import pandas as pd
import csv
import re
from tqdm import tqdm

# reverse_data_dict_biogrid: combining flybase, bgee, biogrid aliases
with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

df = pd.read_csv('../csv_data/output_pos.csv', header=None, encoding='utf-8')
df = df[[0,2]]

# writing the output file
with open('labeling.tsv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')

    count = 0

    for idx in tqdm(range(len(df))):
        pmid, text_1 = df.iloc[idx]
        text_1 = text_1.lower()
        if text_1 == 'no abstract available':
            continue
        count += 1
        text_1 = ' '.join(text_1.split()) # remove redundant while space

        writer.writerow([text_1])
        writer.writerow(['index', 'article_pmid','entity_text','entity_fbid','start_position','end_position'])

        # rule 1: scan the alias that comtaining white space.
        # e.g. T beta h,  Dm Rg3
        save_range = []
        save_alias = []
        for key,value in reverse_data_dict_biogrid.items():
            if ' ' in key:
                if key in text_1:
                    start_position = text_1.find(key)
                    end_position = start_position + len(key)

                    if (not text_1[start_position-1].isalpha()) and (not text_1[end_position].isalpha()):
                        if text_1[start_position:end_position] != key:
                            print('Position Error!')
                            quit()
                        save_range.append(range(start_position, end_position))
                        save_alias.append((key, start_position, end_position))
            else:
                continue

        remove_list = []
        for i in range(len(save_alias)):
            for j in range(i+1,len(save_alias)):
                key_a, start_position_a, end_position_a = save_alias[i]
                key_b, start_position_b, end_position_b = save_alias[j]
                if (start_position_a in range(start_position_b, end_position_b)) and (end_position_a in range(start_position_b, end_position_b)):
                    remove_list.append((key_a, start_position_a, end_position_a))
                elif (start_position_b in range(start_position_a, end_position_a)) and (end_position_b in range(start_position_a, end_position_a)):
                    remove_list.append((key_b, start_position_b, end_position_b))

        remove_list = list(set(remove_list))

        for i in remove_list:
            save_alias.remove(i)

        for tuple_ in save_alias:
            key, start_position, end_position = tuple_
            writer.writerow([count, pmid, key, reverse_data_dict_biogrid[key], start_position, end_position])

        # rule 2: scan the alias that only 1 word.
        # e.g. olfD, sbl, bss
        text_1_split = re.split('\s|/',text_1)
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
                writer.writerow([count, pmid, word,reverse_data_dict_biogrid[word], start_position, end_position])
            start_position = end_position + 1

        writer.writerow([])
        writer.writerow(['-'*20])
        writer.writerow([])
