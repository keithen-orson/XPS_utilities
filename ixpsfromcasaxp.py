#This script will extract the data from the casaxp (.vms) exported file format for the ixps maps.
#The data is stored in a list of numpy arrays, that can be manipulated however.  Right now it applies a median filter
#and then plots only the energies that correspond to the copper peak (552-554 eV).
#The program also extracts the dimensions of the ixps maps (although it hasn't been tested with different dimensions yet).


import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import scipy.signal

mypath = '/Users/apple/Documents/Research/IXPS training'
#mypath = input("input folder path")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles:

    if "copy" in i:     #this block skips the file if it's a copy, and skips the file it it's not a text file
        continue
    elif ".vms" in i:
        pass
    else:
        continue

    filepath = mypath + '/' + i     #this block gets the full file path from the folder name and the file name
    #print(filepath)
    f = open(filepath)              #Open the file, then store the contents in "file_contents," then close it so that
    file_contents = f.readlines()   #python doesn't try and open like 100 files at a time
    f.close()

    energies = []
    dimensions = []
    data = []
    for j in range(len(file_contents)):
        if "XPS" in file_contents[j]:
            energies.append(float(file_contents[j+1]))
            currentdimensions = (int(file_contents[j+13]), int(file_contents[j+14]))
            dimensions.append(currentdimensions)
            points = currentdimensions[0]*currentdimensions[1]          #figures out how many data points to expect in the image maps
            currentdata = np.array(file_contents[j+42:j+points+42])     #42 is the number of lines to skip in the metadata
            currentdata = [float(x) for x in currentdata]

            currentdata = np.reshape(currentdata, currentdimensions)
            data.append(np.reshape(currentdata, currentdimensions))

    #print(energies)
    #print(dimensions)

    image = np.empty(currentdimensions)
    counter = 0
    for energy in energies:
        if (energy >=552 and energy <=554):         #plots the energies of all the
            image = np.add(image, data[counter])
        counter +=1

    image = scipy.signal.medfilt(image, 3)
    plt.imshow(image, 'gray')
    plt.title(i)
    plt.colorbar()
    plt.show()

