# #### Downscaled Climate Projections Archive processing
# ###### Workflow
# * Submit data request
# * Download data to data folder
# * Process NetCDF files into dataframes
# * Compute annual means (2000, 2005, and 2010) from monthly data
# * Compute means for each state

#Import libraries
import sys, os, glob, time, datetime
import numpy as np
import pandas as pd
import netCDF4
import matplotlib

#Get nc filenames
dataFolder = r'C:\Workspace\Gits\WaterAccounting\Data\hydro5\*.nc'
dataFiles = glob.glob(dataFolder)
dataFile = dataFiles[0]
print dataFile

for dataFile in dataFiles:
    print "Working on " + dataFile

    #Extract data
    nc = netCDF4.Dataset(dataFile,mode='r')
    print nc.variables.keys()

    #Get the static variables
    times = nc.variables['time']
    lats = nc.variables['latitude'][:]
    lons = nc.variables['longitude'][:]

    #Get the specific variable (last in list)
    param_name = nc.variables.keys()[-1]
    paramData = nc.variables[param_name]


    #Format of the et variable
    print param.shape
    #21 different projections
    #132 months (Jan 2000 thru Dec 2010)
    #216 N-S samples (latitudes)
    #460 E-W samples (longitudes)

    #Make yearly means of the ccsm4.1.rcp26 projection (idx = 2)

    #Set the index of the climate model to use -- see projections5.txt
    rcpIndex = 2 #ccsm4.1.rcp26 

    t0 = 0
    data2000 = paramData[rcpIndex,t0:t0+12,:,:].mean(axis=0)

    t5 = 5 * 12
    data2005 = paramData[rcpIndex,t5:t5+12,:,:].mean(axis=0)

    t10 = 10 * 12
    data2010 = paramData[rcpIndex,t10:t10+12,:,:].mean(axis=0)

    print data2000.shape, data2005.shape, data2010.shape
    #This leaves us with 3 ndarrays: one for each year with et values at each lat/long


    #Export as table of x,y, et
    outFile = open("{}.csv".format(param_name),'wt')
    outFile.write("Longitude,Latitude,y2000,y2005,y2010\n")
    for x in xrange(lons.size):
        for y in xrange(lats.size):
            etVal00 = et2000[y,x]
            etVal05 = et2005[y,x]
            etVal10 = et2010[y,x]
            outStr = "{},{},{},{},{}\n".format(lons[x],lats[y],etVal00,etVal05,etVal10)
            if type(et2005[y,x]) is not np.ma.core.MaskedConstant: 
                outFile.write(outStr)
    outFile.close()
        



