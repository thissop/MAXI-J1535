def plot_all(image_df_dir: str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', # I usually zip this dirs when saving to GitHub
             qpo_df_dir: str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs', 
             plot_dir: str='none',  
             ignore_range: float=[0.8,1.2], 
             qpo_results_csv: str = './data/processed/2022/new_current_qpos.csv'):

    '''IMPORTS'''
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from tqdm import tqdm 
    import os 

    # get arrays

    qpo_results_df = pd.read_csv(qpo_results_csv)

    quads = [i.replace('.png', '') for i in os.listdir('./code/xspec_related/qpo_routines/full_aggregation/plot_dists/quad-panels') if i!='.gitkeep']
    singles = [i.replace('.png', '') for i in os.listdir('./code/xspec_related/qpo_routines/full_aggregation/plot_dists/single-panels') if i!='.gitkeep']
    pretties = quads = [i.replace('.png', '') for i in os.listdir('./code/xspec_related/qpo_routines/full_aggregation/plot_dists/pretty-singles') if i!='.gitkeep']

    for i in tqdm(range(len(qpo_results_df.index))): 
        row = qpo_results_df.iloc[[i]]
        full_id = row['full_id'].item()
        
        if (full_id not in singles) or (full_id not in pretties) or (full_id not in quads):  
            print(full_id)
            con_class = int(row['confidence_class'].item())
            if con_class >=0: 
                num_qpos = int(row['num_qpos'].item())
            else: 
                num_qpos = 0

            plt.style.use(r"C:\Users\Research\Documents\GitHub\sunnyhills\other\aesthetics\science.mplstyle")
            plt.rcParams.update({'font.size': 8})

            image_df = pd.read_csv(image_df_dir + '/' + full_id + '_plot-data.csv')
            (x,y,xerr,yerr) = (np.array(image_df[i]) for i in ['x', 'y', 'xerr', 'yerr'])

            fitted_labels = ['freq', 'norm', 'fwhm', 'fit_stat']
            qpo_df = pd.read_csv(qpo_df_dir +'/'+full_id+'.csv')
            (freqs, norms, widths, fit_stats) = (np.array(qpo_df[i]) for i in fitted_labels)

            min_freq, max_freq = np.min(freqs), np.max(freqs)

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


            order = ['first_', 'second_', 'third_']
            canidate_freqs = []
            canidate_widths = []
            canidate_norms = []

            for i in range(num_qpos):
                canidate_freqs.append(row[order[i]+'freq'].item())
                canidate_widths.append(row[order[i]+'width'].item())
                canidate_norms.append(row[order[i]+'norm'].item())

            # Fit Stats
            
            ax = ax_dict['A']
            
            ax.scatter(freqs, fit_stats, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
            ax.hlines(y=np.max(fit_stats)-14, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}10$', color='black', ls='--')
            ax.hlines(y=np.max(fit_stats)-24, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}20$', color='black', ls='--')
            
            if num_qpos>0: 
                for frq in canidate_freqs: 
                    ax.axvline(frq, ymin=0.9, ymax=1, color='C7')
            
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

            if num_qpos>0 and con_class>=0: 
                for canidate_index in range(len(canidate_freqs)): 
                    canidate_freq = canidate_freqs[canidate_index]
                    canidate_width = canidate_widths[canidate_index]
                    canidate_norm = canidate_norms[canidate_index]
                    x_low = 0.85*canidate_freq
                    x_high = 1.15*canidate_freq

                    x_range = np.linspace(x_low, x_high, 50)

                    y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

                    ax.plot(x_range, y_loren, color='orange', lw=1, ls='--')
                    
                    continuum_mask = np.logical_and(continuum_x>x_low*0.75, continuum_x<x_high*1.25)
                    x_range_total = continuum_x[continuum_mask]
                    total_y = loren(x_range_total, canidate_freq, canidate_width, canidate_norm) + continuum_y[continuum_mask]

                    ax.plot(x_range_total, total_y, color='orange', lw=1)
                
                    fundamental_freq = canidate_freqs[0]
                    for n in range(2,5): 
                        harmonic = n*fundamental_freq
                        subharmonic = fundamental_freq/n

                        ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
                        ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green')         
            
            plt.suptitle(full_id+'; Confidence Class: '+str(con_class))

            if plot_dir != 'none': 
                plot_path = './code/xspec_related/qpo_routines/full_aggregation/plot_dists/quad-panels/'+full_id+'.png'
                plt.savefig(plot_path,bbox_inches='tight', dpi=150)

            #else: 
                #plt.show()
                
            plt.clf()
            plt.close()

            # only the neat plot

            fig, ax = plt.subplots(figsize=(3,2))

            ax.set(xscale='log', yscale='log', xlabel='Frequency [Hz]', ylabel='rms-Normalized Power')
            
            ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
            ax.set_ylim(bottom=10**-5)

            continuum_x = np.array(image_df.e)
            continuum_y = np.array(image_df.total)

            ax.plot(continuum_x, continuum_y)

            if num_qpos>0 and con_class>=0: 
                for canidate_index in range(len(canidate_freqs)): 
                    canidate_freq = canidate_freqs[canidate_index]
                    canidate_width = canidate_widths[canidate_index]
                    canidate_norm = canidate_norms[canidate_index]
                    x_low = 0.85*canidate_freq
                    x_high = 1.15*canidate_freq

                    x_range = np.linspace(x_low, x_high, 50)

                    y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

                    ax.plot(x_range, y_loren, color='orange', lw=1, ls='--')
                    
                    continuum_mask = np.logical_and(continuum_x>x_low*0.75, continuum_x<x_high*1.25)
                    x_range_total = continuum_x[continuum_mask]
                    total_y = loren(x_range_total, canidate_freq, canidate_width, canidate_norm) + continuum_y[continuum_mask]

                    ax.plot(x_range_total, total_y, color='orange', lw=1)
                
                    


            

            if plot_dir != 'none': 
                plt.suptitle(full_id)
                ax.set(xlim=(min(x),20))
                plot_path = './code/xspec_related/qpo_routines/full_aggregation/plot_dists/pretty-singles/'+full_id+'.png'
                
                
                plt.savefig(plot_path,bbox_inches='tight', dpi=150)

                xlim=(0.1,20)
                plt.suptitle(full_id+'; Confidence Class: '+str(con_class))
                if num_qpos>0 and con_class>=0: 
                    fundamental_freq = canidate_freqs[0]
                    for n in range(2,5): 
                        harmonic = n*fundamental_freq
                        subharmonic = fundamental_freq/n

                        ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
                        ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green') 
                ax.axvspan(ignore_range[0],ignore_range[1], color='red', alpha=0.15, zorder=1)
                plot_path = './code/xspec_related/qpo_routines/full_aggregation/plot_dists/single-panels/'+full_id+'.png'
                plt.savefig(plot_path,bbox_inches='tight', dpi=150)

            else: 
                plt.show()

            plt.clf()
            plt.close()


plot_all(plot_dir='save') 