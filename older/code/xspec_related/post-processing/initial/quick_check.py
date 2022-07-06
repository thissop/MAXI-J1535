import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib.ticker as mticker
import matplotlib.image as mpimg
from scipy.signal import find_peaks

plt.rcParams['font.family']='serif'
plt.rcParams["mathtext.fontset"] = 'cm'

img = mpimg.imread(r'C:\Users\Research\Documents\GitHub\MAXI-J1535\documentation\archive\old_misc\Capturegauss.PNG') 

root_dir = r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\xspec_related\qpo_routines\jan-1-2022\final_logs\final_logs'

for i, file in enumerate(os.listdir(root_dir)): 
    if i == 1: 
        
        df = pd.read_csv(os.path.join(root_dir, file))
        freqs = np.array(df['freq'])
        norms = np.array(df['norm'])
        fitstats = np.array(df['fit_stat'])

        fig = plt.figure(figsize=(10,10))

        gs = fig.add_gridspec(5,2)
        ax1 = fig.add_subplot(gs[0:2, 0])
        ax2 = fig.add_subplot(gs[0:2, 1])
        ax3 = fig.add_subplot(gs[2:, :])
        
        '''
        for i in range(2): 
            axs[i].set(xscale='log', yscale='log', xlabel='Frequency [hz]')
            axs[i].tick_params(axis='both', which='both', direction='in')
            #axs[i].tick_params(axis='y', labelsize ='x-small')
            axs[i].xaxis.set_major_formatter(mticker.ScalarFormatter())
            axs[i].xaxis.set_minor_formatter(mticker.ScalarFormatter())
        '''    
      
        ax1.scatter(freqs, fitstats, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
        ax1.set(ylabel=r"$\chi^2$"+' Fit Statistic', yscale='log')
        ax1.yaxis.set_minor_formatter(mticker.ScalarFormatter())
        ax1.yaxis.set_major_formatter(mticker.ScalarFormatter())

        ax2.scatter(freqs, norms, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
        ax2.set(ylabel='Normalization')

        ax3.axis('off')
        ax3.imshow(img)

        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        plt.suptitle(file)

        min_freq, max_freq = np.min(freqs), np.max(freqs)
        
        # Find peaks
        
        # Rec chi. "peaks" aka valleys
        neg_fitstats = -1*fitstats
        min_height = np.min(neg_fitstats)+14
        chiPeakIndices, _ = find_peaks(neg_fitstats, height=min_height)
        chiPeakFreqs = freqs[chiPeakIndices]
        chiPeakIndices = chiPeakIndices[np.logical_or(chiPeakFreqs<0.9, chiPeakFreqs>1.1)] # was originally ignored betweeen 0.9-1.1 
   
        plt.rcParams['font.size']=6
        
        ax1.hlines(y=np.max(fitstats)-14, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}10$', color='black', ls='--')
        ax1.hlines(y=np.max(fitstats)-24, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}20$', color='black', ls='--')
        ax1.scatter(freqs[chiPeakIndices], fitstats[chiPeakIndices], color='C1', marker='x', s=20)
        
        min_norm, sigma_norm = np.min(norms), np.std(norms)
        
        ax2.hlines(y=min_norm+sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+1\sigma$')
        ax2.hlines(y=min_norm+2*sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+2\sigma$')
        
        for ax in [ax1, ax2]:
            ax.legend(fontsize=10)

        plt.savefig(r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\xspec_related\post-processing\initial\vetting_template.png', bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.close()

plt.show()