import pandas as pd
import pickle
from tqdm import tqdm

# ---------------load reverse_data_dict that contain flybase and bgee information--------------------
with open('./pickles/reverse_data_dict.pickle', 'rb') as handle:
    reverse_data_dict = pickle.load(handle)
ori_reverse_data_dict = len(reverse_data_dict)

# ------------------------------load biogrid data-----------------------------------------------------
biogrid_df  = pd.read_csv('./csv_data/biogrid_symbol_and_its_alias.csv', encoding='utf-8')
biogrid_df = biogrid_df.fillna('')

# -----------alias_list: list containing small list combine with alias + symbol----------------------
alias_list = []
for idx in range(len(biogrid_df)):
    symbol, aliases = biogrid_df.iloc[idx]
    aliases = symbol + ', ' +  aliases
    aliases = aliases.split(', ')
    while True:
        if '' in aliases:
            aliases.remove('')
            print('***remove ""***')
        else:
            break
    alias_list.append(aliases)

# -------------------remove alias that appear in different gene--------------------------------
remove_list = []
for i in tqdm(range(len(alias_list))):
    for j in range(i+1,len(alias_list)):
        list_1 = alias_list[i]
        list_2 = alias_list[j]
        for alias in list_1:
            if alias in list_2:
                remove_list.append(alias)

# ------------------remove alias base on remove_list-----------------------------------------------
remove_list = list(set(remove_list))
for alias in remove_list:
    for idx in range(len(alias_list)):
        if alias in alias_list[idx]:
            alias_list[idx].remove(alias)

# -----------------save and load alias_list-----------------------------------------------------------
with open('./pickles/alias_list.pickle', 'wb') as handle:
    pickle.dump(alias_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('./pickles/alias_list.pickle', 'rb') as handle:
    alias_list = pickle.load(handle)

# --------------------------------combine data-------------------------------------------------------
count = 0
different_alias_count = 0
alias_not_found = []
for idx in range(len(alias_list)):
    aliases = alias_list[idx]
    add_frag = False
    fbid_list = []
    for alias in aliases:
        if alias in reverse_data_dict:
            fbid_list.append(reverse_data_dict[alias])
    fbid_list_copy = fbid_list.copy()
    fbid_list = list(set(fbid_list))
    if len(fbid_list) == 1:
        add_frag = True
        fbid = fbid_list[0]
    elif len(fbid_list) == 0:
        count += 1
        alias_not_found.append(alias)
        #print('{:20} not found! {}'.format(alias,count))
        #print('='*20)
    else:
        different_alias_count += 1
        print('',)
        print('different_alias_count',different_alias_count)
        print('aliases',aliases)
        print('fbid_list',fbid_list)
        print('fbid_list_copy alias:',fbid_list_copy)
        print('='*20)
    if add_frag:
        for alias in aliases:
            if alias not in reverse_data_dict:
                reverse_data_dict[alias] = fbid
                #print(alias ,reverse_data_dict[alias])

print('alias_not_found:',len(alias_not_found))
print('original reverse_data_dict:',ori_reverse_data_dict)
print('new reverse_data_dict:',len(reverse_data_dict))
print('add alias:',len(reverse_data_dict) - ori_reverse_data_dict)

reverse_data_dict_biogrid = reverse_data_dict

# ------------------save and load reverse_data_dict_biogrid--------------------------------------
with open('./pickles/reverse_data_dict_biogrid.pickle', 'wb') as handle:
    pickle.dump(reverse_data_dict_biogrid, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('./pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)
