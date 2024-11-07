##############################################################
###### Compute accuracy on bulk and velocity broadening ######
##############################################################

import numpy as np

##############################################################

sigma_v = 100  # units: km/s, intrinsic velocity broadening
sigma_g = 0.65 # units: eV, gain RMS variability (at 1 keV)
sigma_0 = 4    # units: eV, instrument resolution
E_0     = 7000 # units: eV, line centroid

N_l   = 100 # number of counts in the line
N_c   =  20 # number of counts in the continuum
N_b   =   5 # number of counts in the BKG

c     = 3e5 # units: km/s, speed of light

##############################################################

### 1) Computing accuracy on the bulk motions:

SNR   = N_l/(np.sqrt(N_l+N_c+N_b)) # S-to-N ratio

print("Signal to noise ratio", "{:.2f}".format(SNR))

dE_bulk_stat=sigma_0/SNR
dv_bulk_stat=sigma_0/SNR * c/E_0

print("Acc. bulk motion (eV)",  "{:.2f}".format(dE_bulk_stat))
print("Acc. bulk motion (km/s)","{:.2f}".format(dv_bulk_stat))

dv_bulk_sys=sigma_g * c/E_0

print("Sys. bulk motion (km/s)","{:.2f}".format(dv_bulk_sys))

dv_bulk_tot=np.sqrt(dv_bulk_stat**2 + dv_bulk_sys**2)

print("Tot. bulk motion (km/s)","{:.2f}".format(dv_bulk_tot))

### Note that the accuracy on the bulk motion can be improved
### comparing with lines from plasma likely at rest (e.g ISM)
#
#E_1=1010 # as an example E_0 of 2nd line is shifted by 10 eV
#S_1=5    # and the SNR ratio is assumed as 5
#
#dv_bulk_dif=c*sigma_0*np.sqrt(1/(E_0*SNR)**2+1/(E_1*S_1)**2)
#
#print("Dif. bulk motion (km/s)","{:.2f}".format(dv_bulk_dif))

### 2) Computing accuracy on the line broadening:

sigma_s = sigma_v / c * E_0 # conv km/s to eV at the centroid

ds_stat = (sigma_0**2+sigma_s**2) / (np.sqrt(2)*sigma_s*SNR)

dv_stat=ds_stat * c/E_0

print("Acc. broadening (eV)","{:.2f}".format(ds_stat))
print("Acc. broadening (km/s)","{:.2f}".format(dv_stat))

ds_sys = -1*sigma_s + np.sqrt(sigma_s**2+sigma_g**2)

dv_sys=ds_sys * c/E_0

print("Sys. broadening (eV)","{:.2f}".format(ds_sys))
print("Sys. broadening (eV)","{:.2f}".format(dv_sys))
