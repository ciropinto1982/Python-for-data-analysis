# This script opens the light surve fits file and plot the columns needed (time and rate)

# information about pyfits library ------> https://pythonhosted.org/pyfits/
# about matplotlib.pyplot (plotting library) ---> https://matplotlib.org/api/pyplot_api.html

import numpy as np
import pyfits
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import rc, font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import statistics
import math

tp=[31000. , 59000. , 178000. , 292000. , 414000.] # end-time of each exposure in seconds

# load ascii data (cut from 10 June 2013)

filename1=('lc_0310keV.txt')    # Full band
filename2=('lc_031keV.txt')     # Soft
filename3=('lc_15keV.txt')      # Hard

t0,r0,e0=np.loadtxt(filename1, usecols=(0,1,2), unpack=True)    # Full band
ts,rs,es=np.loadtxt(filename2, usecols=(0,1,2), unpack=True)    # Soft
th,rh,eh=np.loadtxt(filename3, usecols=(0,1,2), unpack=True)    # Hard

# AND PLOT lightcurve!

fig1=plt.figure(1)
frame1=fig1.add_axes((0.1,.4,0.875,.575))

plt.errorbar(t0-min(t0), r0, yerr=e0, linewidth=0.5, ecolor="black")

plt.ylabel('Rate (c/s)')
#plt.xlabel('Time (s)')
plt.ylim([0.4,2.25])
plt.xlim([0.0,4.15e5])

frame1.set_xticklabels([]) #Remove x-tic labels for the first frame

for i in range(0,4):
	rate_new=[0.0,2.25]
	time_edit=tp[i]
	time_new=[time_edit,time_edit]
	plt.plot(time_new,rate_new, color='black', linewidth=1.0, linestyle=':')

# and plot Second panel for Hardness ratio

frame2=fig1.add_axes((.1,.1,0.875,.3))

Hardness=rh/(rs+rh)

plt.errorbar(t0-min(t0), Hardness, yerr=eh/(rs+rh), linewidth=0.5, ecolor="black")

plt.ylabel('Hardness')
plt.xlabel('Time (s)')
plt.ylim([0.3,0.69])
plt.xlim([0.0,4.15e5])

for i in range(0,4):
	rate_new=[0.0,0.85]
	time_edit=tp[i]
	time_new=[time_edit,time_edit]
	plt.plot(time_new,rate_new, color='black', linewidth=1.0, linestyle=':')

plt.savefig('Overall_lc_HR.png')
plt.close('all')

