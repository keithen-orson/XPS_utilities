import os
import xps_reference
import pandas as pd
import matplotlib.pyplot as plt

mypath = input("input folder path: ")
if not (os.path.isdir(mypath)):
    raise NameError('path is not a directory')

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

onlyfiles = list_files(mypath)
print(onlyfiles)

for i in onlyfiles:

    (dirname, filename) = os.path.split(i)
    fileinname = filename
    fileoutname = 'shifted_' + filename
    fileoutname = os.path.join(dirname, fileoutname)

    #This checks that this is a copy of the original text file that has been trimmed with the kolxpdtrimmer file
    if (".txt" in i) and ("shifted_" in i):
        continue
    elif (".txt" in i) and ("copy" in i):
        pass
    else:
        continue

    xy = xps_reference.load_trimmed_spectra(filename=i,kinetictobinding=True)
    xycopy = xps_reference.shift_spectra(xy, -.63, manualinput=False)
    xycopy = pd.DataFrame(xycopy)
    xycopy.to_csv(
        fileoutname,
        index=False, header=False, sep=' ')