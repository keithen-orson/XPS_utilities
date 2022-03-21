from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from peakfit_functions import *

#mypath = input("input file path: ")
mypath = '/Users/apple/Documents/Research/Muri NiCr experiments/NiCr bare metal/5-26/data.csv'
master = pd.read_csv(mypath)

peakfit = []

# fig = plotall(master, plotrange=(0, 1000))
# plt.xlim(1000, 0)
# plt.xlabel("binding energy (eV)")
# plt.show()

for j in range(int(len(master.columns)/2)):
    tempx = pd.DataFrame
    tempy = pd.DataFrame
    for i, col in enumerate(master.columns):

        if (int(col.split(" ")[1]) == j) and ('binding' in col):
            print(col)
            tempx = master[col]
        elif(int(col.split(" ")[1]) == j) and ('intensity' in col):
            print(col)
            tempy = master[col]

    if tempy.empty:
        print('array empty')
        continue
    tempx = tempx.dropna()
    tempy = tempy.dropna()
    x = tempx.to_numpy()
    y = tempy.to_numpy()

    parameters = fit_ni2p32(x, y)







