import pickle
import re

with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

count = 0
for key, value in reverse_data_dict_biogrid.items():
    print(key)
    count += 1

    if count == 100:
        break

# text_1 = 'mirror-image 123123/456465-54654,4456\\12'
# text_1_split = re.split(r'\s|/|,|-|\\', text_1)
#
# print('text_1:',text_1)
# print('text_1_split:',text_1_split)
