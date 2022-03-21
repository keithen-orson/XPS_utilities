import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
from matplotlib import gridspec
import peakfit_functions as pf

"""peak fitting practice in python based off the tutorial by Emily Ripka

https://github.com/emilyripka/BlogRepo/blob/master/181119_PeakFitting.ipynb
"""


# linearly spaced x-axis of 10 values between 1 and 10
x_array = np.linspace(1,100,50)

"""Simple gaussian and multiple gaussian examples"""
#
# amp1 = 100
# sigma1 = 10
# cen1 = 50
# y_array_gauss = amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x_array-cen1)/sigma1)**2)))
#
# # creating some noise to add the the y-axis data
# y_noise_gauss = (np.exp((np.random.ranf(50))))/5
# y_array_gauss += y_noise_gauss
#
# fig = plt.figure(1)
# gs = gridspec.GridSpec(1,1)
# ax1 = fig.add_subplot(gs[0])
#
# ax1.plot(x_array, y_array_gauss, "ro")
#
# popt_gauss, pcov_gauss = scipy.optimize.curve_fit(pf._1gaussian, x_array, y_array_gauss, p0=[amp1, cen1, sigma1])
# perr_gauss = np.sqrt(np.diag(pcov_gauss))
#
#
# # this cell prints the fitting parameters with their errors
# print("amplitude = %0.2f (+/-) %0.2f" % (popt_gauss[0], perr_gauss[0]))
# print("center = %0.2f (+/-) %0.2f" % (popt_gauss[1], perr_gauss[1]))
# print("sigma = %0.2f (+/-) %0.2f" % (popt_gauss[2], perr_gauss[2]))
#
# fig2 = plt.figure(2)
# ax1 = fig2.add_subplot(gs[0])
# ax1.plot(x_array, y_array_gauss, "ro")
# ax1.plot(x_array, pf._1gaussian(x_array, *popt_gauss), 'k--')
#
# amp1 = 100
# sigma1 = 10
# cen1 = 40
#
# amp2 = 75
# sigma2 = 5
# cen2 = 65
#
# y_array_2gauss = amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x_array-cen1)/sigma1)**2))) + \
#                 amp2*(1/(sigma2*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x_array-cen2)/sigma2)**2)))
#
# # creating some noise to add the the y-axis data
# y_noise_2gauss = (np.exp((np.random.ranf(50))))/5
# y_array_2gauss += y_noise_2gauss
# fig3 = plt.figure(3)
# ax1 = fig3.add_subplot(gs[0])
# ax1.plot(x_array, y_array_2gauss, "ro")
#
# popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(pf._2gaussian, x_array, y_array_2gauss, p0=[amp1, cen1, sigma1,
#                                                                                              amp2, cen2, sigma2])
#
# perr_2gauss = np.sqrt(np.diag(pcov_2gauss))
#
# pars_1 = popt_2gauss[0:3]
# pars_2 = popt_2gauss[3:6]
# gauss_peak_1 = pf._1gaussian(x_array, *pars_1)
# gauss_peak_2 = pf._1gaussian(x_array, *pars_2)
#
# fig4 = plt.figure(4)
# ax1 = fig4.add_subplot(gs[0])
# ax1.plot(x_array, y_array_2gauss, "ro")
# ax1.plot(x_array, gauss_peak_1, 'g')
# ax1.plot(x_array, gauss_peak_2, 'y')
# print(type(popt_2gauss))
# ax1.plot(x_array, pf._2gaussian(x_array, *popt_2gauss), 'k--')

"""Simple Voigt Peaks"""

x_array = np.linspace(1,100,50)

ampG1 = 21
cenG1 = 50
sigmaG1 = 5
ampL1 = 80
cenL1 = 50
widL1 = 5

y_array_voigt = (ampG1*(1/(sigmaG1*(np.sqrt(2*np.pi))))*(np.exp(-((x_array-cenG1)**2)/((2*sigmaG1)**2)))) +\
                ((ampL1*widL1**2/((x_array-cenL1)**2+widL1**2)) )
background = np.zeros(len(x_array))
background[0:25] = 10
y_array_voigt = y_array_voigt + background
# creating some noise to add the the y-axis data
y_noise_voigt = (((np.random.ranf(50))))*5
y_array_voigt += y_noise_voigt

shirley_br = pf.shirley_calculate(x_array, y_array_voigt)

popt_1voigt, pcov_1voigt = scipy.optimize.curve_fit(pf._1Voigt, x_array, (y_array_voigt-shirley_br), p0=[ampG1, cenG1, sigmaG1,
                                                                                         ampL1, cenL1, widL1])

perr_1voigt = np.sqrt(np.diag(pcov_1voigt))
pars_1 = popt_1voigt
voigt_peak_1 = pf._1Voigt(x_array, *pars_1)
residual_1voigt = y_array_voigt - pf._1Voigt(x_array, *popt_1voigt)-shirley_br

fig = plt.figure(5, figsize=(4,4))
gs = gridspec.GridSpec(2,1, height_ratios=[1,0.25])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
gs.update(hspace=0)

ax1.plot(x_array, y_array_voigt, "ro")
ax1.plot(x_array, pf._1Voigt(x_array, *popt_1voigt), 'k--')#,\
         #label="y= %0.2f$e^{%0.2fx}$ + %0.2f" % (popt_exponential[0], popt_exponential[1], popt_exponential[2]))

# peak 1
ax1.plot(x_array, voigt_peak_1, "g")
ax1.fill_between(x_array, voigt_peak_1.min(), voigt_peak_1, facecolor="green", alpha=0.5)

# residual
ax2.plot(x_array, residual_1voigt, "bo")

ax1.plot(x_array, shirley_br, '^')

plt.show()