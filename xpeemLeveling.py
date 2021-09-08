
from skimage import io
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from tifffile import imsave
from xpeemfunctions import threshold
from xpeemfunctions import meshplot

'''
Right now this script takes a .tif file and performs a plane leveling operation on every frame in it.
what I need to do is take the plane leveling function and just put it into it's own function that I can use later.  

this code works now- the array temps has the correct data but somehow the array xpeem doesn't.  
the data losses showing up at the peaks is happening at line 62, where i'm moving the transformed data into the original matrix, I just don't know why
'''

#mypath = input("input file path")  #this needs to be the file path right now
mypath= '/Users/apple/Documents/Research/NiCr XPEEM/segmentation movie 2/'
myfile = 'region 1 crop only.tif'
xpeem = io.imread(mypath+myfile)

#print(type(xpeem).__name__)
#print(xpeem.shape)
new_temps = []
old_temps = []
best_fits = []
means = []
temps = []
for i in range(len(xpeem)):

    temp = xpeem[i, :, :]
    #get the intensity values
    dimensions = temp.shape
    temp = temp.flatten()     #turn the intensity values into a flat array of z values
    mean = np.average(temp)
    totalpoints = dimensions[0]*dimensions[1]
    xarray = np.linspace(0, totalpoints-1, totalpoints)%dimensions[0]
    yarray = np.linspace(0, dimensions[1]-1, totalpoints)        #a sequence that makes y values that correspond to the z points
    yarray = [int(item) for item in yarray]                     #turn the y values into ints
    flat = np.ones(xarray.shape)    #make an array of zeros to represent the coefficients in the below equation
    coefs = np.linalg.lstsq(np.stack([xarray, yarray, flat]).T, temp, rcond=None)[0]        #least squares solver for the coefficients of the plane
    #print(coefs)
    best_fit = np.zeros(totalpoints)
    original_temps = np.zeros(totalpoints)
    mean_grid = np.zeros(totalpoints)
    new_temps = np.zeros(totalpoints)
    for j in range(len(temp)):
        fit_val = (coefs[0] * xarray[j] + coefs[1] * yarray[j] + coefs[2])
        best_fit[j] = fit_val
        mean_grid[j] = mean
        original_temps[j] = temp[j]
        zdiff = fit_val-mean #get the difference between the plane fit and the
        new_temp = temp[j]-zdiff
        new_temps[j] = new_temp
        if new_temp < 700:
            print(temp[j],zdiff)

    means.append(mean_grid)
    best_fits.append(best_fit)
    old_temps.append(original_temps)

    temps.append(threshold(new_temps,False,1.5,mean+8000, False))
    #temps.append(new_temps)



    xpeem[i, :, :] = np.reshape(new_temps, (dimensions[0], dimensions[1]))       #replace the data in each frame with the plane leveled data



'''def meshplot(dataset_num, dimensions, temps):
    ax = plt.axes(projection='3d')
    X = np.linspace(0,dimensions[0]-1,dimensions[0])
    Y = X
    X,Y = np.meshgrid(X,Y)
    #dataset_num = 294   # change this number to look at a different dataset

    ax.plot_surface(X, Y, np.reshape(temps[dataset_num],(dimensions[0],dimensions[1])),cmap=cm.coolwarm, linewidth=0)            #plots fitted temp values
    #ax.plot_surface(X,Y, np.reshape(best_fits[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap=cm.Blues)     #plots best fit plane
    #ax.plot_surface(X,Y, np.reshape(means[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap = cm.summer)         #plots mean value
    #ax.plot_surface(X,Y, np.reshape(old_temps[dataset_num],(40,40)),  linewidth=0, antialiased=False, cmap = cm.copper)     #plots unaltered temp values
'''
dataset_num = 294
meshplot(dataset_num, dimensions, temps)

for i in range(len(xpeem)):
    temparray = np.reshape(temps[i], (dimensions[0], dimensions[1]))
    temps[i] = temparray

temps = np.array(temps)
final_data = np.array(temps)


print(np.shape(temps))
print(type(temps))
print(np.shape(xpeem))
print(type(xpeem))
testarray = (xpeem[dataset_num,:,:])
print(np.amin(testarray))

plt.show()


plt.imshow(temps[dataset_num, :, :], 'jet', origin='lower')
plt.show()

imsave('multipage.tif', final_data)
