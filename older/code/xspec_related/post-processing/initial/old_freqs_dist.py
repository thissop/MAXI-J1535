import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.family']='serif'
plt.rcParams["mathtext.fontset"] = 'cm'

df = pd.read_csv('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/data/processed/fixed_merged.csv?token=GHSAT0AAAAAABP54PQODGXCA4HY4XBWECH4YPMUCAA')
freqs_1 = np.array(df['first_par1s'])
freqs_2 = np.array(df['second_par1s'])
freqs_3 = np.array(df['third_par1s'])

fig, axs = plt.subplots(1,2, figsize=(6,3))

combined_freqs = np.concatenate((freqs_1, freqs_2, freqs_3))
mask = combined_freqs!=0
combined_freqs = combined_freqs[mask]

axs[0].hist(combined_freqs)
axs[0].set(ylabel='Count')

axs[1].boxplot(combined_freqs, vert=False)
axs[1].set_yticks([])

for ax in [0,1]: 
    axs[ax].minorticks_on()
    axs[ax].set(xlabel='Frequency [hz]')

plt.suptitle('Min: '+str(min(combined_freqs)))

plt.savefig(r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\xspec_related\post-processing\initial\old_freqs_dist.png', bbox_inches='tight')