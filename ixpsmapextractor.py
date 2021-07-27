import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

mypath = '/Users/apple/Documents/Research/IXPS training'
#mypath = input("input folder path")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles:

    if "copy" in i:     #this block skips the file if it's a copy, and skips the file it it's not a text file
        continue
    elif ".txt" in i:
        pass
    else:
        continue

    filepath = mypath + '/' + i     #this block gets the full file path from the folder name and the file name
    #print(filepath)
    f = open(filepath)              #Open the file, then store the contents in "file_contents," then close it so that
    file_contents = f.readlines()   #python doesn't try and open like 100 files at a time
    f.close()

    while not file_contents[0].startswith('.'):     #gets rid of the lines up to the first line of data
        del(file_contents[0])

    newstring = file_contents[0]
    file_contents[0] = newstring[8:]

    counter = -1
    for line in file_contents:
        counter = counter + 1
        if 'Dim' in line:
            dimensions = line.split(',')
            filt1 = filter(str.isdigit, dimensions[0])
            xdim = int("".join(filt1))
            filt2 = filter(str.isdigit, dimensions[1])
            ydim = int("".join(filt2))
            continue

        cleaned = line[:-2]
        if counter >= (len(file_contents)-4):
            continue
        elif cleaned == '':
            print(counter)
            continue
        else:
            file_contents[counter] = float(cleaned)

    length = len(file_contents)
    cleaned = file_contents[length-4]
    file_contents[length-4] = float(cleaned[:-3])      #clean the parenthesis off the last data point
    del(file_contents[(length-3):length])       #delete the dimensions at the end of the file

    #print(file_contents)
    image = np.reshape(file_contents, (xdim, ydim))


    plt.imshow(image, 'gray')
    plt.show()





