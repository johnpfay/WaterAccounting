#DaymetExtract.py
#
# Download and manipulate daymet precip data
# Data source https://thredds.daac.ornl.gov/thredds/catalog/ornldaac/1343/catalog.html

from matplotlib import pyplot as plt
import pandas as pd
import netCDF4

url='https://thredds.daac.ornl.gov/thredds/dodsC/ornldaac/1343/daymet_v3_prcp_annttl_1980_hi.nc4'
vname = 'Tx_1211'
station = 0

nc = netCDF4.Dataset(url)
h = nc.variables[vname]
times = nc.variables['time']
jd = netCDF4.num2date(times[:],times.units)
hs = pd.Series(h[:,station],index=jd)

fig = plt.figure(figsize=(12,4))
ax = fig.add_subplot(111)
hs.plot(ax=ax,title='%s at %s' % (h.long_name,nc.id))
ax.set_ylabel(h.units)