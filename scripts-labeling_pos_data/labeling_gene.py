import pickle
import pandas as pd

with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

df = pd.read_csv('../csv_data/output_pos.csv', header=None, encoding='utf-8')
df = df[[0,2]]

pmid, text_1 = df.iloc[0]
print(text_1)
print()

for key,value in reverse_data_dict_biogrid.items():
    if ' ' in key:
        if key in text_1:
            start_position = text_1.find(key)
            end_position = start_position + len(key)
            print('article_pmid:',pmid)
            print('entity_text:',key)
            print('entity_fbid:',reverse_data_dict_biogrid[key])
            print('start_position:',start_position)
            print('end_position:',end_position)
            if text_1[start_position:end_position] != key:
                print('Position Error!')
                quit()
            print('-'*20)
    else:
        continue

text_1_split = text_1.split()
start_position = 0
end_position = 0
for word in text_1_split:
    end_position = start_position + len(word)
    if word in reverse_data_dict_biogrid:
        print('article_pmid:',pmid)
        print('entity_text:',word)
        print('entity_fbid:',reverse_data_dict_biogrid[word])
        print('start_position:',start_position)
        print('end_position:',end_position)
        if text_1[start_position:end_position] != word:
            print('Position Error!')
            quit()
        print('-'*20)
    start_position = end_position + 1

print()
# for key,value in reverse_data_dict_biogrid.items():
#     if ' ' in key:
#         print('{:25}   {:25}'.format(key,value))
