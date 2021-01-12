import re

def find_target():
    """
    Finding targets from "all_crms.gff3" by regular expression.

    return: target_list
    """
    fh = open('./positive_data/all_crms.gff3')
    target_list = {}
    for i in fh:
        text = re.findall('target=FB:[0-9a-zA-Z_-]+:[0-9a-zA-Z_-]+',i)
        if text == []:
            continue
        text = ''.join(text)
        text = text.split(':')
        id = text[1]
        alias = text[2]
        if id not in target_list:
            target_list[id] = alias
    return target_list

target_list = find_target()

if __name__ == '__main__':
    print('Length of target_list:',len(target_list))

    for i,j in target_list.items():
        print(i,j)
