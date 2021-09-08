from os import listdir
from os.path import isfile, join
import numpy as np

'''
Takes a folder path, scans all of the xps data, trims it (ignores files that have already been converted), converts the kinetic energy to binding energy 
and normalizes the height of the curves to 1

This script only works on sweep scans (one xy column) and will save a copy of xy data with the metatdata (notated by #)
removed.  
'''

mypath = input("input folder path: ")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles:

    if ("igor" in i):
        continue
    elif (".txt" in i):
        pass
    else:
        continue
    filepath = mypath + '/' + i
    print(filepath)
    f = open(filepath)
    file_contents = f.readlines()
    f.close()

    while file_contents[0].startswith('#'):
        del(file_contents[0])


    xy = np.zeros((2, len(file_contents)))
    for j in range(len(file_contents)):
        linedata = file_contents[j].split()
        xy[0, j] = 1486.7-float(linedata[0])
        xy[1, j] = float(linedata[1])

    maxintensity = max(xy[1, :])
    minintensity = min(xy[1,:])
    xy[1,:] = (xy[1,:]-minintensity)/(maxintensity-minintensity)

    for j in range(len(file_contents)):
        file_contents[j] = ''+str(xy[0,j]) + '   ' + str(xy[1,j])+'\n'


    copyname = mypath+'/'+'igor_'+i
    copy = open(copyname, "w")
    for lines in file_contents:
        copy.write('%s' % lines)

    copy.close()