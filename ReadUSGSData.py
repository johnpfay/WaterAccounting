#ReadUSGSData.py
#
# Description:
#  Accesses raw USGS water usage data and creates Numpy/Pandas table for analysis/visualization.
# 
# Summer 2017
# John.Fay@duke.edu

#Import modules
import sys, os, urllib
import pandas as pd
import numpy as np

#Get paths
rootFolder = os.path.dirname(sys.argv[0])

#Retrieve annual water usage data, if not present already
for year in ['2005','2010']:
    theURL = 'http://water.usgs.gov/watuse/data/{0}/usco{0}.txt'.format(year)
    theFN = theURL.split("/")[-1]
    theFullFN = os.path.join(rootFolder,theFN)
    if not os.path.exists(theFullFN):
        print("Downloading {}".format(theURL))
        theResponse = urllib.urlretrieve(theURL,theFullFN)
        print("...Done!")
    else:
        print("{} already rerieved".format(theURL))

#Create data frames from the documents
theData = pd.read_csv(theFullFN,'\t')
