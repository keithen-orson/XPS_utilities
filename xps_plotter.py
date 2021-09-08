from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np

'''Takes a folder path, scans all of the trimmed xps data (.txt files containing only columns of data and starting with
the word copy), plots them in terms of binding energy for an Al kalpha source, and then saves the plots in the folder 
that the data came from'''

mypath = input("input folder path: ")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles:

    if ("copy" in i) and (".txt" in i):
        pass
    else:
        continue
    filepath = mypath + '/' + i
    print(filepath)
    f = open(filepath)
    file_contents = f.readlines()
    f.close()
    xy = np.zeros((2, len(file_contents)))
    for j in range(len(file_contents)):
        linedata = file_contents[j].split()
        xy[0, j] = 1486.7-float(linedata[0])
        xy[1, j] = float(linedata[1])


    leftbinding = max(xy[0,:])
    rightbinding = min(xy[0,:])
    fig, ax = plt.subplots()
    ax.plot(xy[0, :], xy[1, :])
    plt.xlabel('Kinetic energy (eV)')
    plt.xlim((max(xy[0,:]), min(xy[0,:])))
    plt.title(i)
    plt.savefig(mypath+'/'+i[:-4]+'.png')
    plt.show()









