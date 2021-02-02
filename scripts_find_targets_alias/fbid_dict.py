from tqdm import tqdm
import pickle

# with open('dmel-all-r6.24.gtf','r') as fh:
#     gene_data = dict()
#     for row in tqdm(fh):
#         row = row.split()
#         fbid = row[9][1:-2]
#         symbol = row[11][1:-2]
#         if fbid not in gene_data:
#             gene_data[fbid] = symbol
#
# with open('gene_data.pickle', 'wb') as handle:
#     pickle.dump(gene_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./pickles/gene_data.pickle', 'rb') as handle:
    gene_data = pickle.load(handle)

print(len(gene_data.keys()))
