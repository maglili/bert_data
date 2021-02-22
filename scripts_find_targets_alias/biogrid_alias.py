import pandas as pd
from tqdm import tqdm
import csv
import pickle

df = pd.read_csv('BIOGRID-ORGANISM-Drosophila_melanogaster-4.2.193.tab2.txt',sep='\t')
df = df[['Official Symbol Interactor A','Official Symbol Interactor B', 'Synonyms Interactor A', 'Synonyms Interactor B']]

symbol_and_its_alias = {}

for i in range(len(df)):
    Symbol_A = df.iloc[i]['Official Symbol Interactor A']
    Synonyms_A = df.iloc[i]['Synonyms Interactor A'].split('|')
    Synonyms_A = '\t'.join(Synonyms_A)
    Symbol_B = df.iloc[i]['Official Symbol Interactor B']
    Synonyms_B = df.iloc[i]['Synonyms Interactor B'].split('|')
    Synonyms_B = '\t'.join(Synonyms_B)

    if Symbol_A not in symbol_and_its_alias:
        symbol_and_its_alias[Symbol_A] = Synonyms_A
    elif Synonyms_A not in symbol_and_its_alias[Symbol_A]:
        print('Symbol:',Symbol_A)
        print('symbol_and_its_alias:',symbol_and_its_alias[Symbol_A])
        print('different alias:',Synonyms_A)
        symbol_and_its_alias[Symbol_A] += '\t' + Synonyms_A
        print('combine:', symbol_and_its_alias[Symbol_A])
        print('='*20)

    if Symbol_B not in symbol_and_its_alias:
        symbol_and_its_alias[Symbol_B] = Synonyms_B
    elif Synonyms_B not in symbol_and_its_alias[Symbol_B]:
        print('Symbol:',Symbol_B)
        print('symbol_and_its_alias:',symbol_and_its_alias[Symbol_B])
        print('different alias:',Synonyms_B)
        symbol_and_its_alias[Symbol_B] += '\t' + Synonyms_B
        print('combine:', symbol_and_its_alias[Symbol_B])
        print('='*20)

for key, value in symbol_and_its_alias.items():
    value = value.split('\t')
    if '-' in value:
        print('remove "-"')
        value.remove('-')
    symbol_and_its_alias[key] = value

# with open('biogrid_symbol_ad_its_alias.pickle', 'wb') as handle:
#     pickle.dump(symbol_and_its_alias, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('biogrid_symbol_and_its_alias.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Symbol', 'Alias'])

    for key, value in symbol_and_its_alias.items():
        alias_string = ', '.join(value)
        writer.writerow([key, alias_string])
