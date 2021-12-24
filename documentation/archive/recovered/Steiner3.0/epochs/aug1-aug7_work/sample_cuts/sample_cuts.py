def evaluate_cuts(key, data_dir, results_file):
    # Import(s)
    import os, shutil
    import numpy as np
    import pandas as pd
    from astropy.io import fits
    
    # Action
    
    ids = np.array(pd.read_csv(key)['ID'])
    
    bg_count_rates = np.array([])
    source_count_rates = np.array([])
    source_exposures = np.array([])
    source_bg_ratios = np.array([])
    source_counts_master = np.array([])
    
    for id in ids: 
        split_id = id.split('_')
        obsid = split_id[0]
        gti = split_id[1]
        
        data_file = data_dir + '/' + obsid + '/jspipe/js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
        bg_file = data_file.replace('.jsgrp', '.bg')
        
        orig_data_file = data_file
        temp_data_file = data_file.replace('.fits', '(temp).fits')
        temp_data_file = data_file.replace('.jsgrp', '(temp).fits')
        shutil.copyfile(orig_data_file, temp_data_file)
        data_hdul = fits.open(temp_data_file)
        counts_array = np.array(data_hdul[1].data['COUNTS'])
        exp_time = float(data_hdul[1].header['EXPOSURE'])
        channels_array = np.array(data_hdul[1].data['CHANNEL'])
        
        cr_mask = np.logical_and(channels_array>=50, channels_array<=999)
        
        orig_bg = bg_file
        temp_bg_file = bg_file.replace('.bg', '(temp).bg')
        shutil.copyfile(orig_bg, temp_bg_file)
        bg_hdul = fits.open(temp_bg_file)
        bg_counts_array = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        # Actual calculations 
        
        # Misc.
        source_exposures = np.append(source_exposures, exp_time)
        
        # Source counts and count rate
        source_counts = np.sum(counts_array[cr_mask])
        source_count_rate = source_counts/exp_time
        source_count_rates = np.append(source_count_rates, source_count_rate)
        source_counts_master = np.append(source_counts_master, source_counts)
        
        # Get background count rate, sum(bg counts where 10.0>keV>0.5)
        bg_counts = np.sum(bg_counts_array[cr_mask])
        bg_count_rate = bg_counts/bg_exp_time
        bg_count_rates = np.append(bg_count_rates, bg_count_rate)
        
        # (Source counts+background counts)/background counts = source background ratio
        source_bg_ratio = (bg_counts+source_counts)/bg_counts
        source_bg_ratios = np.append(source_bg_ratios, source_bg_ratio)
        
        os.remove(temp_data_file)
        os.remove(temp_bg_file)
        
    zipped = list(zip(ids, bg_count_rates, source_count_rates, 
                      source_exposures, source_bg_ratios, 
                      source_counts_master))   
                      
    out_df = pd.DataFrame(zipped, columns=['ids', 'bg_count_rates', 
                                                   'source_count_rates',  
                                                   'source_exposures', 
                                                   'source_bg_ratios',  
                                                   'source_counts_master'])
                                                   
    out_df.to_csv(results_file, index=False)

