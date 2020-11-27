import pandas as pd
from year_count_pos import year_set #this is a variable
import matplotlib.pyplot as plt

df = pd.read_csv('output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
all_set = dict() # save all data in output_neg_all.csv
for i in range(1985,2022):
    all_set[str(i)] = df[df[4]==str(i)]

#loading positive data
pos_df = pd.read_csv('output_pos.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
pos_df = pos_df[0]
pos_pmid = pos_df.tolist()


d  = {} #save randomly extract data
frames=[] #list to save extract data
for i in year_set:
    d["y" + i] = all_set[i].sample(n=year_set[i], random_state=1)
    frames.append(d["y" + i])
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
