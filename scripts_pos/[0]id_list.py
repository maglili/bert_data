import re
def find_list():
    fh = open('all_crms.gff3')
    id_list = list()
    for i in fh:
        text = re.findall('PMID:[0-9.]+',i)
        str=''.join(text)
        str = re.findall('[0-9.]+',str)
        str=''.join(str)
        str = str.strip()
        if str not in id_list:
            id_list.append(str)

    while True:
        id_list.remove('')
        if '' not in id_list:
            break

    return id_list

if __name__ == '__main__':
    id_list = find_list()
    print('Length of id_list:',len(id_list))
