#spell-checker: disable

## QPO Finder 

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








## Plotting functions

def make_vetting_plot(
    full_id:str, 
    image_df_dir: str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', # I usually zip this dirs when saving to GitHub
    qpo_df_dir: str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs', 
    canidates_dict: float={}, 
    annotations_dict: str={},
    plot_dir: str='none',  
    ignore_range: float=[0.8,1.2]):

    """
    Args: 
        annotations_dict: two item dictionary; first array should be initial algorithmic annotations; second array should be human annotations
        ignore_range: inclusive range of frequencies in which peak detection should be excluded from. Default is [0.8-1.2]
    
    Returns: 
    """

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

    canidate_labels = ['num_qpos', 'canidate_freqs', 'canidate_chis', 'canidate_widths', 'canidate_norms']
    (num_qpos, peak_freqs, peak_chis, peak_widths, peak_norms) = (np.array(canidates_dict[i]) for i in canidate_labels)
    fundamental_index = canidates_dict['fundamental_index']

    if len(annotations_dict)>0: 

        fig = plt.figure(constrained_layout=True, figsize=(7,4))
        mosaic = """
            AB
            CD
            EF
            """

        ax_dict = fig.subplot_mosaic(mosaic)

        for ax_str in ["E", "F"]: 
            ax_dict[ax_str].axis('off')

    else: 
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
    ax.scatter(peak_freqs, peak_chis, color='C1', marker='x', s=20)
    
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

    ax.plot(image_df.e, image_df.total)

    def loren(E, EL, σ, K):
        return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

    if num_qpos>0: 
        for canidate_index in range(len(peak_widths)): 
            canidate_freq = peak_freqs[canidate_index]
            canidate_width = peak_widths[canidate_index]
            canidate_norm = peak_norms[canidate_index]
            x_range = np.linspace(0.85*canidate_freq, 1.15*canidate_freq, 50)

            y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

            ax.plot(x_range, y_loren, color='orange', lw=1)

        fundamental_freq = peak_freqs[fundamental_index]
        for n in range(2,5): 
            harmonic = n*fundamental_freq
            subharmonic = fundamental_freq/n

            ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
            ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green')
        
    # Annotations Info
    if len(annotations_dict)>0: 

        annotations_key = list(annotations_dict.keys())
        annotations_values = list(annotations_dict.values())

        ax = ax_dict['E']
        ax.set(title='Detected QPO Frequencies')

        if annotations_values[0] != [-1]: 
            freqs_str = '\n'.join(annotations_dict[annotations_key[0]])

            ax.text(0., 0.25, freqs_str)

        ax = ax_dict['F']

        if len(annotations_dict)>1: 
            #thoughts_str = '\n'.join(annotations_dict[annotations_key[1]])
            thoughts_str = '' # fix for later 
            ax.text(0., 0.25, thoughts_str)

            
  
    if plot_dir != 'none': 
        plot_path = plot_dir + '/'+full_id+'.png'
        plt.savefig(plot_path,bbox_inches='tight', dpi=150)

    else: 
        plt.show()

    plt.clf()
    plt.close()


### not really long term functions 

