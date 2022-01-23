import os 
import pandas as pd
import numpy as np


def count_spectral(): 
    root_dir = './code/xspec_related/spectral_routines/dec-28-21/current_logs/logs'
    before_counter = 0
    for file in os.listdir(root_dir): 
        if 'before_error' in file: 
            before_counter += 1

    print('spectral logs: ', before_counter)

def count_qpo(): 
    root_dir = './code/xspec_related/qpo_routines/jan-1-2022/final_logs/final_logs'
    before_counter = 0
    for file in os.listdir(root_dir): 
        if '.csv' in file: 
            before_counter += 1

    print('qpo logs: ', before_counter)

#count_spectral()
#count_qpo()

def count_files_general(): 
    root_dir = './code/xspec_related/spectral_routines/dec-28-21/current_logs/logs'
    before_counter = 0
    for file in os.listdir(root_dir): 
        if 'after_error' in file: 
            before_counter += 1

    print('# logs: ', before_counter)

#count_files_general()

def count_lines_general(): 
    root_dir = './code/xspec_related/spectral_routines/dec-28-21/current_logs/logs'
    for file in os.listdir(root_dir): 
        if 'errorlog.txt' in file: 
            num_lines = sum(1 for line in open(os.path.join(root_dir,file)))
            if num_lines != 5: 
                print(file, num_lines)

#count_lines_general()

def investigate_exposure_times(): 

    exposures = []

    from astropy.io import fits
    nicer_data_root = 'C:/Users/Research/Documents/GitHub LFS/Steiner/thaddaeus'
    qpo_dir = './code/xspec_related/qpo_routines/jan-1-2022/final_logs/final_logs'
    
    
    for qpo_file in os.listdir(qpo_dir):
        full_id = qpo_file.split('.')[0]
        split_id = full_id.split('_')
        obs_id = split_id[0]
        gti = split_id[1]

        pds_file = nicer_data_root+'/'+obs_id+'/jspipe/js_ni'+obs_id+'_0mpu7_silver_GTI'+gti+'-bin.pds'

        if os.path.exists(pds_file): 
            hdul = fits.open(pds_file)
            exposure = hdul[1].header['EXPOSURE']
            exposures.append(exposure)
            hdul.close()

    print(exposures)


#investigate_exposure_times()


def why_this_not_work_lol(): 
    log_file_dict = {'net_source_count_rate':{'search_string':r'#Net count rate (cts/s)', 'line_index':6}, 
                 'source_percent':{'search_string':r'#Net count rate (cts/s)','line_index':9}, 
                 'tin_before_error':{'search_string':r'#   2    2   diskbb     Tin', 'line_index':6}, 
                 'diskbb_norm_before_error':{'search_string':r'#   3    2   diskbb     norm', 'line_index':5},
                 'gamma_before_error':{'search_string':r'#   4    3   nthComp    Gamma', 'line_index':5},
                 'nthcomp_norm_before_error':{'search_string':r'#   9    3   nthComp', 'line_index':5}, 
                 'fit_stat':{'search_string':r'#Fit statistic', 'line_index':4}}


    for i, j in zip(log_file_dict.keys(), log_file_dict.values()): 
        print(i)

why_this_not_work_lol()

    
