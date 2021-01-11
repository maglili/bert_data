"""
print errors
"""
import pickle

with open('./alias_data/gene_list.pkl', 'rb') as a:
    gene_list = pickle.load(a)

with open('./alias_data/aka_list.pkl', 'rb') as b:
    aka_list = pickle.load(b)

with open('./alias_data/error_list.pkl', 'rb') as c:
    error_list = pickle.load(c)

for id in error_list:
    print('id:',id)
