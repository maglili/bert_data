import pickle
import pandas as pd
import csv
import re
from tqdm import tqdm

# reverse_data_dict_biogrid: combining flybase, bgee, biogrid aliases
with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

print(len(reverse_data_dict_biogrid))
count = 0

for key, value in reverse_data_dict_biogrid.items():
    if 'enhancer' in key:
        print(key)

print('='*20)

for key, value in reverse_data_dict_biogrid.items():
    if value  == 'FBgn0002734':
        print(key)
