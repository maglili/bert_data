import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append(r'../scripts_pos')

def check_year_distr(year_list: list) -> dict:
    """
    return a dictionary
    key: years
    values: year count
    """
    year_set = {}
    for year in year_list:
        if year not in year_set:
            year_set[year] = 1
        else:
            year_set[year] += 1
    return year_set

# pos data
pos_df = pd.read_csv('../csv_data/output-pos-remove_no_abst.csv', squeeze=True, header=None, encoding='iso-8859-1', dtype=str)
pos_df = pos_df.fillna('')
pos_pmid = pos_df[0].tolist()

# neg data
df = pd.read_csv('../csv_data/output_neg_all.csv', squeeze=True, header=None, encoding='iso-8859-1', dtype=str)
df = df.fillna('')
count = 0
remove_list = []
for i in range(len(df)):
    pmid = df.iloc[i][1]
    abst = df.iloc[i][3]
    if pmid in pos_pmid:
        count += 1
        remove_list.append(i)
    if abst == 'No abstract available':
        count += 1
        remove_list.append(i)
df = df.drop(remove_list)

# pos year distribution
year_list = pos_df[4].to_list()
year_set = check_year_distr(year_list)

# save all data by its published year, balance data to fit pos data
all_set = dict()
for i in range(1985,2021):
    all_set[str(i)] = df[df[4]==str(i)]

# extract data
extract_pmid = []
extract_result = {}
for i in range(5):
    extract_frames = []
    for year, appear_times in year_set.items():
        random_seed = 0
        extract_count = 0
        while True:
            extract_data = all_set[year].sample(n=1, random_state = random_seed)
            neg_pmid = extract_data[1].item()
            abst = extract_data[3].item()
            if abst == '':
                print('ERROR!')
                quit()
            if neg_pmid not in extract_pmid:
                extract_frames.append(extract_data)
                extract_pmid.append(neg_pmid)
                extract_count += 1
            else:
                random_seed += 1
            if extract_count == appear_times:
                break
    result = pd.concat(extract_frames) #combine dataframes in frames
    print(result)
    extract_result['data'+str(i)] = result
    filename='neg_set'+str(i)+'.csv'
    result.to_csv('../csv_data/neg_set/'+filename, header = False, index = False, encoding = 'utf-8')
    print('='*60)

#examine results
for dataframe in extract_result.values():
    years = dataframe[4].to_list()
    test_year_set = check_year_distr(years)
    print(year_set == test_year_set)
    print('='*50)
    year_count = result[4].tolist()
    year_set_neg = {}

    # # plot year distribution
    # for year in year_count:
    #     year_set_neg[year]=year_set_neg.get(year,0) + 1
    #
    # keys = year_set_neg.keys()
    # x = []
    # for i in keys:
    #     num = int(i)
    #     x.append(num)
    #     x.sort()
    # print(x)
    #
    # y = []
    # for i in x:
    #     st = str(i)
    #     y.append(year_set_neg[st])
    # print(y)
    #
    # for i in range(len(x)):
    #     print('Published in',x[i],':',y[i])
    #
    # plt.bar(x,y)
    # plt.title('Randomly extract data distribution')
    # plt.xlabel('year')
    # plt.ylabel('count')
    # plt.show()

#examine redundant
pmid_set = []
for idx,dataframe in extract_result.items():
    pmid = dataframe[1].to_list()
    pmid_set.append(pmid)

redundant = 0
for i in range(5):
    for j in range(i+1,5):
        for k in pmid_set[i]:
            if k in pmid_set[j]:
                print('redundant')
                print(i)
                print(k)
                print(j)
                print('='*20)
                redunat += 1

if redundant == 0:
    print('No redundant!')
