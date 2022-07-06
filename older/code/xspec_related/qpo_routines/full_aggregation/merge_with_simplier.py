#cSpell: disable 

def merge_it_all(): 
    import pandas as pd
    import numpy as np
    import re

    from local_funcs import quick_plot, hunter

    df = pd.read_csv('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/xspec_related/better-organization/analysis-routines/qpo_data_aggregation/results/pre-steiner-compiled.csv')

    df = df.drop(columns=['fundamental_index'])

    flagged_mask = np.where(df['num_qpos']=='flagged')[0]

    zeroes = np.zeros(len(df.index)).astype(int)

    zeroes[flagged_mask] = -1

    df['confidence_class'] = zeroes 

    df = df.replace({'flagged': np.nan}, regex=True)

    full_ids = np.array(df['full_id'])

    steiner_df = pd.read_csv('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/xspec_related/better-organization/analysis-routines/qpo_data_aggregation/results/discussion_with_steiner.csv')
    steiner_ids = np.array(steiner_df['full_id'])
    steiner_comments = np.array(steiner_df['updated_comment'])

    for flagged_index in flagged_mask:
        full_id = full_ids[flagged_index]
        correct_answer = False

        canidates_dict, _ = hunter(full_id)

        steiner_index = np.where(steiner_ids == full_id)[0][0]
        comment = steiner_comments[steiner_index]

        quick_plot(full_id=full_id, canidates_dict=canidates_dict, message=comment) 

        while not correct_answer: 
            user_choice = input(full_id+": ")

            if user_choice == 'none': # return none for all features for that QPO 
                new_row = [full_id, 0] + 12*[np.nan] + [1]

                df.loc[flagged_index] = new_row 
                correct_answer=True
            
            elif user_choice == 'choose': 
                quick_plot(full_id=full_id, canidates_dict=canidates_dict, message=comment)
                qpos_to_keep = [int(i) for i in re.sub(' +', ' ', input('Enter QPO indices to keep: ')).split(' ')]

                num_qpos = len(qpos_to_keep)
                
                qpo_props = []

                for i in qpos_to_keep: # needs to be zero indexed! 
                    qpo_props.append(canidates_dict['canidate_freqs'][i])
                    qpo_props.append(canidates_dict['canidate_widths'][i])
                    qpo_props.append(canidates_dict['canidate_norms'][i])
                    qpo_props.append(canidates_dict['canidate_rms_powers'][i])

                new_row = [full_id, num_qpos] + qpo_props + ((3-num_qpos)*4)*[np.nan] + [1]

                df.loc[flagged_index] = new_row 
                correct_answer = True

            elif user_choice == 'skip': 
                correct_answer = True 

    df.to_csv('additions.csv', index=False)

#merge_it_all()

def make_quick_plots(current_df: str = './code/xspec_related/qpo_routines/full_aggregation/current_qpos.csv',
               image_df_dir: str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', # I usually zip this dirs when saving to GitHub
               plot_dir: str='./code/xspec_related/qpo_routines/full_aggregation/plot_dists'): 
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt 
    from tqdm import tqdm 

    current_df = pd.read_csv(current_df)

    full_ids = np.array(current_df['full_id'])
    current_mask = np.where(current_df['confidence_class']>-1)[0]

    first_freqs, second_freqs = (np.array(current_df[col]) for col in ['first_freq', 'second_freq'])
    first_widths, second_widths = (np.array(current_df[col]) for col in ['first_width', 'second_width'])
    first_norms, second_norms = (np.array(current_df[col]) for col in ['first_norm', 'second_norm'])

    for index in tqdm(current_mask):
        full_id = full_ids[index] 

        freqs = [first_freqs[index], second_freqs[index]]
        widths = [first_widths[index], second_widths[index]]
        norms = [first_norms[index], second_norms[index]]

        plt.style.use(r"C:\Users\Research\Documents\GitHub\sunnyhills\other\aesthetics\science.mplstyle")
        plt.rcParams.update({'font.size': 8})

        image_df = pd.read_csv(image_df_dir + '/' + full_id + '_plot-data.csv')
        (x,y,xerr,yerr) = (np.array(image_df[i]) for i in ['x', 'y', 'xerr', 'yerr'])

        fig, ax = plt.subplots(figsize=(4,2))

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ax.set(xlim=(0.1,20), xscale='log', yscale='log', xlabel='Frequency [Hz]')
        ax.axvspan(0.8,1.2, color='red', alpha=0.15, zorder=1)

        ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
        ax.set_ylim(bottom=10**-5)

        continuum_x = np.array(image_df.e)
        continuum_y = np.array(image_df.total)

        ax.plot(continuum_x, continuum_y)

        def loren(E, EL, σ, K):
            return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

        for canidate_index in range(2): 
            canidate_freq = freqs[canidate_index]
            canidate_width = widths[canidate_index]
            canidate_norm = norms[canidate_index]
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
            plot_path = plot_dir + '/'+full_id+'.png'
            plt.savefig(plot_path,bbox_inches='tight', dpi=150)

        else: 
            plt.show()

        plt.clf()
        plt.close()

make_quick_plots()