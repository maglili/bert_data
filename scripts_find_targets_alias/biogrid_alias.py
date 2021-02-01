import pandas as pd
from tqdm import tqdm
import csv
import pickle

df = pd.read_csv('BIOGRID-ORGANISM-Drosophila_melanogaster-4.2.193.tab2.txt',sep='\t')
df = df[['Official Symbol Interactor A','Official Symbol Interactor B', 'Synonyms Interactor A', 'Synonyms Interactor B']]

symbol_and_its_alias = {}

for i in tqdm(range(len(df))):
    Symbol_A = df.iloc[i]['Official Symbol Interactor A']
    Synonyms_A = df.iloc[i]['Synonyms Interactor A'].split('|')
    Symbol_B = df.iloc[i]['Official Symbol Interactor B']
    Synonyms_B = df.iloc[i]['Synonyms Interactor B'].split('|')

    if Symbol_A not in symbol_and_its_alias:
        symbol_and_its_alias[Symbol_A] = Synonyms_A

    if Symbol_B not in symbol_and_its_alias:
        symbol_and_its_alias[Symbol_B] = Synonyms_B

with open('biogrid_symbol_ad_its_alias.pickle', 'wb') as handle:
    pickle.dump(symbol_and_its_alias, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('biogrid_symbol_ad_its_alias.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Symbol', 'Alias'])

    for key, value in symbol_and_its_alias.items():
        if value == ['-']:
            writer.writerow([key])
        else:
            alias_string = ', '.join(value)
            writer.writerow([key, alias_string])
