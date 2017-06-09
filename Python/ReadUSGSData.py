#ReadUSGSData.py
#
# Description:
#  Accesses raw USGS water usage data and creates Numpy/Pandas table for analysis/visualization.
#  Provides the template for the following analyses:
#  - Merge data for 2000, 2005, and 2010 into a single data frame
#  - Aggregate county level data to the state level
#  - Generate state/county choropleth maps of different attributes
# 
# Summer 2017
# John.Fay@duke.edu

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Create a master data frame from the yearly file/url
theBaseURL = 'http://water.usgs.gov/watuse/data/{0}/usco{0}.txt' #Use format to replace {0} with year
#Initialize list of year data frames
dfs = []
#Loop through years
for year in (2000,2005,2010):
    print "Creating data frame for year {}...".format(year)
    #Create data frames from on-line tables
    df = pd.read_table(theBaseURL.format(year))
    #Insert year column if not there already
    cols = df.columns
    if not "YEAR" in df.columns:
        df.insert(4,"YEAR",year)
    #Create a list of column names
    cols.to_series().to_csv("cols{}.csv".format(year),index=False)
    #Append to list of dataframes
    dfs.append(df)
#Merge into a single table
print "Merging tables..."
df = pd.concat(dfs)

#Summarize data by state
grpState =  df[['STATE','TP-TotPop','PS-WFrTo']].groupby(df['STATE'])
dfState = grpState.sum()