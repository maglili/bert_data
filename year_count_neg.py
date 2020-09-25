import pandas as pd
import csv

df = pd.read_csv('output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
df = df[4]
df = df.tolist()
print(df[0])
print(type(df[0]))

for index,value in enumerate(df):
    if type(value) != str:
        print(index+1)
        

print('length of df:',len(df))
'''
year_set = dict()

for i in df:
    year_set[i] = year_set.get(i,0)+1

count = 0
for key,value in year_set.items():
    count = count + value
#print(count)

keys = year_set.keys()
x = []
for i in keys:
    num = int(i)
    x.append(num)
    x.sort()
#print(x)

y = []
for i in x:
    st = str(i)
    y.append(year_set[st])
#print(y)

for i in range(len(x)):
    print('Published in',x[i],':',y[i])

plt.bar(x,y)
plt.show()
'''
