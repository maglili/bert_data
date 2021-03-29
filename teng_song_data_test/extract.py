import pandas as pd
import pickle
from tqdm import tqdm
import matplotlib.pyplot as plt
import sys
sys.path.append(r'../scripts_pos')

def check_year_distr(pos_year_list: list) -> dict:
    """
    return a dictionary.

    key: years
    values: year count
    """
    pos_year_dict = {}
    for year in pos_year_list:
        year = str(year)
        if year not in pos_year_dict:
            pos_year_dict[year] = 1
        else:
            pos_year_dict[year] += 1
    return pos_year_dict

# pos data
pos_df = pd.read_csv('../csv_data/output-pos-remove_no_abst.csv', squeeze=True, header=None, encoding='iso-8859-1', dtype=str)
pos_df = pos_df.fillna('')
pos_pmid = pos_df[0].tolist()

# neg data
with open('./st_del_pos_blank.pkl','rb') as f:
    df = pickle.load(f)
print('Original:')
print(df)
print('='*10)

# pos year distribution
pos_year_list = pos_df[4].to_list()
pos_year_dict = check_year_distr(pos_year_list)

# save all data by its published year, balance data to fit pos data
all_set = dict()
for i in range(1985,2021):
    all_set[str(i)] = df[df['year']==i]

# extract data
extract_pmid = []
extract_result = {}
for i in range(6):#<----------------------------------- modify
    extract_frames = []
    for year, appear_times in pos_year_dict.items():
        random_seed = 0
        extract_count = 0
        while True:
            extract_data = all_set[year].sample(n=1, random_state = random_seed)
            neg_pmid = extract_data['Id'].item()
            abst = extract_data['abst'].item()

            # safety trigger
            if abst == '':
                print('ERROR!')
                quit()

            # data not been extract
            if neg_pmid not in extract_pmid:
                extract_frames.append(extract_data)
                extract_pmid.append(neg_pmid)
                extract_count += 1

            # data have been extract
            else:
                random_seed += 1

            # extract enough data
            if extract_count == appear_times:
                break

    result = pd.concat(extract_frames) #combine dataframes in frames
    print(result)
    extract_result['data'+str(i)] = result
    filename='neg_set'+str(i)+'.csv'
    result.to_csv('./'+filename, header = False, index = False, encoding = 'utf-8')
    print(result[result['year']==2020])
    print('='*60)

#print(extract_result)
#examine results
for dataframe in extract_result.values():
    years = dataframe['year'].to_list()
    test_pos_year_dict = check_year_distr(years)
    print('Pos distribution == Neg distribution:',pos_year_dict == test_pos_year_dict)
    print('='*50)

# ----------------------examine redundant--------------------------------------
pmid_set = []
for idx, dataframe in extract_result.items():
    pmid = dataframe['Id'].to_list()
    pmid_set.append(pmid)

redundant = 0
for i in range(6): #<----------------------------------- modify
    for j in range(i+1,6): #<----------------------------------- modify
        for pmid in pmid_set[i]:
            if pmid in pmid_set[j]:
                print('redundant')
                print(i)
                print(pmid)
                print(j)
                print('='*20)
                redunat += 1
if redundant == 0:
    print('No redundant!')