def count_sample(results_file, log_dir):
    # Import(s)
    import os, re
    import numpy as np
    import pandas as pd
    
    # Action 
    df = pd.read_csv(results_file)
    
    intitial_size = len(df.index)
    
    # Background Counts cut 
    bg_cr_mask = np.where(df['bg_count_rates']<5)
    df = df.iloc[bg_cr_mask]
    bg_cr_cut_size = len(df.index)
    
    # Ratios cut
    ratios_mask = np.where(df['source_bg_ratios']>=10)
    df = df.iloc[ratios_mask]
    ratios_cut_size = len(df.index)
    
    # Exposures cut
    exposures_mask = np.where(df['source_exposures']>=60)
    df = df.iloc[exposures_mask]
    exposures_cut_size = len(df.index)
    
    # 2000 source counts minimum 
    counts_mask = np.where(df['source_counts_master']>=2000)
    df = df.iloc[counts_mask]
    counts_2000_cut_size = len(df.index)
    
    # 5000 source counts minimum
    counts_mask = np.where(df['source_counts_master']>=5000)
    df = df.iloc[counts_mask]
    counts_5000_cut_size = len(df.index)
    
    
    # Find how many have fitted results with red. chi in good range
    log_files = np.array([
                          os.path.join(log_dir, 
                          file) for file in os.listdir(log_dir) if 'errorlog' not in file])
    
    log_ids = np.array([])
    red_pgs = np.array([])
    
    def split_line(line):
        return re.sub(' +', ',', line).split(',')
    
    for log_file in log_files: 
        seg_id = log_file.split('/')[-1].replace('.txt', '')
        log_ids = np.append(log_ids, seg_id)
        with open(log_file, 'r') as f:
            for line in f: 
                if '#Fit statistic  : PG-Statistic' in line: 
                    pg_stat = float(split_line(line)[4])
                    
                elif '#Test statistic : Chi-Squared' in line: 
                    dof = float(split_line(line)[4])
                    red_pg = pg_stat/dof
                    red_pgs = np.append(red_pgs, red_pg)
    
    log_zipped = list(zip(log_ids, red_pgs))                
    log_df = pd.DataFrame(log_zipped, columns=['ids', 'redpgstat'])
    redpg_mask = np.where(log_df['redpgstat']>0.9)
    redpg_mask = np.intersect1d(np.where(log_df['redpgstat']<2.0), redpg_mask)
    log_df = log_df.iloc[redpg_mask]
    
    merged_df = df.merge(log_df, on='ids')
    merged_size = len(merged_df.index)
    
    tighter_redpg_mask = np.intersect1d(np.where(log_df['redpgstat']>0.95), 
                                        np.where(log_df['redpgstat']<1.5))
    tighter_log_df = log_df.iloc[tighter_redpg_mask]
    tighter_merged_df = df.merge(tighter_log_df, on='ids')
    tighter_merge_size = len(tighter_merged_df.index)
    
    # Save ids
    final_ids = merged_df['ids']
    final_zipped = list(zip(final_ids))
    final_df = pd.DataFrame(final_zipped, columns=['ids'])
    final_df.to_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/final_ids.csv')
    
    merged_df.to_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/aftersamplecuts.csv')
    
    # Print Results
    print('   SAMPLE SIZE EVALUATION   ')
    print(30*'-')
    print('Initial Size    |    '+str(intitial_size))
    print(30*'-')
    print('After Cut #1:   |    '+str(bg_cr_cut_size))
    print(30*'-')
    print('After Cut #2:   |    '+str(ratios_cut_size))
    print(30*'-')
    print('After Cut #3:   |    '+str(exposures_cut_size))
    print(30*'-')
    print('After Cut #4:   |    '+str(counts_2000_cut_size))
    print(30*'-')
    print('After Cut #5:   |    '+str(counts_5000_cut_size))
    print(30*'-')
    print('')
    print('Number of fitted objects in final sample with red. pgstat [0.9, 2.0]: '+str(merged_size))
    print('Number of fitted objects in final sample with red. pgstat [.95, 1.5]: '+str(tighter_merge_size))
    print('')
    criterion_list = ['BG Count Rate < 5c/s', 'Ratios >= 10', 'Source Exposure > 60s', 'Source Counts > 2000', 'Source Counts > 5000']
    
    print('Criterion for final sample: ', criterion_list)
            
def two_plots(full_file, after_cuts_file, plot_dir):
    # Import(s)
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    
    # Action
    full_df = pd.read_csv(full_file)
    cut_df = pd.read_csv(after_cuts_file)
    
    all_ratios = np.array(full_df['source_bg_ratios'])
    all_source_count_rates = np.array(full_df['source_count_rates'])
    
    cut_ratios = np.array(cut_df['source_bg_ratios'])
    cut_source_count_rates = np.array(cut_df['source_count_rates'])
    
    source_counts = np.array(cut_df['source_counts_master'])
    redpgs = np.array(cut_df['redpgstat'])
    
    # Make first plot
    plt.rcParams['font.family']='serif'
    plt.scatter(all_source_count_rates, all_ratios, color='lightsteelblue', edgecolors='black', label='All Data')
    plt.scatter(cut_source_count_rates, cut_ratios, color='#408ee0', edgecolors='black', label='Edited Sample')
    plt.legend(fancybox=False, framealpha=0, edgecolor='black')
    
    plt.yscale('log')
    plt.xscale('log')
    
    plt.xlabel('Source Count Rate')
    plt.ylabel('Count Rate Ratio')
    
    #plt.axes().yaxis.set_minor_locator(ticker.AutoMinorLocator())
    #plt.axes().xaxis.set_minor_locator(ticker.AutoMinorLocator())
    plt.tick_params(axis='both',which='both',direction='in')
    plt.tick_params(which='both',bottom=True,top=True,left=True,right=True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    
    plt.savefig(plot_dir+'/ratio_comparison.png', dpi=150)
    
    plt.clf()
    plt.close()
    
    # Make second plot
    plt.rcParams['font.family']='serif'
    plt.scatter(source_counts, redpgs, color='#408ee0', edgecolors='black')
    plt.xscale('log')
    
    plt.xlabel('log10 Source Counts')
    plt.ylabel('Reduced pg-Stat')
    
    plt.axes().yaxis.set_minor_locator(ticker.AutoMinorLocator())
    #plt.axes().xaxis.set_minor_locator(ticker.AutoMinorLocator())
    
    plt.tick_params(axis='both',which='both',direction='in')
    plt.tick_params(which='both',bottom=True,top=True,left=True,right=True)
    plt.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
    
    plt.savefig(plot_dir+'/source_counts_comparison.png', dpi=150)
    
    plt.clf()
    plt.close()
    
    
key = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/misc/all_seg_ids.csv'
data_dir = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus'
results_file = '/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/information_for_cuts.csv'

#evaluate_cuts(key, data_dir, results_file)
log_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored/logs'
#count_sample(results_file, log_dir)

after_sample_cuts = '/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/aftersamplecuts.csv'
full_file = '/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/information_for_cuts.csv'
plot_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts'
two_plots(full_file, after_sample_cuts, plot_dir)