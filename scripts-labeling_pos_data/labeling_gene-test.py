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

# Open positive data (target)
df = pd.read_csv('../csv_data/output-pos-remove_no_abst.csv', header=None, encoding='utf-8')
df = df[[0,2]]

# writing the output file
with open('labeling.tsv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')

    count = 0 # counter
    for idx in tqdm(range(len(df))):
        count+=1
        pmid, text = df.iloc[idx]
        text = text.lower()
        text = ' '.join(text.split()) # remove redundant while space

        # write to csv
        writer.writerow([text])
        writer.writerow(['index', 'article_pmid','entity_text','entity_fbid','start_position','end_position', 'manual_label'])

        # rule 1: scan the alias that comtaining white space
        # e.g. T beta h,  Dm Rg3

        found_alias = [] # save founded alias

        # Find alias that containing whike space, e.g. T beta h,  Dm Rg3
        for key, value in reverse_data_dict_biogrid.items():

            if (' ' in key):
                if key in text:
                    found_alias.append(key)
            else:
                continue

        # rule 2: scan the alias that only 1 word
        # e.g. olfD, sbl, bss
        text_split = re.split(r'\s|/', text)
        text_split = list(set(text_split))
        if '' in text_split:
            text_split.remove('')

        # Processing alias.
        # e.g. su(H), -> su(H)
        for alias in text_split:
            if len(alias)>1:
                if alias not in reverse_data_dict_biogrid:
                    if (not alias[0].isalpha()) and (not alias[0].isnumeric()):
                        alias = alias[1:]
                    if (not alias[-1].isalpha()) and (not alias[-1].isnumeric()):
                        alias = alias[:-1]
                    if alias in reverse_data_dict_biogrid:
                        found_alias.append(alias)
                else:
                    found_alias.append(alias)

        # use regular expression to find position
        found_alias = list(set(found_alias))
        save_range = [] # save alias Position
        for alias in found_alias:
            alias = re.escape(alias)
            pos = [(m.start(0), m.end(0)) for m in re.finditer(alias, text)]
            save_range.extend(pos)
        save_range.sort()

        # remove redundant alias (alias that smaller than another one)
        remove_list = []
        print('type(save_range):',type(save_range))
        print('len(save_range):',len(save_range))
        for i in range(len(save_range)):
            for j in range(i+1,len(save_range)):
                if (save_range[i][0] >= save_range[j][0]) and (save_range[i][1] <= save_range[j][1]):
                    remove_list.append(save_range[i])
                if (save_range[j][0] >= save_range[i][0]) and (save_range[j][1] <= save_range[i][1]):
                    remove_list.append(save_range[j])
        remove_list = list(set(remove_list))
        for pos in remove_list:
            save_range.remove(pos)

        # remove wrong alias
        # e.g. The paper show that ... -> how
        remove_list = []
        for range in save_range:
            if (range[0] > 0) and (range[1] < len(text)):
                if (text[range[0]-1].isalpha()) or (text[range[1]].isalpha()):
                    remove_list.append(range)
        remove_list = list(set(remove_list))
        for pos in remove_list:
            save_range.remove(pos)

        # write to csv
        for start, end in save_range:
            word = text[start:end]
            writer.writerow([count, pmid, word, reverse_data_dict_biogrid[word], start, end])

        writer.writerow([])
        writer.writerow(['-'*20])
        writer.writerow([])

        if count == 3:
            break
