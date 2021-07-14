# PYTHON routine that reads results from a table and plot them
# It also fit different relationships (e.g. powerlaws)
# The example shown here applies to the luminosity-temperature trends
# of the cold and hot blackbody components in the spectral model

# Import libraries

import scipy.stats
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools

from scipy import optimize
from decimal import Decimal
from math import cos
from math import log
from math import sqrt
from matplotlib.pyplot import cm
from scipy.optimize import curve_fit
from matplotlib import pyplot
from scipy.odr import *

#--------Define function for fits--------------------

def powerlaw(p, x): # this is your 'straight line' y=f(x) for ODR
	A, B = p
	return A*(x**B)

def powerlaw0(p, x): # slope fixed == 0, i.e. constant
	A    = p
	return A*(x**0)

def powerlaw4(p, x): # slope fixed == 4
	B = p
	return B*(x**4)

def powerlaw2(p, x): # slope fixed == 2
	B = p
	return B*(x**2)

# --------get data-----------------------------------------------
#
# Provide a table with the best-fit values and uncertainties (lower, upper error)
# The script allow you to skip the first 2 rows if containing labels and header
# The parameters called here are the column density (NH), the temperature in keV and
# bolometric luminosities (1e-3 to 1e3 keV) and not just X-ray (0.3-10 keV) luminosity
# of each blackbody component, and finally (optional) the chi-squared value of the fit.

NH,NHe1,NHe2, T1,T1e1,T1e2, T2,T2e1,T2e2, L1,L1e1,L1e2, L2,L2e1,L2e2, chisq\
	=np.loadtxt('Table_of_results.txt', unpack=True, skiprows=2)

NH_err=(np.abs(NHe1)+np.abs(NHe2))/2.
T1_err=(np.abs(T1e1)+np.abs(T1e2))/2.
T2_err=(np.abs(T2e1)+np.abs(T2e2))/2.
L1_err=(np.abs(L1e1)+np.abs(L1e2))/2./1e39
L2_err=(np.abs(L2e1)+np.abs(L2e2))/2./1e39

L1=L1/1e39
L2=L2/1e39

T1=np.array(T1)
T2=np.array(T2)
L1_err=np.array(L1_err)
L2_err=np.array(L2_err)
T1_err=np.array(T1_err)
T2_err=np.array(T2_err)

# --------plot and fit data L1-T1 and L2-T2--------------------

fig = plt.figure(figsize=(7,5))
left, bottom, width, height = 0.1, 0.11, 0.85, 0.85
ax = fig.add_axes([left, bottom, width, height])

plt.scatter(T1, L1, color='blue'  ,label="BB$_{cold}$")
plt.scatter(T2, L2, color='orange',label="BB$_{hot}$")

plt.errorbar(T1, L1, yerr=L1_err, xerr=T1_err, marker='',color='blue',\
			 capsize=0, fmt='none',zorder=-1,ecolor='blue')
plt.errorbar(T2, L2, yerr=L2_err, xerr=T2_err, marker='',color='orange',\
			 capsize=0, fmt='none',zorder=-1,ecolor='orange')

plt.ylabel("$L_{BOL}$ ($10^{39}$ erg s$^{-1}$)", fontsize=15)
plt.xlabel("T (keV)", fontsize=15)
plt.xlim([0.1,5])
plt.ylim([0.5,12])
plt.xscale('log')
plt.yscale('log')

# -------- fit data L1-T1 --------------------

# Free slope

used_model = Model(powerlaw)
data = RealData(T1, L1, sx=T1_err, sy=L1_err)
odr = ODR(data, used_model, beta0=[1, -1])
out = odr.run()
out.pprint()
print("Const & Slope (T1L1 Int, Slope) ============> ", out.beta)
print("Const & Slope (T1L1 Uncertinty) ============> ", out.sd_beta)
x_line=np.arange(0.1, 1.8, 0.1)
y_line=out.beta[0]*(x_line**out.beta[1])
plt.plot(x_line,y_line,c='black',linestyle='-',label="L$\propto$T$^{\\alpha}$")

# Slope==0 (constant)

used_model = Model(powerlaw0)
data = RealData(T1, L1, sx=T1_err, sy=L1_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.1, 0.7, 0.1)
y_line=out.beta[0]*(x_line**0)
plt.plot(x_line, y_line, c='green', linestyle='-', label="L$\propto$T$^0$")

# Slope==2 (advected disk)

used_model = Model(powerlaw2)
data = RealData(T1, L1, sx=T1_err, sy=L1_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.1, 1.8, 0.1)
y_line=out.beta[0]*(x_line**2)
plt.plot(x_line, y_line, c='black', linestyle=':', label="L$\propto$T$^2$")

