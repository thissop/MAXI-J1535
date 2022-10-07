import pandas as pd 
import os 
from astropy.io import fits 
from tqdm import tqdm 
import numpy as np

def initial_finalization_lol(): 

    df =  pd.read_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv')

    new_df = pd.DataFrame()

    '''
    GRS
    net_count_rate: A
    gamma: B
    kTe: C
    nthcomp_norm: D
    diskbb_tin: E 
    diskbb_norm: F
    hardness: G

    MAXI

    A:simpl_FracScat
    B:net_source_count_rate
    C:tin_before_error
    D:diskbb_norm_before_error
    E:gamma_before_error
    F:nthcomp_norm_before_error
    G:hardness_ratio 

    SHARED 

    A: net_count_rate
    B: hardness 
    C: gamma
    D: nthcomp_norm 
    E: diskbb_tin
    F: diskbb_norm

    '''

    out_cols = ['observation_ID', 'A', 'B', 'C', 'D', 'E', 'F']

    # SORT TO SAME OUTPUT LETTER COLUMNS FOR EASE OF EXPLANATION

    keep = ['observation_ID', 'A', 'G', 'B', 'D', 'E', 'F']

    for i, j in zip(keep, out_cols):
        new_df[j] = df[i]
    ## GRS ## 
    new_df.to_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv', index=False)
    ## maxi 
    df =  pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv')

    new_df = pd.DataFrame()

    keep = ['observation_ID', 'B', 'G', 'E', 'F', 'C', 'D']

    for i, j in zip(keep, out_cols):
        new_df[j] = df[i]

    new_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv', index=False)

def make_grs_hardness_files(): 
    grs_df =  pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv')
    commands_file = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/xspec_commands.sh'

    commands = ['heainit', 'xspec']
    
    # Handle GRS FIRST 

    for observation_ID in tqdm(list(grs_df['observation_ID'])):
        
        commands.append(f'cd /mnt/c/Users/Research/Documents/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/{observation_ID}')
        commands.append('data src_pcu2.pha')
        commands.append('ignore **-2.0 7.0-**')
        commands.append(f'log /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/GRS_logs/{observation_ID}_soft.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('notice **-**')
        commands.append('ignore **-13.0 60.0-**')
        commands.append(f'log /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/GRS_logs/{observation_ID}_hard.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('data none')

    commands.append('cd /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/')
    
    '''
    for observation_ID in list(maxi_df['observation_ID']):
        observation_ID_list = observation_ID.split('_')
        obsid = observation_ID_list[0]
        gti = observation_ID_list[1]
        commands.append(f'data /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp')

        commands.append('ignore **-0.5 3.0-**')
        commands.append('ignore 1.7-2.3')
        commands.append(f'log {observation_ID}_soft.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('notice **-**')
        commands.append('ignore **-3.0 10.0-**')
        commands.append(f'log /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/MAXI_logs/{observation_ID}_hard.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('data none')
    
    '''

    with open(commands_file, 'w') as f1: 
        for line in commands: 
            f1.write(line+'\n')

def do_maxi_stuff(): 
    maxi_df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv') 


    hardness_ratios = []

    for observation_ID in tqdm(list(maxi_df['observation_ID'])):
        observation_ID_list = observation_ID.split('_')
        obsid = observation_ID_list[0]
        gti = observation_ID_list[1]

        source_fits = f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp'
        bg_fits = source_fits.replace('.jsgrp', '.bg')
        data_hdul = fits.open(source_fits)
        counts_arr = np.array(data_hdul[1].data['COUNTS'])
        exp_time = float(data_hdul[1].header['EXPOSURE'])
        
        soft_counts = np.sum(counts_arr[50:170])+np.sum(counts_arr[230:300])
        hard_counts = np.sum(counts_arr[400:1000])

        bg_hdul = fits.open(bg_fits)
        bg_counts_arr = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        bg_soft_counts = np.sum(bg_counts_arr[50:170])+np.sum(bg_counts_arr[230:300])
        bg_hard_counts = np.sum(bg_counts_arr[400:1000])
        
        net_hard = (hard_counts-(bg_hard_counts/bg_exp_time*exp_time))
        net_soft = (soft_counts-(bg_soft_counts/bg_exp_time*exp_time))
        
        hardness_ratio = net_soft / (net_soft+net_hard)
        hardness_ratios.append(hardness_ratio)

    maxi_df['B'] = hardness_ratios
    maxi_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv', index=False)

#do_maxi_stuff()

def aggregate_grs_stuff(): 
    import re 

    grs_df =  pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv')

    hardness_ratios = []

    def get_net_countrate(filepath):
            with open(filepath, 'r') as f:
                for line in f: 
                    if '#Net count rate (cts/s)' in line: 
                        line_list = (re.sub(' +', ',', line)).split(',')
                        return float(line_list[6])


    for observation_ID in tqdm(list(grs_df['observation_ID'])):
        hard_file = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/GRS_logs/{observation_ID}_hard.txt'
        soft_file = hard_file.replace('_hard.txt','_soft.txt')
        #'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/GRS_logs/10258-01-02-00_soft.txt'
        #'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_softness/GRS_logs/10258-01-02-00_soft.txt'

        hard = get_net_countrate(hard_file)
        soft = get_net_countrate(soft_file)
        
        hardness = (soft)/(soft+hard)
        hardness_ratios.append(hardness)

    grs_df['B'] = hardness_ratios 
    grs_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv', index=False)

aggregate_grs_stuff()