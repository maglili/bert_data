import pandas as pd
import pickle

flybase_df  = pd.read_csv('./csv_data/flybase_gene-combine.csv',header=None, encoding='utf-8')
flybase_df = flybase_df.fillna('')
flybase_df = flybase_df[[0,3,4]]
bgee_df = pd.read_csv('./csv_data/bgee_gene-combine.csv',header=None, encoding='utf-8')
bgee_df = bgee_df.fillna('')

data_dict = {}

# ------------------add flybase_df data to data_dict---------------------
for idx in range(len(flybase_df)):
    fbid, gene_symbol, alias = flybase_df.iloc[idx]
    gene_symbol = gene_symbol.split('\\')[1]
    #print(fbid, gene_symbol, alias)
    if fbid not in data_dict:
        data_dict[fbid] = alias + ', ' + gene_symbol
    else:
        print('error !!! multiple fbid appear.')
# print(data_dict['FBgn0031081'])
# print('='*10)

# ------------------add bgee_df data to data_dict--------------------------
for idx in range(len(bgee_df)):
    fbid, gene_symbol, alias = bgee_df.iloc[idx]
    if fbid not in data_dict:
        data_dict[fbid] = alias + ', ' + gene_symbol
    else:
        data_dict[fbid] += ', ' + alias + ', ' + gene_symbol
# print(data_dict['FBgn0031081'])
# print('='*10)

# -------------------remove redundant alias in data_dict---------------------
for key,value in data_dict.items():
    value = value.split(', ')
    value = list(set(value))
    if '' in value:
        value.remove('')
    data_dict[key] = value
# print(data_dict['FBgn0031081'])
# print('='*10)

# --------------------building reverse_data_dict-------------------------------
reverse_data_dict = {}
muti_count = 0
remove_key_list = []
for key,value in data_dict.items():
    for alias in value:
        if alias not in reverse_data_dict:
            reverse_data_dict[alias] = key
        else:
            muti_count += 1
            # print('error! alias already exist!',muti_count)
            # print()
            # print('alias:',alias)
            # print()
            # print('fbid:',key)
            # print('data:',data_dict[key])
            # print()
            # print('same alias fbid:',reverse_data_dict[alias])
            # print('same alias data:',data_dict[reverse_data_dict[alias]])
            # print('='*20)
            remove_key_list.append(alias)

remove_key_list = list(set(remove_key_list))
print('redudant alias:',len(remove_key_list))
for alias in remove_key_list:
    reverse_data_dict.pop(alias, None)

count = 0
for key, value in reverse_data_dict.items():
    count +=1
    print(' count {:8}:   {:45}      {:10}'.format(count,key,value))

with open('reverse_data_dict.pickle', 'wb') as handle:
    pickle.dump(reverse_data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