# Slope==4 (thin disk)

used_model = Model(powerlaw4)
data = RealData(T1, L1, sx=T1_err, sy=L1_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.1, 1.8, 0.1)
y_line=out.beta[0]*(x_line**4)
plt.plot(x_line,y_line,c='red',linestyle='-',label="L$\propto$T$^4$")

# Residual Variance: 0.901 slope = -3.86
# Residual Variance: 2.187 slope = 0
# Residual Variance: 1.857 slope = 2
# Residual Variance: 1.619 slope = 4

# -------- fit data L2-T2 --------------------

# Free slope

used_model = Model(powerlaw)
data = RealData(T2, L2, sx=T2_err, sy=L2_err)
odr = ODR(data, used_model, beta0=[1, 3.5])
out = odr.run()
out.pprint()
print("Const & Slope (T2L2 Int, Slope) ============> ", out.beta)
print("Const & Slope (T2L2 Uncertinty) ============> ", out.sd_beta)
x_line=np.arange(0.1, 12, 0.2)
y_line=out.beta[0]*(x_line**out.beta[1])
plt.plot(x_line, y_line, c='black', linestyle='-')

# Slope==0 (constant)

used_model = Model(powerlaw0)
data = RealData(T2, L2, sx=T2_err, sy=L2_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.6, 2.7, 0.1)
y_line=out.beta[0]*(x_line**0)
plt.plot(x_line, y_line, c='green', linestyle='-')

# Slope==2 (advected disk)

used_model = Model(powerlaw2)
data = RealData(T2, L2, sx=T2_err, sy=L2_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.1, 12, 0.2)
y_line=out.beta[0]*(x_line**2)
plt.plot(x_line, y_line, c='black', linestyle=':')

# Slope==4 (thin disk)

used_model = Model(powerlaw4)
data = RealData(T2, L2, sx=T2_err, sy=L2_err)
odr = ODR(data, used_model, beta0=[1])
out = odr.run()
out.pprint()
x_line=np.arange(0.1, 12, 0.2)
y_line=out.beta[0]*(x_line**4)
plt.plot(x_line, y_line, c='red', linestyle='-')

# Residual Variance:   2.143 slope = 3.0
# Residual Variance: 121.760 slope = 0
# Residual Variance:   3.213 slope = 2
# Residual Variance:   2.413 slope = 4

# -------- save plots PDF --------------------

plt.legend(loc='lower right', fontsize=12)

plt.savefig('plot_LT_BB12.pdf')
plt.close('all')

# -------- spearman and pearson coefficients --------------------

#print("L1-T1 HC spear =",scipy.stats.spearmanr(T1,L1)) # correlation=0.036, pvalue=0.855
#print("L2-T2 HC spear =",scipy.stats.spearmanr(T2,L2)) # correlation=0.296, pvalue=0.127
#print("L1-T1 HC pears =",scipy.stats.pearsonr(T1,L1))  # correlation=0.054, pvalue=0.785
#print("L2-T2 HC pears =",scipy.stats.pearsonr(T2,L2))  # correlation=0.239, pvalue=0.220

# -------- evaluate chi-sq goodness of fit Chi2 / y-errors ------

# compute chi^2/dof for a CONSTANT distribution (only y_errors)

N = len(L1)
mu = np.mean(L1)
z = (L1 - mu) / L1_err
chi2 = np.sum(z ** 2)
chi2dof = chi2 / (N - 1)

print("Chi2/d.o.f. (T1L1 CNST) = ", round(chi2dof,2))

N = len(L2)
mu = np.mean(L2)
z = (L2 - mu) / L2_err
chi2 = np.sum(z ** 2)
chi2dof = chi2 / (N - 1)

print("Chi2/d.o.f. (T2L2 CNST) = ", round(chi2dof,2))

# compute chi^2/dof for a POWERLAW distribution (only y_errors)

A=0.014 # Update these values from the best fit results
B=-3.86

L1_exp=A*(T1**B)

N = len(L1)
z = (L1 - L1_exp) / L1_err
chi2 = np.sum(z ** 2)
chi2dof = chi2 / (N - 2)

print("Chi2/d.o.f. (T1L1 POWf) = ", round(chi2dof,2))

A=2.33 # Update these values from the best fit results
B=2.99

L2_exp=A*(T2**B)

N = len(L2)
z = (L2 - L2_exp) / L2_err
chi2 = np.sum(z ** 2)
chi2dof = chi2 / (N - 2)

print("Chi2/d.o.f. (T2L2 POWf) = ", round(chi2dof,2))

