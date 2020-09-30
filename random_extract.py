import pandas as pd
from year_count_pos import year_set
import matplotlib.pyplot as plt

df = pd.read_csv('output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
all_set = dict()

for i in range(1985,2022):
    all_set[str(i)] = df[df[4]==str(i)]

d  = {}
frames=[]

for i in year_set:
    d["y" + i] = all_set[i].sample(n=year_set[i])
    frames.append(d["y" + i])

result = pd.concat(frames)

result.to_csv('random_extract.csv', header = False, index = False, encoding = 'utf-8')

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
plt.show()
