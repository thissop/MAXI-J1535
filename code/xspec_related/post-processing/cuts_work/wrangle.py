import os
import re
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm

nicer_data_root = 'C:/Users/Research/Documents/GitHub LFS/Steiner/thaddaeus'
spectral_dir = './code/xspec_related/spectral_routines/dec-28-21/current_logs/logs'
qpo_dir = './code/xspec_related/qpo_routines/jan-1-2022/final_logs/final_logs'

results_dict = {'full_ids':[], 

                'mjd':[], 
    
                'net_source_count_rate':[],
                'source_percent':[], 
                'source_exposure_time':[], 

                'tin_before_error':[], 
                'diskbb_norm_before_error':[],
                'gamma_before_error':[],
                'nthcomp_norm_before_error':[], 

                'fit_stat':[], 
                'reduced_fit_stat':[],

                'tin_after_error':[], 
                'diskbb_norm_after_error':[],
                'gamma_after_error':[],
                'nthcomp_norm_after_error':[], 
                
                'hardness_ratio':[], 
                
                'counts_ratio':[],
                'source_counts':[],
                'net_source_counts':[],
                'bg_net_count_rate':[],

                'pds_exposure':[]}


# base sub dict: :{'search_string':r'', 'line_index':}
log_file_dict = {'net_source_count_rate':{'search_string':r'#Net count rate (cts/s)', 'line_index':6}, 
                 'source_percent':{'search_string':r'#Net count rate (cts/s)','line_index':9}, 
                 'tin_before_error':{'search_string':r'#   2    2   diskbb     Tin', 'line_index':6}, 
                 'diskbb_norm_before_error':{'search_string':r'#   3    2   diskbb     norm', 'line_index':5},
                 'gamma_before_error':{'search_string':r'#   4    3   nthComp    Gamma', 'line_index':5},
                 'nthcomp_norm_before_error':{'search_string':r'#   9    3   nthComp', 'line_index':5}, 
                 'fit_stat':{'search_string':r'#Fit statistic', 'line_index':4}}

for qpo_file in tqdm(os.listdir(qpo_dir)):
    full_id = qpo_file.split('.')[0]
    split_id = full_id.split('_')
    obs_id = split_id[0]
    gti = split_id[1]

    ### BEFORE ERROR PART
    before_error_log = spectral_dir+'/'+full_id+'_before_error.txt'
    if os.path.exists(before_error_log): 
        results_dict['full_ids'].append(full_id)
        with open(before_error_log, 'r') as f:
            f_lines = f.readlines()
            for line_index, line in enumerate(f_lines): 
                for search_term, search_array in zip(log_file_dict.keys(), log_file_dict.values()): 
                    if search_array['search_string'] in line: 
                        line_list = (re.sub(' +', '@@@', line)).split('@@@')
                        
                        queried_value = line_list[search_array['line_index']]

                        if search_term == 'net_source_count_rate':
                            source_percent = line_list[log_file_dict['source_percent']['line_index']]
                            source_percent = source_percent[1:]
                            results_dict['source_percent'].append(source_percent)
                            
                        elif search_term == 'fit_stat': 
                            fit_stat = float(queried_value)
                            dof_line_list = (re.sub(' +', '@@@', f_lines[line_index+3])).split('@@@')

                            dof = float(dof_line_list[7])

                            results_dict['reduced_fit_stat'].append(fit_stat/dof)

                        results_dict[search_term].append(queried_value)

                        break    

        ### AFTER ERROR PART 
        after_error_log = spectral_dir + '/' + full_id +'_errorlog.txt'
        after_error_key = ['tin_after_error','diskbb_norm_after_error','gamma_after_error','nthcomp_norm_after_error']
        
        if os.path.exists(after_error_log): 
            with open(after_error_log, 'r') as f:
                f_lines = f.readlines() 
                for line, key_name in zip(f_lines[1:], after_error_key):
                    if 'value' in line: 
                        continue 
                    else: 
                        queried_value = line.split(',')[0]
                        results_dict[key_name].append(queried_value)

        else: 
            for label in after_error_key: 
                results_dict[label].append(np.nan)

        ### SPECTRAL FITS FILE PART

        ### PDS FILE PART
        pds_file = nicer_data_root+'/'+obs_id+'/jspipe/js_ni'+obs_id+'_0mpu7_silver_GTI'+gti+'-bin.pds'

    ### FIX THIS !!! 

        results_dict['pds_exposure'].append(np.nan)

        
        
        ### OTHER FITS OPERATIONS

        data_file = nicer_data_root + '/' + obs_id + '/jspipe/js_ni' + obs_id + '_0mpu7_silver_GTI' + gti + '.jsgrp'
        bg_file = data_file.replace('.jsgrp', '.bg')

        data_hdul = fits.open(data_file)
        
        counts_array = np.array(data_hdul[1].data['COUNTS'])
        exp_time = float(data_hdul[1].header['EXPOSURE'])
        channels_array = np.array(data_hdul[1].data['CHANNEL'])

        results_dict['source_exposure_time'].append(exp_time)
        
        soft_mask = np.logical_and(channels_array>=200, channels_array<=399)
        hard_mask = np.logical_and(channels_array>=400, channels_array<=999)
        
        hard_counts = np.sum(counts_array[hard_mask])
        soft_counts = np.sum(counts_array[soft_mask])
        
        mjd = float(data_hdul[1].header['MJDSTART'])
        results_dict['mjd'].append(mjd)
        
        bg_hdul = fits.open(bg_file)
        bg_counts_array = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        bg_hard_counts = np.sum(bg_counts_array[hard_mask])
        bg_soft_counts = np.sum(bg_counts_array[soft_mask])
        
        hardness_numerator = (hard_counts-(bg_hard_counts/bg_exp_time*exp_time))
        hardness_denom = (soft_counts-(bg_soft_counts/bg_exp_time*exp_time))
        
        hardness_ratio = hardness_numerator / hardness_denom
        
        results_dict['hardness_ratio'].append(hardness_ratio)

        source_sum = hard_counts+soft_counts
        bg_sum = bg_hard_counts+bg_soft_counts
        counts_ratio = (source_sum+bg_sum)/bg_sum

        results_dict['counts_ratio'].append(counts_ratio)

        results_dict['source_counts'].append(source_sum)
        
        net_source_counts = source_sum - (bg_sum/bg_exp_time*exp_time)
        results_dict['net_source_counts'].append(source_sum)

        results_dict['bg_net_count_rate'].append(bg_sum/bg_exp_time)

        data_hdul.close()
        bg_hdul.close()

df = pd.DataFrame.from_dict(results_dict, orient='columns')

for dict_list in results_dict.values(): 
    print(len(dict_list))

df.to_csv('wrangled_spectral_data.csv', index=False)