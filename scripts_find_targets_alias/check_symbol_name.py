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

count = 0
for i in range(len(flybase_df)):
    fbid_fb, gene_symbol_fb, alias_fb = flybase_df.iloc[i]
    try:
        fbid_bg = bgee_df[bgee_df[0] == fbid_fb][0].item()
        gene_symbol_bg = bgee_df[bgee_df[0] == fbid_fb][1].item()
        alias_bg = bgee_df[bgee_df[0] == fbid_fb][2].item()
    except:
        print(fbid_fb, 'not in bgee_df!')
        continue
    gene_symbol_fb = gene_symbol_fb.split('\\')[1]
    if gene_symbol_fb != gene_symbol_bg:
        count += 1
        print('count',count,'---','fbid:',fbid_fb,'---',gene_symbol_fb,'vs',gene_symbol_bg)
