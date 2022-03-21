from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import peakfit_functions


#/Users/apple/Documents/Research/Muri NiCr experiments/NiCr bare metal/5-26/trimmed clean ni2p.txt
filename = input("Input file name: ")
f = open(filename)
file_contents = f.readlines()
f.close()
xy = np.zeros((2, len(file_contents)))
for j in range(len(file_contents)):
    linedata = file_contents[j].split()
    xy[0, j] = 1486.7 - float(linedata[0])
    xy[1, j] = float(linedata[1])

parameters = peakfit_functions.fit_ni2p32(xy[0, :], xy[1, :])




