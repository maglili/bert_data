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
        pmid, text = df.iloc[idx]
        text = text.lower()
        # if text == 'no abstract available':
        #     continue
        count += 1
        text = ' '.join(text.split()) # remove redundant while space

        writer.writerow([text])
        writer.writerow(['index', 'article_pmid','entity_text','entity_fbid','start_position','end_position', ',manual_label'])

        # rule 1: scan the alias that comtaining white space =========================================================
        # e.g. T beta h,  Dm Rg3
        save_range = [] # save range: (start_position, end_position)
        save_alias = [] # save alias info: (key, start_position, end_position)

        for key, value in reverse_data_dict_biogrid.items():
            # alias that containing whike space, e.g. T beta h,  Dm Rg3
            if (' ' in key):
                if key in text:
                    start_position = text.find(key)
                    end_position = start_position + len(key)

                    # Guarantee we won't find wrong alias
                    # e.g. ... gene belongs ... -> find: gene b
                    if (not text[start_position-1].isalpha()) and (not text[end_position].isalpha()):
                        # safety trigger
                        if text[start_position:end_position] != key:
                            print('Position Error!')
                            quit()

                        save_range.append(range(start_position, end_position))
                        save_alias.append((key, start_position, end_position))
            else:
                continue

        remove_list = [] # save tuple that need to delete
        # find redundant alias
        for i in range(len(save_alias)):
            for j in range(i+1,len(save_alias)):
                key_a, start_position_a, end_position_a = save_alias[i]
                key_b, start_position_b, end_position_b = save_alias[j]
                if (start_position_a in range(start_position_b, end_position_b)) and (end_position_a in range(start_position_b, end_position_b)):
                    remove_list.append((key_a, start_position_a, end_position_a))
                elif (start_position_b in range(start_position_a, end_position_a)) and (end_position_b in range(start_position_a, end_position_a)):
                    remove_list.append((key_b, start_position_b, end_position_b))

        # remove info from save_alias
        remove_list = list(set(remove_list))
        for i in remove_list:
            save_alias.remove(i)

        # write infomation to tsv file
        for tuple_ in save_alias:
            key, start_position, end_position = tuple_
            writer.writerow([count, pmid, key, reverse_data_dict_biogrid[key], start_position, end_position])

        # rule 2: scan the alias that only 1 word ============================================================
        # e.g. olfD, sbl, bss
        text_split = re.split(r'\s|/|,|\\', text) #<-------------add "-"
        start_position = 0
        end_position = 0
        for word in text_split:
            add_2 = False # frag that indicate start_position = end_position + 2
            skip_frag = False
            end_position = start_position + len(word)
            for range_ in save_range:
                if start_position in range_: # Guarantee alias won't be add redundantly
                    skip_frag = True
                    continue
            if len(word) > 1:
                if (not word[0].isalpha()) and (not word[0].isnumeric()):
                    word = word[1:]
                    start_position += 1
                if (not word[-1].isalpha()) and (not word[-1].isnumeric()):
                    word = word[:-1]
                    end_position -= 1
                    add_2 = True

            if (word in reverse_data_dict_biogrid) and (skip_frag == False):
                # safety trigger
                if text[start_position:end_position] != word:
                    print('Position Error!')
                    print('word:',word)
                    print('text[start_position:end_position]:',text[start_position:end_position])
                    quit()
                writer.writerow([count, pmid, word,reverse_data_dict_biogrid[word], start_position, end_position])
            if not add_2:
                start_position = end_position + 1
            else:
                start_position = end_position + 2

        writer.writerow([])
        writer.writerow(['-'*20])
        writer.writerow([])
