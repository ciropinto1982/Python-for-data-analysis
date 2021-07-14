### Python script to read and join lightcurves from individual observations

# information about pyfits library ------> https://pythonhosted.org/pyfits/
# about matplotlib.pyplot (plotting library) ---> https://matplotlib.org/api/pyplot_api.html

## ------ STEP 0 -------- ##
# Read useful libraries

import numpy as np
import matplotlib.pyplot as plt
import pyfits
#from matplotlib.font_manager import FontProperties
#from matplotlib.legend_handler import HandlerLine2D
#from matplotlib import rc, font_manager
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#import statistics
#import math

## ------ STEP 1 -------- ##
# Open lc fits files (0.3-10 keV)
# Using fits files as ascii are in bad format (have an "&" at the end)
# Let's assume that in the current directory there's a subdirectory of each of 5 observations
# and that in each directory there is an XMM/EPIC-PN lightcurve extracted within 0.3-10 keV
# extracted with the standard epiclccorr XMM SAS taks with the following (same) name
# for each observation: PN_lccorr_0310keV.lc

OBS_id=['0000000001','0000000002','0000000003','0000000004','0000000005'] # TO BE UPDATED!

directory='./'

filename=directory+str(OBS_id[0])+'/'+'PN_lccorr_0310keV.lc' # first piece

lc=pyfits.open(filename)
da=lc[1].data
t1=da.field(0)
r1=da.field(1)
e1=da.field(2)

time=t1-t1[0]
rate=r1
erro=e1

filter=np.where((rate>0.1) & (rate+erro<2.4)) # Filtering lightcurve from bad times
time=time[filter]                        # filtering bad (low expo) values
rate=rate[filter]
erro=erro[filter]

time=np.arange(0.0,len(time),1)*1e3  # To remove breaks due to bad points

tsta=np.max(time)-time[0]+1e3

tstop_array=np.zeros(5)
tstop_array[0]=tsta

for i in range(1,5):
    print(str(OBS_id[i]))
    filename=directory+str(OBS_id[i])+'/'+'PN_lccorr_0310keV.lc' # following frames
    lc=pyfits.open(filename)                                     # temporary values
    da=lc[1].data
    tt=da.field(0)
    rt=da.field(1)
    et=da.field(2)
    filter=np.where((rt>0.1) & (rt+et<2.4)) # Filtering lightcurve from bad times and low exposure bins
    tt=tt[filter]                           # (update these values e.g. 0.1,2.4 according to your source)
    rt=rt[filter]
    et=et[filter]
    tt=np.arange(0.0,len(tt),1)*1e3  # To remove breaks due to bad points
    ts=np.max(tt)-tt[0]
    tt=np.array(tt-tt[0]+tsta)
    rt=np.array(rt)
    et=np.array(et)
    time=[*time,*tt]
    rate=[*rate,*rt]
    erro=[*erro,*et]
    tsta=np.max(time)-time[0]+1e3
    tstop_array[i]=tsta

print(tstop_array)

time=np.array(time)
rate=np.array(rate)
erro=np.array(erro)

time=np.arange(0.0,len(time),1)*1e3  # To remove any further breaks due to bad points

## ------ STEP 3--------- ##
# Make PLOT

fig1=plt.figure(1)
frame1=fig1.add_axes((.09,.1,0.9,0.85))

#plt.plot(time,rate, color='k', linewidth=0.8)
#plt.scatter(time,rate, color='k', linewidth=0.5)
plt.errorbar(time,rate,yerr=erro, linewidth=0.5, ecolor="black")

for i in range(0,4):
    rate_new=[0.0,2.3]
    time_edit=tstop_array[i]
    time_new=[time_edit,time_edit]
    plt.plot(time_new,rate_new, color='black', linewidth=1.0, linestyle=':')

plt.ylabel('Rate (c/s)')
plt.xlabel('Time (s)')
plt.ylim([0.5,2.3])
plt.xlim([-5e3,4.15e5])
plt.savefig('lc_0310keV.png')
plt.close('all')

## ------ STEP 4--------- ##
# Save joint lightcurve

Par_list='Time, Rate, Error'

Table_lc=[time, rate, erro]

Table_lc=np.array(Table_lc)

Table_lc=Table_lc.transpose()

f1=open('lc_0310keV.txt', 'wb')     # APPEND MODE N-items + items
np.savetxt(f1, Table_lc, delimiter=' ',fmt='%2.3f',header=Par_list)
f1.close()