def initial_pass(
    #key_df:str=r'code\xspec_related\good_ids.csv',
    outfile:str=r'code\xspec_related\better-organization\analysis-routines\qpo_data_aggregation\results\pre-steiner-compiled.csv',
    prelim_results:str=r'code\xspec_related\better-organization\analysis-routines\qpo_data_aggregation\results\prelim_vetting_classes.csv',
    image_df_dir:str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', 
    data_dir:str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs'): 

    import pandas as pd
    import numpy as np

    out_cols = ['full_id', 'num_qpos']

    for qpo_order in ['first', 'second', 'third']: 
        for val in ['freq', 'width', 'norm', 'rms_power']: 
            out_cols.append(qpo_order+'_'+val)

    col_str = ','.join(out_cols)+',fundamental_index'

    with open(outfile, 'w') as f: 
        f.write(col_str+'\n')

    #full_ids = pd.read_csv(key_df)['full_id']

    prelim_df = pd.read_csv(prelim_results)

    full_ids = prelim_df['full_id']
    prelim_classes = prelim_df['comment']

    index_counter = 0
    for full_id, comment in zip(full_ids, prelim_classes):
        canidates_dict, annotations_dict = hunter(full_id)
        
        freqs = canidates_dict['canidate_freqs']
        widths = canidates_dict['canidate_widths']
        norms = canidates_dict['canidate_norms']
        rms_powers = canidates_dict['canidate_rms_powers']

        num_qpos = canidates_dict['num_qpos']
        
        if comment == 'g': 
            # algo was able to detect the value 
            
            out_str = full_id + ',' + str(num_qpos)

            filler_str = ''
            for i in range(3-num_qpos): 
                filler_str += ',,,,' # starts with comma, doesn't end with comma
            
            for i in range(num_qpos): 
                temp_list = [freqs[i], widths[i], norms[i], rms_powers[i]]
                out_str += ','+','.join([str(item) for item in temp_list]) 
                 
            out_str += filler_str 

            out_str += ','+str(canidates_dict['fundamental_index'])

        elif comment == 'n': 
            num_qpos = 0
            out_str = full_id + ',' + str(num_qpos)

            filler_str = ''
            for i in range(3-num_qpos): 
                filler_str += ',,,,' # starts with comma, doesn't end with comma
            
            for i in range(num_qpos): 
                temp_list = [freqs[i], widths[i], norms[i], rms_powers[i]]
                out_str += ','+','.join([str(item) for item in temp_list]) 
                 
            out_str += filler_str 

            out_str += ',-1'

        elif '?' in comment:
            
            out_str = full_id + ',' +','.join(14*['flagged'])

        else: 
            
            print(full_id + ' prelim comment: '+comment)
            make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annotations_dict)
            
            qpos_to_keep_input = input('Enter QPO indices to keep: ')
            
            if qpos_to_keep_input!='skip':

                qpos_to_keep = [int(qpo_index) for qpo_index in qpos_to_keep_input.split(' ')] 
            
                fundamental_index = input(full_id + " fundamental_index: ")

                freqs,widths,norms,rms_powers = [np.array(prelim_list)[qpos_to_keep] for prelim_list in [freqs,widths,norms,rms_powers]] 

                adjusted_num_qpos = len(freqs)

                out_str = full_id + ',' + str(adjusted_num_qpos)

                filler_str = ''
                for i in range(3-adjusted_num_qpos): 
                    filler_str += ',,,,' # starts with comma, doesn't end with comma
                
                for i in range(adjusted_num_qpos): 
                    temp_list = [freqs[i], widths[i], norms[i], rms_powers[i]]
                    out_str += ','+','.join([str(item) for item in temp_list]) 
                    
                out_str += filler_str 

                out_str += ',' + fundamental_index

            else: # in case I have second thoughts and want to change it lol 
                out_str = full_id + ',' +','.join(14*['flagged'])
                
                new_comment = input(full_id+' new commment: ')
                
                prelim_classes[index_counter] = new_comment + '?'



        index_counter += 1
        with open(outfile, 'a') as f: 
                f.write(out_str+'\n')

    df = pd.DataFrame(list(zip(full_ids, prelim_classes)), columns=['full_id', 'comment'])
    df.to_csv(prelim_results, index=False) 
    
def reviewing_with_steiner(
    outfile:str=r'code\xspec_related\better-organization\analysis-routines\qpo_data_aggregation\results\discussion_with_steiner.csv',
    prelim_results:str=r'code\xspec_related\better-organization\analysis-routines\qpo_data_aggregation\results\prelim_vetting_classes.csv',
    image_df_dir:str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', 
    data_dir:str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs'):

    import pandas as pd
    import numpy as np

    with open(outfile, 'w') as f: 
        f.write('full_id,updated_comment'+'\n')

    prelim_df = pd.read_csv(prelim_results)

    review_ids = prelim_df['full_id']
    prelim_classes = prelim_df['comment']


    index_counter = 0
    for full_id, comment in zip(review_ids, prelim_classes):
        if '?' in comment: 
            canidates_dict, annotations_dict = hunter(full_id)

            print(f'{full_id}; initial comment: {comment}')
            make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annotations_dict)
            new_comment = input(f'{full_id}; new comment: ').replace(',',' ')
            with open(outfile, 'a') as f: 
                f.write(f'{full_id},{new_comment}\n')







## MISC. ##

def print_classes(): 
    dict = {'g':'\'G\'ood, as in stick to default', 
            'n':'no qpos in PDS',
            '?':'if ? in class, go over it with Dr. Steiner'}

    print(dict)