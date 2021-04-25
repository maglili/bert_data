def rm_sign(alias, reverse_data_dict_biogrid):
    """
    Remove unalpha character.

    input:
        alias(string), reverse_data_dict_biogrid(dict)
    output:
        alias(string), found_frag(bool)
    """
    found_frag = False
    while True:
        continue_frag = False
        if alias in reverse_data_dict_biogrid:
            found_frag = True
            break
        if (alias != '') and (not alias[0].isalpha()) and (not alias[0].isnumeric()):
            alias = alias[1:]
            continue_frag = True
        if (alias != '') and (not alias[-1].isalpha()) and (not alias[-1].isnumeric()):
            alias = alias[:-1]
            continue_frag = True
        if (continue_frag == False) or (alias == ''):
            break
    return alias, found_frag

if __name__ == '__main__':
    import pickle
    import re
    with open('../scripts_find_targets_alias/pickles/reverse_data_dict_biogrid.pickle', 'rb') as handle:
        reverse_data_dict_biogrid = pickle.load(handle)
    alias = 'stg'
    alias, found_frag = rm_sign(alias, reverse_data_dict_biogrid)
    print(alias, found_frag)
