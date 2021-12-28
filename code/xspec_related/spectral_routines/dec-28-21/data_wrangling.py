from os import error


def wrangle_to_csv(log_dir, data_dir):
    # Import(s)
    import os, shutil, re
    import numpy as np
    import pandas as pd
    from astropy.io import fits
    
    # Action 
    
    def split_line(line):
        return re.sub(' +', ',', line).split(',')
    
    log_files = np.array([
        os.path.join(log_dir, 
        file) for file in os.listdir(log_dir) if 'errorlog' not in file])
    
    dict = {
    'ids':np.array([]),
    'net_count_rates':np.array([]),
    'source_percents':np.array([]),
    'hardness_ratios':np.array([]),
    'mjds':np.array([]),
    'tins':np.array([]),
    'diskbb_norms':np.array([]),
    'gammas':np.array([]),
    'nthcomp_norms':np.array([]),
    'red_pgs':np.array([]),
    'tin_lowers':np.array([]),
    'tin_uppers':np.array([]),
    'tin_tclouts':np.array([]),
    'diskbb_norm_lowers':np.array([]),
    'diskbb_norm_uppers':np.array([]),
    'diskbb_norm_tclouts':np.array([]),
    'gamma_lowers':np.array([]),
    'gamma_uppers':np.array([]),
    'gamma_tclouts':np.array([]),
    'nthcomp_norm_lowers':np.array([]),
    'nthcomp_norm_uppers':np.array([]),
    'nthcomp_norm_tclouts':np.array([]),
    }    
    
    for log_file in log_files: 
        seg_id = log_file.split('/')[-1].replace('.txt', '')
        dict['ids'] = np.append(dict['ids'], seg_id)
        id_list = seg_id.split('_')
        obsid = id_list[0]
        gti = id_list[1]    
            
        # Retrieve fitted spectral parameters
        with open(log_file, 'r') as f:
            for line in f: 
                if '#Net count rate (cts/s)' in line: 
                    line_list = split_line(line)
                    net_count_rate = float(line_list[6])
                    source_percent = float(line_list[9].replace('(', ''))
                    dict['net_count_rates'] = np.append(dict['net_count_rates'], net_count_rate)
                    dict['source_percents'] = np.append(dict['source_percents'], source_percent)
                
                elif '#   2    2   diskbb     Tin' in line: 
                    tin = float(split_line(line)[6])
                    dict['tins'] = np.append(dict['tins'], tin)
                
                elif '#   3    2   diskbb     norm' in line: 
                    diskbb_norm = float(split_line(line)[5])
                    dict['diskbb_norms'] = np.append(dict['diskbb_norms'], diskbb_norm)
                    
                elif '#   4    3   nthComp    Gamma' in line: 
                    gamma = float(split_line(line)[5])
                    dict['gammas'] = np.append(dict['gammas'], gamma)                        
                
                elif '#   9    3   nthComp    norm' in line: 
                    nthcomp_norm = float(split_line(line)[5])
                    dict['nthcomp_norms'] = np.append(dict['nthcomp_norms'], nthcomp_norm)
                    
                elif '#Fit statistic  : PG-Statistic' in line: 
                    pg_stat = float(split_line(line)[4])
                    
                elif '#Test statistic : Chi-Squared' in line: 
                    dof = float(split_line(line)[4])
                    red_pg = pg_stat/dof
                    dict['red_pgs'] = np.append(dict['red_pgs'], red_pg)
        
        # Get error information
        error_log_file = os.path.join(log_dir, seg_id+'_errorlog.txt')
        
        error_df = pd.read_csv(error_log_file)
        error_params = np.array(['tin', 'diskbb_norm', 'gamma', 'nthcomp_norm'])
        
        df_idx = len(error_df.index)
        if df_idx == 4: 
            for row_idx, error_param in zip(range(len(error_df)), 
            error_params):                  
                row = error_df.loc[row_idx]
                
                arrs = ['_lowers', '_uppers', '_tclouts']
                        
                df_cols = ['lower_bound', 'upper_bound', 'error_string']
                
                for arr, df_col in zip(arrs, df_cols):
                    dict[error_param+arr] = np.append(dict[error_param+arr], 
                                                    row[df_col])
        else: 
            arrs = ['_lowers', '_uppers', '_tclouts']
            for error_param in error_params:
                for arr in arrs: 
                    dict[error_param+arr] = np.append(dict[error_param+arr], np.nan) 
                
            
        # Get hardness ratio
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
        
        soft_mask = np.logical_and(channels_array>=200, channels_array<=399)
        hard_mask = np.logical_and(channels_array>=400, channels_array<=999)
        
        hard_counts = np.sum(counts_array[hard_mask])
        soft_counts = np.sum(counts_array[soft_mask])
        
        mjd = float(data_hdul[1].header['MJDSTART'])
        dict['mjds'] = np.append(dict['mjds'], mjd)
        
        orig_bg = bg_file
        temp_bg_file = bg_file.replace('.bg', '(temp).bg')
        shutil.copyfile(orig_bg, temp_bg_file)
        bg_hdul = fits.open(temp_bg_file)
        bg_counts_array = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        bg_hard_counts = np.sum(bg_counts_array[hard_mask])
        bg_soft_counts = np.sum(bg_counts_array[soft_mask])
        
        hardness_numerator = (hard_counts-(bg_hard_counts/bg_exp_time*exp_time))
        hardness_denom = (soft_counts-(bg_soft_counts/bg_exp_time*exp_time))
        
        hardness_ratio = hardness_numerator / hardness_denom
        
        dict['hardness_ratios'] = np.append(dict['hardness_ratios'], hardness_ratio)
        
        os.remove(temp_data_file)
        os.remove(temp_bg_file)
        
    df = pd.DataFrame.from_dict(dict)
    df.to_csv('results.csv', index=False)
    
    df = pd.read_csv('results.csv')
    out_file = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored/results.csv'
    df.to_csv(out_file, index=False)
    
logs_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored/logs'
data_dir = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus'

wrangle_to_csv(logs_dir,data_dir)

