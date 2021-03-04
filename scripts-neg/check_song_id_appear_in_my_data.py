import pandas as pd
songs_pmid = pd.read_csv('./Id.csv', encoding='utf-8', index_col=0, squeeze=True)
songs_pmid = songs_pmid.to_list()
print('len of songs_pmid:',len(songs_pmid))

neg_data = pd.read_csv('../csv_data/output_neg_all.csv', encoding='iso-8859-1', header=None, dtype=str)
neg_data = neg_data[1]
neg_data = neg_data.to_list()
print('len of my neg_data:',len(neg_data))

count = 0
for id in songs_pmid:
    if id in neg_data:
        count += 1
print("song's id appear in my neg_data:",count)
