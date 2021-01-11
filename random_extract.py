import pandas as pd
from year_count_pos import year_set #this is a variable
import matplotlib.pyplot as plt

df = pd.read_csv('./csv_data/output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)

all_set = dict() # save all data by its published year
for i in range(1985,2022): # balance data to fit pos data
    all_set[str(i)] = df[df[4]==str(i)]

#loading positive data
pos_df = pd.read_csv('./csv_data/output_pos.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
pos_pmid = pos_df[0].tolist()


d  = {} #save randomly extract data
frames=[] #list to save extract data
for year,times in year_set.items():
    d["y" + year] = all_set[year].sample(n=times, random_state=1)
    frames.append(d["y" + year])
result = pd.concat(frames) #combine dataframes in frames
print(result)
#result.to_csv('random_extract.csv', header = False, index = False, encoding = 'utf-8')

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

plt.bar(x,y)
plt.title('Randomly extract data distribution')
plt.xlabel('year')
plt.ylabel('count')
plt.show()
