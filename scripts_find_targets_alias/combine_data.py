import pandas as pd
import pickle

flybase_df  = pd.read_csv('./csv_data/flybase_gene-combine.csv',header=None, encoding='utf-8')
flybase_df = flybase_df.fillna('')
bgee_df = pd.read_csv('./csv_data/bgee_gene-combine.csv',header=None, encoding='utf-8')
bgee_df = bgee_df.fillna('')

flybase_df = flybase_df[[0,3,4]]
print(flybase_df)
print('='*10)
print(bgee_df)
print('='*10)

data_dict = {}
for idx in range(len(flybase_df)):
    fbid, gene_symbol, alias = flybase_df.iloc[idx]
    gene_symbol = gene_symbol.split('\\')[1]
    #print(fbid, gene_symbol, alias)
    if fbid not in data_dict:
        data_dict[fbid] = alias + ', ' + gene_symbol

print(data_dict['FBgn0031081'])
print('='*10)

for idx in range(len(bgee_df)):
    fbid, gene_symbol, alias = bgee_df.iloc[idx]
    if fbid not in data_dict:
        data_dict[fbid] = alias + ', ' + gene_symbol
    else:
        data_dict[fbid] += ', ' + alias + ', ' + gene_symbol

print(data_dict['FBgn0031081'])
print('='*10)
