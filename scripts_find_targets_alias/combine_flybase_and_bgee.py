import pandas as pd
import pickle

flybase_df  = pd.read_csv('./csv_data/flybase_gene-combine.csv',header=None, encoding='utf-8')
flybase_df = flybase_df.fillna('')

bgee_df = pd.read_csv('./csv_data/bgee_gene-combine.csv',header=None, encoding='utf-8')
bgee_df = bgee_df.fillna('')

data_dict = {}

# ------------------add flybase_df data to data_dict---------------------
for idx in range(len(flybase_df)):
    fbid, name, annotation, gene_symbol, alias = flybase_df.iloc[idx]
    gene_symbol = gene_symbol.split('\\')[1]
    if fbid not in data_dict:
        data_dict[fbid] = fbid + ', ' + name + ', ' + annotation + ', ' + gene_symbol + ', ' + alias
    else:
        print('error !!! multiple fbid appear.')

# ------------------add bgee_df data to data_dict--------------------------
for idx in range(len(bgee_df)):
    fbid, gene_symbol, alias = bgee_df.iloc[idx]
    if fbid not in data_dict:
        data_dict[fbid] = fbid + ', ' + gene_symbol + ', ' + alias
    else:
        data_dict[fbid] += ', ' + gene_symbol + ', ' + alias

# -------------------remove redundant alias in data_dict---------------------
for key,value in data_dict.items():
    value = value.lower()
    value = value.split(', ')
    value = list(set(value))
    if '' in value:
        value.remove('')
    data_dict[key] = value

# --------------------building reverse_data_dict-------------------------------
reverse_data_dict = {}
remove_key_list = [] # remove alias that appear in different gene
for key,value in data_dict.items():
    for alias in value:
        if alias not in reverse_data_dict:
            reverse_data_dict[alias] = key
        else:
            # print('Error {}! {} already exist!'.format(muti_count, alias))
            # print()
            # print('Present fbid:',key)
            # print('Present data:',data_dict[key])
            # print()
            # print('Existing alias fbid:',reverse_data_dict[alias])
            # print('Existing alias data:',data_dict[reverse_data_dict[alias]])
            # print('='*20)
            remove_key_list.append(alias)

# --------------------remove alias from inverse dict------------------------------
remove_key_list = list(set(remove_key_list))
print('len of redudant alias:',len(remove_key_list))
for alias in remove_key_list:
    reverse_data_dict.pop(alias, None)

print('len of reverse_data_dict:',len(reverse_data_dict))

# --------------------save to picke-------------------------------
with open('./pickles/reverse_data_dict.pickle', 'wb') as handle:
    pickle.dump(reverse_data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
