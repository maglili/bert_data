import re

def findid():
    fh = open('all_crms.gff3')
    ind = list()
    for i in fh:
        text = re.findall('PMID:[0-9.]+',i)
        str=''.join(text)
        str = re.findall('[0-9.]+',str)
        str=''.join(str)
        str = str.strip()
        if str not in ind:
            ind.append(str)

    while True:
        ind.remove('')
        if '' not in ind:
            break
    #print(ind)
    return ind
