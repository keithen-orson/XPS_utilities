import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

masterdata = pd.read_csv('/Users/apple/Documents/Research/Muri NiCr experiments/Muri Master Data.csv')

masterdata = masterdata.astype('float', errors='ignore')
masterdata = masterdata.fillna(0)
roomdata = masterdata[(masterdata['Temperature'] <100)]
hightempdata = masterdata[(masterdata['Temperature'] >= 400)]
molydata = masterdata[(masterdata['Mo Fraction'] >0)]
nomolydata = masterdata[(masterdata['Mo Fraction'] == 0)]
croandohfrac = (masterdata['Cr 2p CrOH']+masterdata['Cr 2p Cr(IV) oxide']+masterdata['Cr 2p Cr2O3'])/masterdata['Total Signal']
bulk = roomdata[(roomdata['Angle'] ==0 ) & (roomdata['Base compositoin'])]
surface = roomdata[(roomdata['Angle'] >= 30) & (roomdata['Base compositoin'])]



fig4 = plt.figure(4)
plt.scatter(molydata['Temperature'], molydata['Cr O+OH/total'])
plt.scatter(nomolydata['Temperature'], nomolydata['Cr O+OH/total'])


fig1 = plt.figure(1)
plt.hist(molydata['Cr metal fraction'], alpha=.5)
plt.hist(molydata['Cr OH Fraction'], alpha=.5)


fig2 = plt.figure(2)
plt.hist(molydata['Cr metal fraction'], alpha=.5)
plt.hist(molydata['Cr OH Fraction'], alpha=.5)



fig3 = plt.figure(3)
ax = fig3.add_subplot(projection='3d')
ax.scatter(nomolydata['Cr OH Fraction'], nomolydata['Oxide/Hydroxide ratio from Ni and Cr'], nomolydata['Temperature'], alpha=.5)
ax.scatter(molydata['Cr OH Fraction'], molydata['Oxide/Hydroxide ratio from Ni and Cr'], molydata['Temperature'])
ax.set_xlabel('Cr OH fraction')
ax.set_ylabel('Oxide/Hyroxide Ratio')
ax.set_zlabel('Temperature')


plt.show()