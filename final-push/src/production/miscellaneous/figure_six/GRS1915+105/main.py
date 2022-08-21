import xspec
from xspec import * 
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl
import seaborn as sns 
import numpy as np
from qpoml.utilities import unprocess1d, lorentzian 

# SETUP #

#sns.set_style('ticks')
plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
#sns.set_style('darkgrid')
sns.set_context("paper", font_scale=0.6) #font_scale=
plt.rcParams['font.family'] = 'serif'
plt.rcParams["mathtext.fontset"] = "dejavuserif"

# XSPEC STUFF # 

os.chdir('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/50703-01-67-00/')
s = Spectrum('power_0_249.pha')
s.response = 'power_0_249.rmf'

m = Model("loren+loren", setPars={1:0, 4:0})

m.lorentz.LineE.frozen = True 
m.lorentz_2.LineE.frozen = True

s.ignore("**-0.5")

xspec.Fit.nIterations = 100
xspec.Fit.query = 'yes'
xspec.Fit.perform()
xspec.Fit.show()
cstat = xspec.Fit.statistic
dof = xspec.Fit.dof
chi2r = xspec.Fit.testStatistic/dof

Plot.xAxis = "keV"
Plot("ldata", "model")

data_x = Plot.x()
data_y = Plot.y()
data_xerr = Plot.xErr()
data_yerr = Plot.yErr()
model_y = Plot.model()

Plot.commands = ()
AllModels.clear()
AllData -= "*"

# RESULTS # 

qpo_preprocess_dictionary = {'frequency': ('normalize', 0.466, 6.229), 'width': ('normalize', 0.034, 0.924), 'rms': ('normalize', 3.637, 16.218)}

true = [0.36782925559604374,0.2749438202247191,0.8709482553056195]
predicted = [0.3670194179584083,0.2713332616821381,0.8429529949027209]

true_frequency = unprocess1d(np.array([true[0]]), qpo_preprocess_dictionary['frequency'])[0]
true_width = unprocess1d(np.array([true[1]]), qpo_preprocess_dictionary['width'])[0]
true_rms = unprocess1d(np.array([true[2]]), qpo_preprocess_dictionary['rms'])[0]
true_mask = np.logical_and(data_x>0.6*true_frequency, data_x<1.4*true_frequency)
true_x = np.array(data_x)[true_mask]
true_y = lorentzian(true_x, true_frequency, true_width, true_rms)

predicted_frequency = unprocess1d(np.array([predicted[0]]), qpo_preprocess_dictionary['frequency'])[0]
predicted_width = unprocess1d(np.array([predicted[1]]), qpo_preprocess_dictionary['width'])[0]
predicted_rms = unprocess1d(np.array([predicted[2]]), qpo_preprocess_dictionary['rms'])[0]
predicted_mask = np.logical_and(data_x>0.6*predicted_frequency, data_x<1.4*predicted_frequency)
predicted_x = np.array(data_x)[predicted_mask]
predicted_y = lorentzian(predicted_x, predicted_frequency, predicted_width, predicted_rms)

true_y = true_y+np.array(model_y)[true_mask]
predicted_y = predicted_y+np.array(model_y)[predicted_mask]

# MATPLOTLIB PLOT # 

fig, ax = plt.subplots()

ax.scatter(data_x, data_y, s=3)
ax.plot(true_x, true_y, label='True')
ax.plot(predicted_x, predicted_y, ls='--', label='Predicted')
ax.legend()

ax.set(xlim=(1.5,6), xlabel='Frequency (Hz)', ylabel='Power')

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_six/GRS1915+105/second_plot.pdf')