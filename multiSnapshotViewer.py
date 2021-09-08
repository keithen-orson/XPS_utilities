from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from tifffile import imsave

'''
This program loops through all of the snapshots and will visualize the time series of the scans of each different
category of scans (o1s, ni2p, etc) based on the energy that they start with.  
The program also removes outliers by removing the three edge detectors and anything that is three standard deviations away
from the average value.
The function to plot the different groups of scans can be modified to show time instead of temperature, but this is approximate
as the snapshots are not taken at exact times or temperatures.  
'''

mypath = input("input folder path: ")
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyfiles:
    if ('.txt') not in i:
        print('removed '+ i)
        onlyfiles.remove(i)
onlyfiles.sort(key=lambda x: x.split('-')[5])
onlyfiles.sort(key=lambda x: len(x))


counter = 0
masterlist = []
scantypes = []
scanenergies = []
startenergy = []
for i in onlyfiles:
    if not (".txt" in i):
        continue
    filepath = mypath + '/' + i
    f = open(filepath)
    lines = f.readlines()
    f.close()
    print(i)

    str_dataset = []
    dataset = []  # this becomes your full dataset by the end, in python list format

    # This block of code gets rid of the metadata starting with #, and sums up all of the individual measurements from
    # each snapshot, and gets (energy, intensity) data in the list 'dataset'
    for row in lines:

        if row.find('#') == -1:
            row_split = row.split()

            new_row = []
            row_str = ''  # accumulators
            intensity_sum = 0

            for element in row_split:
                try:
                    num_element = float(element)
                    if row_split.index(element) == 0:
                        new_row.append(num_element)
                        row_str += element + '\t'
                    else:
                        intensity_sum += num_element
                except:
                    pass
            row_str += str(intensity_sum) + '\n'
            str_dataset.append(row_str)
            new_row.append(intensity_sum)
            dataset.append(new_row)

    data = np.array(dataset)  # converts the data to a numpy array

    #this block gets the starting energies so we can sort different types of scans into different figures. Scantypes
    #just contains a list of how many different types of scans there are, identified by their starting energy.
    #scanenergies contains the actual energy values of each type of scan.  startenergy which scan is which type
    if scantypes.count(data[0, 0]) < 1:
        scantypes.append(data[0, 0])
        scanenergies.append(data[:, 0])
    startenergy.append(data[0,0])

    # The next ~20 lines makes a copy of the dataset(named data) and removes outliers by excluding the first three and last
    # three channels and excluding anything with a value or derivative that is three standard deviations away from the mean
    #I moved the outlier processing to a function so I can change parameters in a  more intuitive way.
    #THIS FUNCTION DOES NOT WORK OUTSIDE OF THE LOOP IT'S DEFINED IN- I know this is really bad programming but ehh
    def remove_outliers(edgesize, sigma):
        diffdata = np.gradient(data[:, 1])
        averagediff = np.average(diffdata)
        stddiff = np.std(diffdata)
        outlierlist = []
        averagintensity = np.average(data[:, 1])
        stdintensity = np.std(data[:, 1])

        for i in range(len(diffdata)):

            if (abs(diffdata[i] - averagediff) > sigma * stddiff):
                outlierlist = np.append(outlierlist, int(i))
                data[i,1] = np.NaN
            elif (abs(data[i, 1] - averagintensity) > sigma * stdintensity):
                outlierlist = np.append(outlierlist, int(i))
                data[i,1] = np.NaN

            if ((i <= (edgesize-1)) and len(diffdata) >= edgesize):
                outlierlist = np.append(outlierlist, int(i))
                data[i,1] = np.NaN
            elif ((len(diffdata) - i) <= edgesize):
                outlierlist = np.append(outlierlist, int(i))
                data[i,1] = np.NaN

    #actualy call the outlier remover function
    remove_outliers(3, 3)

    #remove_outliers(3, 3)
    #This block of code adds just the intensity data to a master list in the same order the files are read
    #masterlist has the intensity for a specific snapshot saved in the columns, whith each new row being a new shapshot
    if counter == 0:
        masterlist = data[:,1]
    else:
        masterlist = np.vstack((masterlist, data[:,1]))
    counter +=1


def plot_snapshot_series(choose, mintemp, maxtemp):
#choose which group of snapshots you want to plot.  This is the 2nd one in the list,
    indexes = []
    for i in range(len(startenergy)):
        if startenergy[i] == scantypes[choose]:
            indexes.append(i)
    if (len(indexes) <=2 ):
        print('two or less snapshots, can not plot')
        return 0
    plotdata = []
    for i in range(len(indexes)):
        index = indexes[i]
        plotdata.append(masterlist[index,:])
    print('plotting snapshots beginning at: '+str(1486.7-scantypes[choose]))

    plotdata = scipy.signal.medfilt(plotdata, 3)

    fig, ax = plt.subplots()
    end = len(scanenergies[choose])
    ax.imshow(plotdata, 'jet', extent=[1486.7-scanenergies[choose][0], 1486.7-scanenergies[choose][end-1],mintemp,maxtemp], aspect='auto', origin='lower')
    ax.set_xlabel('Binding energy (eV)')
    ax.set_ylabel('Approximate temperature (degrees C)')
    plt.savefig((mypath+'/'+str(choose)+'.tif'))
    plt.show()
    plt.colorbar


for i in range(len(scantypes)):
    plot_snapshot_series(i,20, 140)
