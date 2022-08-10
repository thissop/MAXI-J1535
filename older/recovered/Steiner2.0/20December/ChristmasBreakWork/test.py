#Imports
#import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Action
df = pd.read_csv('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/temp_vs_lumin.csv')

tins = np.array(df['Temp (keV)'])
cfluxes = np.array(df['Luminosity (log10Flux: erg/cm^{2}/s'])


b_const = (1380649/16021766340) #Boltzman const in $eV \cdot K^{-1}$
tin_temps = 1000*(1/(b_const*tins)) #Checked this with David Cohen's website which states $1 keV \approx 11.6 \cdot 10^{6} K$

#Plot
plt.scatter((tin_temps**4),cfluxes,color='indianred',s=3)
plt.xlabel(r'$\rm{[DiskTemp. (K)]}^{4}$')
plt.ylabel('log10Flux')
plt.yscale('symlog')
plt.xscale('log')
plt.show()




