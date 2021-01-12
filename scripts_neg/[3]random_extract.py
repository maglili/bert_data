import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append(r'D:\user\Documents\N26091194\Projects\web_crawler\scripts_pos')
from year_count_pos import year_set #this is a variable

#loading pos and neg data
df = pd.read_csv('../csv_data/output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
pos_df = pd.read_csv('../csv_data/output_pos.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
pos_pmid = pos_df[0].tolist()

# save all data by its published year, balance data to fit pos data
all_set = dict()
for i in range(1985,2022):
    all_set[str(i)] = df[df[4]==str(i)]

# extract data
extract_frames=[] # save extract dataframes
extract_pmid=[] # save extract pmid
for year, appear_times in year_set.items():
    random_seed = 0
    for i in range(appear_times):
        while True:
            extract_data = all_set[year].sample(n=1, random_state = random_seed)
            neg_pmid = extract_data[1].to_numpy().item()
            if neg_pmid in pos_pmid:
                print('Neg_pmid appear in Pos_pmid in year {}!!!'.format(year))
                print(neg_pmid)
                print('-'*10)
                random_seed += 1
                continue
            elif neg_pmid in extract_pmid:
                print('Dublicate in year {}!!!'.format(year))
                print(neg_pmid)
                print('-'*10)
                random_seed += 1
                continue
            else:
                extract_frames.append(extract_data)
                extract_pmid.append(neg_pmid)
                random_seed += 1
                break

print('='*40)
result = pd.concat(extract_frames) #combine dataframes in frames
print(result)
print('='*40)
#result.to_csv('../csv_data/random_extract_remove_redundant.csv', header = False, index = False, encoding = 'utf-8')

#------------------------------examine year distribution----------------------------------------
year_count = result[4].tolist()
year_set_neg = {}

for year in year_count:
    year_set_neg[year]=year_set_neg.get(year,0) + 1

keys = year_set_neg.keys()
x = []
for i in keys:
    num = int(i)
    x.append(num)
    x.sort()
#print(x)

y = []
for i in x:
    st = str(i)
    y.append(year_set_neg[st])
#print(y)

for i in range(len(x)):
    print('Published in',x[i],':',y[i])

# plt.bar(x,y)
# plt.title('Randomly extract data distribution')
# plt.xlabel('year')
# plt.ylabel('count')
# plt.show()
