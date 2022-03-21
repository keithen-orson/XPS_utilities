import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
import pandas as pd

"""Calculates the a, b and c constants for the transmission function.  Reads in a CSV that has only column names
and one of the columns is labeled RR for retard ratio and one is named I for intensity """

data = pd.read_csv('/Users/apple/Documents/Research/XPS Analysis/XPS calibrations/transmission function data au.csv')
data = data.sort_values(by=['RR'])
print(data)
fig = plt.figure()
ax = fig.add_subplot()
ax.set_xscale('log')
rr = np.array(data['RR'])
i = np.array(data['I'])
plt.scatter(rr,i)

guess = [100,2,5000]
def irr(rr, a, b, c):
    return c*(a**2/(a**2+rr**2))**b


popt, pcov = scipy.optimize.curve_fit(irr, rr, i,p0=guess)
print(popt)
synthrr = np.linspace(10,120)
plt.plot(synthrr,irr(synthrr,popt[0],popt[1],popt[2]))
plt.show()