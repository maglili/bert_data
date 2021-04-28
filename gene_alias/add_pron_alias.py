"""
Add pron in dict.
"""
import pickle
from greek2pron import greek2pron

with open("./pickles/reverse_data_dict_biogrid.pickle", "rb") as handle:
    reverse_data_dict_biogrid = pickle.load(handle)

ori_len = len(reverse_data_dict_biogrid)

# ---------------------change greek to pronunciation--------------------------
pron_alias = {}
for alias, fbid in reverse_data_dict_biogrid.items():
    changing_alias = greek2pron(alias)
    if alias != changing_alias:
        # print('before:',alias)
        # print('after:',changing_alias)
        # print('='*10)
        pron_alias[changing_alias] = fbid

print()
# ---------------------------add pronunciation alias ------------------------
for alias, fbid in pron_alias.items():
    if alias not in reverse_data_dict_biogrid:
        reverse_data_dict_biogrid[alias] = fbid
        # print('Add {} | fbid:{}'.format(alias,fbid))
    else:
        if reverse_data_dict_biogrid[alias] != fbid:
            print()
            print("*" * 50)
            print("FBid error")
            print("alias:", alias)
            print("fbid:", fbid)
            print("reverse_data_dict_biogrid[alias]", reverse_data_dict_biogrid[alias])
            print("*" * 50)
            print()
            reverse_data_dict_biogrid.pop(alias, None)

aft_len = len(reverse_data_dict_biogrid)

print("len before:", ori_len)
print("len after:", aft_len)
print("add aliases:", aft_len - ori_len)

# --------------------save to picke-------------------------------
with open("./pickles/reverse_data_dict_biogrid.pickle", "wb") as handle:
    pickle.dump(reverse_data_dict_biogrid, handle, protocol=pickle.HIGHEST_PROTOCOL)
