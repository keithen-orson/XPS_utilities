from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''Takes a folder path, scans all of the trimmed xps data (.txt files containing only columns of data and starting with
the word copy), plots them in terms of binding energy for an Al kalpha source, and then saves the plots in the folder 
that the data came from

also saves all the xy data to a .csv file that can easily be read into a pandas dataframe for later processing
'''

mypath = input("input folder path: ")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyfiles:
    if ('.txt') not in i:
        onlyfiles.remove(i)
onlyfiles.sort(key=lambda x: x.split('-')[5])
onlyfiles.sort(key=lambda x: len(x))
print(onlyfiles)
data = pd.DataFrame()

for i in onlyfiles:
    if ("copy" in i) and (".txt" in i):
        pass
    else:
        continue
    filepath = mypath + '/' + i
    f = open(filepath)
    file_contents = f.readlines()
    f.close()
    xy = np.zeros((2, len(file_contents)))
    for j in range(len(file_contents)):
        linedata = file_contents[j].split()
        xy[0, j] = 1486.7-float(linedata[0])
        xy[1, j] = float(linedata[1])

    scannum = i.split('-')[5]
    scannum = scannum.split('_')[0]
    leftbinding = max(xy[0,:])
    rightbinding = min(xy[0,:])
    fig, ax = plt.subplots()
    ax.plot(xy[0, :], xy[1, :])
    plt.xlabel('Kinetic energy (eV)')
    plt.xlim((max(xy[0,:]), min(xy[0,:])))
    plt.title(i)
    plt.savefig(mypath+'/'+i[:-4]+'.png')
    plt.show()

    current = pd.DataFrame()
    for j, val in enumerate(xy[0,:]):
        current = current.append([{('bindingE ' + scannum): xy[0,j],
                             ('intensity ' + scannum): xy[1,j]
                             },])
    current = current.reset_index()

    print(current.head())
    current = current.drop(['index'], axis=1)
    data = pd.concat([data, current], axis=1, ignore_index=False)


print(data.head())
data.to_csv(mypath+'/'+'data.csv')






