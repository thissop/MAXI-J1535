#cSpell: disable 

def quick_plot(full_id: str, 
               canidates_dict= {},
               image_df_dir: str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', # I usually zip this dirs when saving to GitHub
               qpo_df_dir: str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs', 
               plot_dir: str='none',  
               ignore_range: float=[0.8,1.2], 
               message: str = 'none'):

    '''IMPORTS'''
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    # get arrays

    plt.style.use(r"C:\Users\Research\Documents\GitHub\sunnyhills\other\aesthetics\science.mplstyle")
    plt.rcParams.update({'font.size': 8})

    image_df = pd.read_csv(image_df_dir + '/' + full_id + '_plot-data.csv')
    (x,y,xerr,yerr) = (np.array(image_df[i]) for i in ['x', 'y', 'xerr', 'yerr'])

    fitted_labels = ['freq', 'norm', 'fwhm', 'fit_stat']
    qpo_df = pd.read_csv(qpo_df_dir +'/'+full_id+'.csv')
    (freqs, norms, widths, fit_stats) = (np.array(qpo_df[i]) for i in fitted_labels)

    min_freq, max_freq = np.min(freqs), np.max(freqs)


    if len(canidates_dict.keys())>0: 
        canidate_labels = ['num_qpos', 'canidate_freqs', 'canidate_widths', 'canidate_norms']
        (num_qpos, peak_freqs, peak_widths, peak_norms) = (np.array(canidates_dict[i]) for i in canidate_labels)
        fundamental_index = canidates_dict['fundamental_index']

    fig = plt.figure(constrained_layout=True, figsize=(7,4))
    mosaic = """
        AB
        CD
        """

    ax_dict = fig.subplot_mosaic(mosaic)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for ax_str in ['A', 'B', 'C', 'D']: 
        ax = ax_dict[ax_str]
        ax.set(xlim=(0.1,20), xscale='log', yscale='log', xlabel='Frequency [Hz]')
        ax.axvspan(ignore_range[0],ignore_range[1], color='red', alpha=0.15, zorder=1)

        if ax_str == 'C' or ax_str == 'D':
            ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
            ax.set_ylim(bottom=10**-5)


    # Fit Stats
    
    ax = ax_dict['A']
    
    ax.scatter(freqs, fit_stats, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    ax.hlines(y=np.max(fit_stats)-14, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}10$', color='black', ls='--')
    ax.hlines(y=np.max(fit_stats)-24, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}20$', color='black', ls='--')
    
    if len(canidates_dict.keys())>0: 
        ax.vlines(peak_freqs, ymin=0.9, ymax=1, color='C1')
    
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

    continuum_x = np.array(image_df.e)
    continuum_y = np.array(image_df.total)

    ax.plot(continuum_x, continuum_y)

    def loren(E, EL, σ, K):
        return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

    if len(canidates_dict.keys())>0: 
        if num_qpos>0: 
            for canidate_index in range(len(peak_widths)): 
                canidate_freq = peak_freqs[canidate_index]
                canidate_width = peak_widths[canidate_index]
                canidate_norm = peak_norms[canidate_index]
                x_low = 0.85*canidate_freq
                x_high = 1.15*canidate_freq

                x_range = np.linspace(x_low, x_high, 50)

                y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

                ax.plot(x_range, y_loren, color='orange', lw=1, ls='--')
                
                continuum_mask = np.logical_and(continuum_x>x_low*0.75, continuum_x<x_high*1.25)
                x_range_total = continuum_x[continuum_mask]
                total_y = loren(x_range_total, canidate_freq, canidate_width, canidate_norm) + continuum_y[continuum_mask]

                ax.plot(x_range_total, total_y, color='orange', lw=1)
            
            if fundamental_index != -1: 
                fundamental_freq = peak_freqs[fundamental_index]
                for n in range(2,5): 
                    harmonic = n*fundamental_freq
                    subharmonic = fundamental_freq/n

                    ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
                    ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green')         
    
    if message!='none': 
        plt.suptitle(message)

    if plot_dir != 'none': 
        plot_path = plot_dir + '/'+full_id+'.png'
        plt.savefig(plot_path,bbox_inches='tight', dpi=150)

    else: 
        plt.show()

    plt.clf()
    plt.close()

'''
canidates_dict = {'num_qpos':2, 'canidate_freqs':[7.45000, 1.48515], 
                  'canidate_widths':[1.5, 0.409873], 
                  'canidate_norms':[3.53001E-04, 3.22288E-04],
                  'fundamental_index':-1}

full_id='1050360113_0'

import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/xspec_related/better-organization/analysis-routines/qpo_data_aggregation/results/discussion_with_steiner.csv')
ids = np.array(df['full_id'])
classes = np.array(df['updated_comment'])

for full_id, classification in zip(ids, classes): 
    message = full_id + ': '+classification
    quick_plot(full_id=full_id, message=message)

'''

def hunter(
    full_id:str,
    image_df_dir:str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', 
    data_dir:str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs'): 
    
    import numpy as np
    import pandas as pd
    from scipy.signal import find_peaks
    
    image_df = pd.read_csv(image_df_dir + '/' + full_id + '_plot-data.csv') 
    (x,y) = (np.array(image_df[i]) for i in ['x', 'y'])

    df = pd.read_csv(data_dir+'/'+full_id+'.csv')

    freqs = np.array(df['freq'])
    norms = np.array(df['norm'])
    widths = np.array(df['fwhm'])
    fit_stats = np.array(df['fit_stat'])

    # Rec chi. "peaks" aka valleys
    neg_fit_stats = -1*fit_stats
    min_height = np.min(neg_fit_stats)+14
    initial_peak_indices, _ = find_peaks(neg_fit_stats, height=min_height)
    canidate_peaks_mask = np.logical_or(freqs[initial_peak_indices]>1.2, freqs[initial_peak_indices]<0.8) # originally 0.9-1.1 ? 

    canidate_peak_indices = initial_peak_indices[canidate_peaks_mask]

    num_qpos = len(canidate_peak_indices)

    if num_qpos > 0: 

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
                        not_harmonic = False
                        break

                    elif canidate/subharmonic < 1.02 and canidate/subharmonic > 0.98:
                        harmonic_statuses.append('s') # for sub-harmonic
                        not_harmonic = False
                        break

                if not_harmonic: 
                    harmonic_statuses.append('n') # for "N"-ot harmonic
            
            else: 
                harmonic_statuses.append('f') # for fundamental, of course 

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

    else: 
        fundamental_index = -1
        harmonic_statuses = [-1]
        str_freqs = [-1]

        canidate_peak_indices = [-1]
        canidate_freqs = [-1]
        canidate_chis = [-1]
        canidate_widths = [-1]
        canidate_norms = [-1]

        canidate_rms_powers = [-1] 

        fundamental_index = -1
        fundamental_freq = -1


    canidate_dict = {
                        'num_qpos':num_qpos, 
                        'canidate_indices':canidate_peak_indices, # indices correspond to the ~268 logarithmically spaced frequencies array used in xspec  
                        'canidate_freqs':canidate_freqs, 
                        'canidate_chis':canidate_chis,
                        'canidate_widths':canidate_widths, 
                        'canidate_norms':canidate_norms, 
                        'canidate_rms_powers':canidate_rms_powers, 
                        'fundamental_index':fundamental_index}

    labels_dict = {'harmonic_status':harmonic_statuses, 
                   'canidate_labels':str_freqs}

    return canidate_dict, labels_dict