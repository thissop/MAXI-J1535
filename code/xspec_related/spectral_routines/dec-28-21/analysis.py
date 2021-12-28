def pairplot(results_file, ids_file, redpg_range, plot_path):
    # Import(s)
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # Action
    df = pd.read_csv(results_file)
    df = df.dropna()
    
    red_pgs = np.array(df['red_pgs'])
    
    good_idx = np.intersect1d(np.where(red_pgs<redpg_range[1]), 
                                       np.where(red_pgs>redpg_range[0]))
        
    df = df.iloc[good_idx]
    
    df = df.merge(pd.read_csv(ids_file), on='ids')
    
    ratios = np.array(df['hardness_ratios'])
    ratios_mask = np.intersect1d(np.where(ratios<1), np.where(ratios>0))
    
    df = df.iloc[ratios_mask]
    
    param_names = ['log10_net_count_rates', 'hardness_ratios',
                   'tins', 'log10_diskbb_norms', 'gammas']
    
    df['log10_diskbb_norms'] = np.log10(df['diskbb_norms'])
    df['log10_net_count_rates'] = np.log10(df['net_count_rates'])
                   
    # Make pairplot
    plt.rcParams['font.family']='serif'
    plt.style.use('ggplot')
    plt.rc('font', size=4)
    
    fig, axs = plt.subplots(len(param_names), len(param_names), 
                            figsize=(14, 14))
                            
    for param_name_x, row_idx in zip(param_names, range(6)): 
        x = df[param_name_x]
        for param_name_y, col_idx in zip(param_names, range(6)): 
            y = df[param_name_y]
            
            if param_name_x != param_name_y:
                axs[row_idx, col_idx].scatter(x, y, marker='.')
                axs[row_idx, col_idx].set(xlabel=param_name_x, ylabel=param_name_y)
            
            else: 
                axs[row_idx, col_idx].hist(x)
                axs[row_idx, col_idx].set(xlabel=param_name_x, ylabel='Frequency')
    
    #plt.tight_layout()
    plt.subplots_adjust(hspace=0.6, wspace=0.5)
    plt.show()
    #plt.savefig(plot_path, dpi=500)


results_file = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored/results.csv'    
plot_path = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored/pairplot.png'
ids_file = '/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/final_ids.csv'
pairplot(results_file, ids_file, [0.95, 1.5], plot_path)
    
    