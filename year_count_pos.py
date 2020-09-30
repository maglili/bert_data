import matplotlib.pyplot as plt
year_set = {'2012': 38, '2014': 37, '2011': 34, '2016': 18, '2013': 24, '2000': 36, '1993': 25, '1999': 30, '2003': 31, '2009': 32, '2002': 33, '2010': 40, '1990': 17, '1989': 20, '1986': 4, '1991': 22, '1992': 20, '2007': 39, '1995': 31, '2004': 32, '2020': 5, '2015': 35, '2001': 22, '2017': 22, '1994': 26, '2006': 26, '1997': 26, '1988': 8, '2005': 41, '1998': 22, '2008': 38, '2019': 25, '2018': 18, '1996': 19, '1985': 2, '1987': 3}
count = 0
if __name__ == '__main__':
    for key,value in year_set.items():
        count = count + value
    #print('total:',count)

    keys = year_set.keys()
    x = []
    for i in keys:
        num = int(i)
        x.append(num)
        x.sort()
    #print(x)

    y = []
    for i in x:
        st = str(i)
        y.append(year_set[st])
    #print(y)

    for i in range(len(x)):
        print('Published in',x[i],':',y[i])

    plt.bar(x,y)
    plt.show()
