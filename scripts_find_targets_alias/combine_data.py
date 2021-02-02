import pandas as pd
import pickle

flybase_df  = pd.read_csv('./csv_data/flybase_gene-combine.csv',header=None, encoding='utf-8')
flybase_df = flybase_df.fillna('')
bgee_df = pd.read_csv('./csv_data/bgee_gene-combine.csv',header=None, encoding='utf-8')
bgee_df = bgee_df.fillna('')


with open('./pickles/gene_data.pickle', 'rb') as handle:
    gene_data = pickle.load(handle)

# flybase_dict = {}
# for i in range(len(flybase_df)):
#     fbid = flybase_df.iloc[i][0]
#     symbol = flybase_df.iloc[i][3].split('\\')[1]
#     alias = flybase_df.iloc[i][4]
#     data = {'symbol':symbol,'alias':alias}
#     flybase_dict[fbid] = data
#print(flybase_dict)
# with open('./pickles/flybase_dict.pickle', 'wb') as handle:
#     pickle.dump(flybase_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('./pickles/flybase_dict.pickle', 'rb') as handle:
    flybase_dict = pickle.load(handle)

# bgee_dict = {}
# for i in range(len(bgee_df)):
#     fbid = bgee_df.iloc[i][0]
#     gbee_symbol = bgee_df.iloc[i][1]
#     gbee_alias = bgee_df.iloc[i][2]
#     data = {'symbol':gbee_symbol,'alias':gbee_alias}
#     bgee_dict[fbid] = data
# with open('./pickles/bgee_dict.pickle', 'wb') as handle:
#     pickle.dump(bgee_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('./pickles/bgee_dict.pickle', 'rb') as handle:
    bgee_dict = pickle.load(handle)
#print(bgee_dict)

combie_dict = {}
for fbid in gene_data.keys():
    fb_status = False
    bgee_status = False
    if fbid in flybase_dict:
        flybase_data = flybase_dict[fbid]
        fb_symbol = flybase_data['symbol']
        fb_alias = flybase_data['alias']
        fb_status = True
    if fbid in bgee_dict:
        bgee_data = bgee_dict[fbid]
        bgee_symbol = bgee_data['symbol']
        bgee_alias = bgee_data['alias']
        bgee_status = True

    if fb_status == bgee_status == False:
        continue
    elif fb_status == bgee_status == True:
        if fb_alias != '':
            data = fb_alias+', '+bgee_alias
            data = data.split(', ')
            data = set(data)
            data = list(data)
            data = ', '.join(data)
            combie_dict[fb_symbol] = data
        else:
            combie_dict[fb_symbol] = bgee_alias
        if bgee_symbol not in combie_dict[fb_symbol]:
            combie_dict[fb_symbol] += ', '+ bgee_symbol
    elif fb_status == True:
        combie_dict[fb_symbol] = fb_alias
    elif bgee_status == True:
        combie_dict[bgee_symbol] = bgee_alias

with open('./pickles/combie_dict.pickle', 'wb') as handle:
    pickle.dump(combie_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
for key, value in combie_dict.items():
    print('{:<10} : {}'.format(key,value))
