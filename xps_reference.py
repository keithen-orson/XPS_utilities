import numpy
import numpy as np
import pandas as pd
import scipy.interpolate as interp
import matplotlib.pyplot as plt
import scipy.optimize as opt
import peakfit_functions

refspectra = '/Users/apple/Documents/Research/Muri NiCr experiments/NiCr bare metal/5-26/copy20210526-101021_--ESp_Cayman_iXPS--6_1-Detector_Region.txt'
experimentalspectra = '/Users/apple/Documents/Research/Muri NiCr experiments/Muri Ni22Cr6Mo slow 12-17-21/23c/0/copy_20211217-115137_Muri Ni22Cr6Mo slow--ESp_Cayman_iXPS--3_1-Detector_Region.txt'

def load_csv(fileoutname, fileinname=True, ):
    """this function is a work in progress, don't use yet"""
    if fileinname == True:
        fileinname = input("Input file name: ")
    print(fileinname)
    xy = pd.read_csv(fileinname)
    xy.to_csv(
        fileoutname,
        index=False, header=False, sep=' ')
    return xy

def load_trimmed_spectra(filename=True, kinetictobinding=True):
    """This function takes a filename and loads a single spectra from it.  The spectra must be just the xy
    data in the format [kinetic energy, intensity] with no header.  It returns the data transformed from
    kinetic energy to binding energy assuming an Al K alpha x-ray source"""

    if filename == True:
        filename = input("Input file name: ")
    print(filename)
    f = open(filename)
    file_contents = f.readlines()

    f.close()
    xy = np.zeros((2, len(file_contents)))
    for j in range(len(file_contents)):
        linedata = file_contents[j].split()

        #stops reading the file at any blank lines
        if not(linedata):
            print("blank lines found, exiting file reader")
            break

        #changes kinetic energy (the default format) to binding energy
        if kinetictobinding:
            xy[0, j] = 1486.7 - float(linedata[0])
            xy[1, j] = float(linedata[1])
        else:
            xy[0, j] = float(linedata[0])
            xy[1, j] = float(linedata[1])

    xy = np.transpose(xy)
    xycopy = xy

    #make sure the binding energies are sorted in ascending order
    xy = xycopy[np.argsort(xycopy[:,0])]
    return xy

def shift_spectra(xy, shift, manualinput=False):
    """shifts a spectra by amount shift"""

    inputshape = xy.shape
    if inputshape[1] != 2 and inputshape[0] == 2:
        xy = np.transpose(xy)
        print("linear_interpolate() transposed the x,y data")
    if manualinput:
        shift = float(input("Energy Shift: "))


    xy[:,0] = xy[:,0] + shift

    return xy

def spectra_interpolate(xy, step, bounds):
    """Given an input array of x, y values, this will interpolate the data using scipy's cubic interpolation
    to get a function with the interpoolated data and desired boundaries and step """
    inputshape = xy.shape
    if inputshape[1] != 2 and inputshape[0] == 2:
        xy = np.transpose(xy)
        print("linear_interpolate() transposed the x,y data")

    f = interp.interp1d(xy[:,0], xy[:,1], kind='linear')
    xnew = np.arange(bounds[0], bounds[1]+step, step)
    ynew = f(xnew)
    xnew = np.array(xnew)
    ynew = np.array(ynew)
    interpolated = np.stack((xnew,ynew))

    return np.transpose(interpolated)

def normalize_spectra_to(target, spectra):
    """normalizes the height of one spectra to that of a target spectrum.  Takes x,y data in a numpy array
    and returns an array of x,y column data"""
    target = np.array(target)
    spectra = np.array(spectra)

    #check the dimensions of the input x,y columns to make sure they are shaped the same
    targetshape = target.shape
    if targetshape[1] != 2 and targetshape[0] == 2:
        target = np.transpose(target)
        print("transposed the x,y data for target")

    spectrashape = spectra.shape
    if spectrashape[1] != 2 and spectrashape[0] == 2:
        spectra = np.transpose(spectra)
        print("transposed the x,y data for spectra")



    target_max = np.max(target[:,1])
    target_min = np.min(target[:,1])
    spectra_max = np.max(spectra[:,1])
    spectra_min = np.min(spectra[:,1])

    normed_spectra = np.zeros(spectra.shape)
    normed_spectra[:,0] = spectra[:,0]

    #first normalized intensity of the spectra to the range 0-1
    normed_spectra[:,1] = (spectra[:,1]-spectra_min)/(spectra_max-spectra_min)

    #then normalize the intensityu the spectra to the target spectra
    normed_spectra[:,1] = (normed_spectra[:,1]*(target_max-target_min))+target_min

    return normed_spectra

