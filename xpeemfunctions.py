from skimage import io
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from tifffile import imsave


def threshold(imgarray, darkparticles, sigma, thresholdvalue, usesigma):
    newarray = imgarray
    if (imgarray.ndim) > 1:
        newarray = imgarray.flatten
    mean = np.average(imgarray)
    stdev = np.std(imgarray)

    if usesigma == True:
        if darkparticles == True:
            for i in range(len(newarray)):
                if (newarray[i]) > (mean-sigma*stdev):
                    newarray[i] = 0
                else:
                    (newarray[i]) = 1
        else:
            for i in range(len(newarray)):
                if (newarray[i]) < (mean+sigma*stdev):
                    newarray[i] = 0
                else:
                    (newarray[i]) = 1

    if (usesigma == False):
        if darkparticles == True:
            for i in range(len(newarray)):
                if (newarray[i]) < thresholdvalue:
                    newarray[i] = 1
                else:
                    newarray[i] = 0
        else:
            for i in range(len(newarray)):
                if (newarray[i]) > thresholdvalue:
                    newarray[i] = 1
                else:
                    newarray[i] = 0
    if (imgarray.ndim) > 1:
        np.reshape(newarray, (imgarray.shape))
    return newarray

def meshplot(dataset_num, dimensions, temps):
    ax = plt.axes(projection='3d')
    X = np.linspace(0,dimensions[0]-1,dimensions[0])
    Y = X
    X,Y = np.meshgrid(X,Y)
    #dataset_num = 294   # change this number to look at a different dataset

    ax.plot_surface(X, Y, np.reshape(temps[dataset_num],(dimensions[0],dimensions[1])),cmap=cm.coolwarm, linewidth=0)            #plots fitted temp values
    #ax.plot_surface(X,Y, np.reshape(best_fits[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap=cm.Blues)     #plots best fit plane
    #ax.plot_surface(X,Y, np.reshape(means[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap = cm.summer)         #plots mean value
    #ax.plot_surface(X,Y, np.reshape(old_temps[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap = cm.copper)     #plots unaltered temp values
