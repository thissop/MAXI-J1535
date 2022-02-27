#cSpell: disable

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tqdm import tqdm 
from scipy.signal import find_peaks

plt.style.use(r"C:\Users\Research\Documents\GitHub\sunnyhills\other\aesthetics\science.mplstyle")
plt.rcParams.update({'font.size': 8})
data_dir = './code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw'
pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
plot_dir = './code/xspec_related/qpo_routines/make_vetting_plots/plots'

all_ids = list(pd.read_csv('./code/xspec_related/good_ids.csv')['full_id'])

def loren(E, EL, σ, K):
    return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

for full_id in tqdm(all_ids): # when no printing do tqdm  
    #full_id = '1050360104_5' # fix this LOL 
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    image_data = data_dir+'/'+full_id+'_plot-data.csv'
    image_data = pd.read_csv(image_data)

    x = np.array(image_data['x'])
    y = np.array(image_data['y'])
    xerr = np.array(image_data['xerr'])
    yerr = np.array(image_data['yerr'])

    # brute force information
    df = pd.read_csv('./code/xspec_related/qpo_routines/jan-1-2022/final_logs/'+full_id+'.csv')

    freqs = np.array(df['freq'])
    norms = np.array(df['norm'])
    redchis = np.array(df['redchi'])
    widths = np.array(df['fwhm'])
    fit_stats = np.array(df['fit_stat'])
    min_freq, max_freq = np.min(freqs), np.max(freqs)

    # Rec chi. "peaks" aka valleys
    neg_fit_stats = -1*fit_stats
    min_height = np.min(neg_fit_stats)+14
    initial_peak_indices, _ = find_peaks(neg_fit_stats, height=min_height)
    canidate_peaks_mask = np.logical_or(freqs[initial_peak_indices]>1.2, freqs[initial_peak_indices]<0.8) # originally 0.9-1.1 ? 

    canidate_peak_indices = initial_peak_indices[canidate_peaks_mask]
    canidate_freqs = freqs[canidate_peak_indices]
    canidate_chis = fit_stats[canidate_peak_indices]
    canidate_widths = widths[canidate_peak_indices]
    canidate_norms = norms[canidate_peak_indices]

    canidate_rms_powers = [y[np.argmin(np.abs(x - freq))] for freq in canidate_freqs] # fundamental is chosen as maximum rms power peak 

    fundamental_index = np.argmax(canidate_rms_powers)
    fundamental_freq = canidate_freqs[fundamental_index]

    harmonic_statuses = []

    # Evaluate harmonic statuses 
    for canidate_index, canidate in enumerate(canidate_freqs): # within 2% !! 
        if canidate_index!=fundamental_index: 
            not_harmonic = True 
            for n in range(2,5): 
                harmonic = n*fundamental_freq
                subharmonic = fundamental_freq/n

                if canidate/harmonic < 1.02 and canidate/harmonic > 0.98: 
                    harmonic_statuses.append('h') # for harmonic (isn't this technicall the "second harmonic")
                    is_harmonic = False
                    break

                elif canidate/subharmonic < 1.02 and canidate/subharmonic > 0.98:
                    harmonic_statuses.append('s') # for sub-harmonic
                    is_harmonic = False
                    break

            if not_harmonic: 
                harmonic_statuses.append('n') # for "N"-ot harmonic
        
        else: 
            harmonic_statuses.append('f') # for fundamental, of course 

    ### MAKE PLOT ###
    fig = plt.figure(constrained_layout=True, figsize=(7,4))
    mosaic = """
        AB
        CD
        EF
        """
    ax_dict = fig.subplot_mosaic(mosaic)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for ax_str in ['C','D']: 
        ax = ax_dict[ax_str]
        ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
        ax.set_ylim(bottom=10**-5)

    for ax_str in ['A','B','C','D']: 
        ax = ax_dict[ax_str]
        ax.set(xlim=(0.1,20), xscale='log', yscale='log', xlabel='Frequency [Hz]')
        ax.axvspan(0.8,1.2, color='red', alpha=0.15, zorder=1)
    
    # Fit Stats
    
    ax = ax_dict['A']
    
    ax.scatter(freqs, fit_stats, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    ax.hlines(y=np.max(fit_stats)-14, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}10$', color='black', ls='--')
    ax.hlines(y=np.max(fit_stats)-24, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}20$', color='black', ls='--')
    ax.scatter(freqs[canidate_peak_indices], fit_stats[canidate_peak_indices], color='C1', marker='x', s=20)
    
    ax.set_ylabel('Fit Statistic')

    ax = ax_dict['B']

    ax.scatter(freqs, norms, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    ax.set_ylabel('Norm.')
    
    min_norm, sigma_norm = np.min(norms), np.std(norms)
    
    ax.hlines(y=min_norm+sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+1\sigma$')
    ax.hlines(y=min_norm+2*sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+2\sigma$')
    
    for ax in [ax_dict['A'], ax_dict['B']]:
        ax.legend(loc='upper left', fontsize='x-small')

    # D --> best fit models 
    # loren(E, EL, σ, K):
    
    ax = ax_dict['D']

    ax.plot(image_data.e, image_data.total)

    for canidate_index in range(len(canidate_widths)): 
        canidate_freq = canidate_freqs[canidate_index]
        canidate_width = canidate_widths[canidate_index]
        canidate_norm = canidate_norms[canidate_index]
        x_range = np.linspace(0.85*canidate_freq, 1.15*canidate_freq, 50)

        y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

        ax.plot(x_range, y_loren, color='orange', lw=1)

    for canidate in np.delete(canidate_freqs, fundamental_index): # within 1% !! 
        for n in range(2,4): 
            harmonic = n*fundamental_freq
            subharmonic = fundamental_freq/n

            ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
            ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green')
        
    # Annotations Info


    ax = ax_dict['E']
    ax.axis('off')
    ax.set(title='Detected QPO Frequencies')

    str_freqs = ['Freq: '+str(round(i,3)) for i in canidate_freqs]

    for counter, str_freq in enumerate(str_freqs): 
        harmonic_status = harmonic_statuses[counter]
        if harmonic_status == 's': 
            str_freqs[counter] = str_freq+'; subharmonic'

        elif harmonic_status == 'h': 
            str_freqs[counter] = str_freq+'; harmonic'

        elif harmonic_status == 'f': 
            str_freqs[counter] = str_freq+'; fundamental'

        else: 
            str_freqs[counter] = str_freq+'; not harmonic or fundamental'

    freqs_str = '\n'.join(str_freqs)

    ax.text(0., 0.25, freqs_str)

    ax = ax_dict['F']
    ax.axis('off')
  
    plt.show()
    plot_path = plot_dir + '/'+full_id+'.png'
    #plt.savefig(plot_path,bbox_inches='tight', dpi=150)

    plt.clf()
    plt.close()
    
    #break

'''

### from the model plotting part ###

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df.e, df.total, color='red',label='Total model',linewidth=3)
for j in range(ncomp):
    ax.plot(df.e, df[f'model{j}'],label=f'{m1.componentNames[j]}')

ax.set_xlabel('Energy (keV)')
ax.set_ylabel(r'counts/s/keV')
ax.set_xscale("linear")
ax.set_yscale("linear")
ax.legend()
ax.set(xlim=(0.1,20))
'''