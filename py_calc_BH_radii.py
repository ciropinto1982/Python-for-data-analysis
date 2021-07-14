# PYTHON scripts to calculate black hole radii and wind propertiesd

import numpy as np
import math

# Definying constants: for stellar mass BH

c=3.0e10                      # cm s**-1
G=6.674e-8                    # cm**3 g**−1 s**−2
Msun=1.989e+33                # solar mass in grams
pi=math.pi                    # greek pi
sT=6.65e-25                   # Thomson cross-sec cm2
cs=1e6                        # sound speed cm/s
ne=1e20                       # electron-density in cm-3
nw=1e14                       # wind-density in cm-3
xi=10**4.3                    # wind ionisation parameter
Lb=1e40                       # Bolometric luminosity
AU=150.*1e6*1e5               # Astronomical Unit in cm
mdot=10                       # Mdot in Eddington units
M=10*Msun                     # Adopting 10Msun BH

# Definying / reading results: example variability timescales

nu=[7e-4,2e-4,1e-4]           # Frequencies in Hz
nu=np.array(nu)
dt=1/nu                       # Timescales

# Definying constants: for a supermassive black hole

M=2e6*Msun                    # Mass of SMBH
dt=1e3                        # Timescale in seconds
RS=2.*G*M/(c**2.)             # Schwarzschild radius = 5.9e11 cm
v=0.15                        # wind speed in c
vdisp=10000.*1e5              # wind vel dispersion in cm/s
Lb=1e44                       # Bolometric luminosity
nw=1e14                       # wind-density in cm-3
xi=10**4.3                    # wind ionisation parameter
NH=0.26e23                    # wind column density in cm^-2

# Calculating radii (Keplerian, Schwarz., Spherisat.)

RT = dt*c                                # Travelling distance

RS = 2.*G*M/(c**2.)                      # Schwarzschild

RG = 1.*G*M/(c**2.)                      # Gravitational

RI = 3*RS                                # Inner radius

RK = G*M/(vdisp**2)                      # kepler law

#RK=((G*M)/(4.*(pi**2.))*(dt**2.))**(1./3.) # Kepler

#print("{:.2e}".format(RG))
#print("{:.2e}".format(RS/RG))
print("{:.2e}".format(RT/RG))
print("{:.2e}".format(RK/RG))

#for i in range(len(dt)):
#    print("{:.2e}".format(RK[i]/RG))

RC=np.sqrt(c*dt/(sT*ne))                # Compton scattering

#for i in range(len(dt)):
#    print("{:.2e}".format(RC[i]))

Rw=np.sqrt(Lb/(xi*nw))                 # Wind radius

print("{:.2e}".format(Rw/RG))

R_sph=5/3*mdot*RI                     # Spheris radius

#print("{:.2e}".format(R_sph))
