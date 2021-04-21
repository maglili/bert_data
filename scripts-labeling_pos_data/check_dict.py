import pickle

with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

count = 0
for key, value in reverse_data_dict_biogrid.items():
    print(key)
    count += 1

    if count == 100:
        break