def subtract_spectra(experimental, reference, wiggle, shirley_subtract=False, testregion=(0,75)):
    """This subtracts a reference spectra (xy columns) from an experimental spectra.  The wiggle parameter
    defines how far the reference spectra can move to account for charging.  Testregion defines the data point
    range for peak alignment process is.  For the Nickel 2p3/2 with step size .05 ev, the metal peaks are
    within the first ~75 data points, or 3.75 eV"""
    #how many steps the reference spectra is allowed to move needs to be an integer
    wiggle = int(wiggle)

    #make sure the arrays are numpy arrays and the arrays are both in ascending order
    expcopy = np.array(experimental)
    refcopy = np.array(reference)

    experimental = expcopy[np.argsort(expcopy[:,0])]
    reference = refcopy[np.argsort(refcopy[:,0])]
    print(detect_bounds(experimental))
    print(detect_bounds(reference))

    fig6 = plt.figure(6)
    plt.plot(experimental[:, 0], experimental[:, 1])
    plt.plot(reference[:, 0], reference[:, 1])

    if (shirley_subtract):
        experimentalbr = peakfit_functions.shirley_calculate(experimental[:,0], experimental[:,1])
        referencebr = peakfit_functions.shirley_calculate(reference[:,0], reference[:,1])
        print("subtracted shirley background from spectra")

        plt.plot(reference[:,0], referencebr)
        plt.plot(experimental[:,0],experimentalbr)
        experimental[:,1] = experimental[:,1]-experimentalbr
        reference[:,1] = reference[:,1]-referencebr

    #normalize the height of the reference spectra to the height of the experimental spectra
    reference = normalize_spectra_to(experimental,reference)


    #trim the reference spectra so it can be wiggled without index errors
    trimmed_reference = reference[0:-wiggle,:]

    residualsum = np.zeros(wiggle)
    for i in range(wiggle):
        trimmed_experimental = experimental[i:-(wiggle-i),:]
        residualsum[i] = np.sum(trimmed_experimental[testregion[0]:testregion[1],:]-trimmed_reference[testregion[0]:testregion[1],:])
        fig5 = plt.figure(5)



    index = np.where(np.absolute(residualsum) == np.amin(np.absolute(residualsum)))
    #index = int(index[0])
    index = 5

    #make a new shifted reference

    shifted_ref = reference[index:-(index+1),:]

    #shift the binding energy
    shifted_ref[:,0] = shifted_ref[:,0]+(index+1)*(shifted_ref[1,0]-shifted_ref[0,0])
    #print(shifted_ref)
    #trim the experimental so they're the same length and can be subtracted, also so they start at the same binding energy
    trimmed_experimental = experimental[2*index+1:,:]
    #print(trimmed_experimental)

    subtracted = trimmed_experimental-shifted_ref
    subtracted[:,0] = trimmed_experimental[:,0]
    plt.plot(subtracted[:,0],subtracted[:,1])
    plt.show()
    return subtracted

def detect_bounds(spectra):
    return np.min(spectra[:,0]), np.max(spectra[:,0])

"""Testing the spectra_interpolate() function """
# data = load_trimmed_spectra()
# fig1 = plt.figure(1)
# plt.plot(data[0,:],data[1,:])
#
# xnew, ynew = spectra_interpolate(data, .05, (850,864))
#
# fig2 = plt.figure(2)
# plt.plot(xnew, ynew)
# plt.show()

# """testing the normalize_spectra_to() function"""
# #subtract the shirley backgrounds by hand using the good compound background from kolxpd
# niexpbr = load_trimmed_spectra(kinetictobinding=False, filename="/Volumes/DATA STICK/Muri Ni22Cr6Mo slow 12-17-21/Curve subtraction tests/Ni bck copy.txt")
# niexpbr = np.vstack((niexpbr, niexpbr[-1,:]))
# niexpbr[-1,0] = niexpbr[-1,0]+.05
# niexpbr[:,0] = niexpbr[:,0]+.1
# print(detect_bounds(niexpbr))
# ref = load_trimmed_spectra(filename=refspectra)
# exp = load_trimmed_spectra(filename=experimentalspectra)
# print(detect_bounds(exp))
# refbr = peakfit_functions.shirley_calculate(ref[:,0],ref[:,1])
# exp[:,1] = exp[:,1]-niexpbr[:,1]
# ref[:,1] = ref[:,1]-refbr
#
#
# fig3 = plt.figure(3)
# plt.plot(ref[:,0],ref[:,1])
# plt.plot(exp[:,0],exp[:,1])
#
# normed = normalize_spectra_to(exp, ref)
# refupper = np.average(normed[-5:,1])
# normed = numpy.vstack(([[865,0],[865.1, 0]], normed))
#
# min, max = detect_bounds(exp)
#
# trimmednormed = spectra_interpolate(normed, .05, (min,max))
#
# fig4 = plt.figure(4)
# plt.plot(exp[:,0],exp[:,1])
# plt.plot(trimmednormed[:,0],trimmednormed[:,1])
# plt.show()
#
# finished = subtract_spectra(exp,trimmednormed,20,shirley_subtract=False)
# finaldata = pd.DataFrame(finished)
# finaldata.to_csv('/Users/apple/Documents/Research/Muri NiCr experiments/Muri Ni22Cr6Mo slow 12-17-21/subtracttest.csv', index=False, header=False)


