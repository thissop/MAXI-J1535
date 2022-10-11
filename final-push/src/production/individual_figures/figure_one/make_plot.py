import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd 
import numpy as np

plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')

sns.set_context('paper')

save_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_1/'

# GRS 
fig, ax = plt.subplots(figsize=(6,2))
df = pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[dates].csv')
df = df.merge(pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'), on='observation_ID')

x = np.array(df['MJD'])
y = np.array(df['A'])

ax.scatter(x,y, s=5, edgecolor='black', lw=0.2)
ax.set(xlabel='Time (MJD)', ylabel='Net Count Rate')

plt.savefig(f'{save_path}GRS_lightcurve.png', dpi=250)
plt.savefig(f'{save_path}GRS_lightcurve.pdf')

# MAXI 

fig, ax = plt.subplots(figsize=(6, 2))

df = pd.read_csv(f'/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[dates].csv')
df = df.merge(pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv'), on='observation_ID')

x, y = (np.array(df[i]) for i in ['MJD', 'A'])
ax.scatter(x,y, s=5, edgecolor='black', lw=0.2)
ax.set(xlabel='Time (MJD)', ylabel='Net Count Rate')


plt.savefig(f'{save_path}MAXI_lightcurve.png', dpi=250)
plt.savefig(f'{save_path}MAXI_lightcurve.pdf')