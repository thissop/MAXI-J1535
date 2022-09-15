import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd 
import numpy as np

plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

sns.set_context('paper')

save_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_one/'

# GRS 
fig, ax = plt.subplots(figsize=(6,2))
df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_dates.csv')
df = df.merge(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'), on='observation_ID')

x = np.array(df['MJD'])
y = np.array(df['A'])

ax.scatter(x,y, s=5, edgecolor='black', lw=0.2)
ax.set(xlabel='Time (MJD)', ylabel='Net Count Rate')

plt.savefig(f'{save_path}GRS_lightcurve.png', dpi=250)


# MAXI 

fig, ax = plt.subplots(figsize=(6, 2))

df = pd.read_csv(f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_dates.csv')
df = df.merge(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv'), on='observation_ID')

x, y = (np.array(df[i]) for i in ['MJD', 'B'])
ax.scatter(x,y, s=5, edgecolor='black', lw=0.2)
ax.set(xlabel='Time (MJD)', ylabel='Net Count Rate')


plt.savefig(f'{save_path}MAXI_lightcurve.png', dpi=250)
