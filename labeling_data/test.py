import pickle
import pandas as pd
import re

# reverse_data_dict_biogrid: combining flybase, bgee, biogrid aliases
with open("../gene_alias/pickles/reverse_data_dict_biogrid.pickle", "rb") as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

# load positive data
df = pd.read_csv(
    "../csv_data/output-pos-remove_no_abst.csv",
    header=None,
    encoding="utf-8",
    dtype=str,
)
df = df[[0, 2]]

# find specific abstract
idx = 91
idx -= 1
start = 723
end = 725
pmid, text = df.iloc[idx]
text = " ".join(text.split())

print("\npmid:", pmid)
# print("\nabst:\n", text)
print()
print("text:", text[start - 5 : end + 5])
print("text:", text[start:end])
