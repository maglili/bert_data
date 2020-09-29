import pandas as pd

df = pd.read_csv('output_neg_all.csv',squeeze=True,header=None,encoding='iso-8859-1',dtype=str)
print(df.head())

all_set = dict()

for i in range(1985,2021):
    all_set[i] = df[df[4]==str(i)]
print(all_set[1985])
