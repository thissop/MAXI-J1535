import os 
import re
from astropy.io import fits
import numpy as np

maxi = False 
grs = False 

temp_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/temp_dir/'
maxi_results = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/MAXI_spectral_results.csv'
grs_results = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/GRS_spectral_results.csv'

if not os.path.exists(maxi_results):
    with open(maxi_results, 'w') as f1:
        f1.write('observation_ID,A,B,C,D,E,F,G\n') 

if not os.path.exists(grs_results):
    with open(grs_results, 'w') as f2:
        f2.write('observation_ID,A,B,C,D,E,F,G\n') 

log_file = ''

for file in os.listdir(temp_dir):
    
    log_file = f'{temp_dir}{file}'
    
    if 'MAXI' in file: 
        maxi = True 

    elif 'GRS' in file: 
        grs = True 

    else: 
        raise Exception('wrong file name!')
    
    break 
       
observation_ID = log_file.split('|')[1] 
net_count_rate = None 
hardness = None 
gamma = None 
nthcomp_norm = None
kTe = None 
Tin = None 
diskbb_norm = None 

with open(log_file, 'r') as f3: 
    for line in f3: 

        line_list = re.sub(' +', ',', line.strip()).split(',')

        if 'Net count rate (cts/s)' in line: 
            net_count_rate = line_list[6]
        
        elif 'diskbb     Tin' in line: 
            Tin = line_list[6]
        
        elif 'diskbb     norm' in line: 
            diskbb_norm = line_list[5]
        
        elif 'nthComp    Gamma' in line: 
            gamma = line_list[5]

        elif 'nthComp    norm' in line: 
            nthcomp_norm = line_list[5]

        elif 'nthComp    kT_e' in line: 
            kTe = line_list[6]

        #elif 'Fit statistic  : PG-Statistic' in line: 
        #    pgstat = line_list[4]
        #elif 'Null hypothesis' in line: 
        #    dof = line_list[6]
        #    red_pgstat = float(pgstat)/float(dof)

if maxi: 
    
    id_list = observation_ID.split('_')
    obsid = id_list[0]
    gti = id_list[1]    

    data_file = f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp'
    bg_file = data_file.replace('.jsgrp', '.bg')

    data_hdul = fits.open(data_file)
    
    counts_array = np.array(data_hdul[1].data['COUNTS'])
    exp_time = float(data_hdul[1].header['EXPOSURE'])
    channels_array = np.array(data_hdul[1].data['CHANNEL'])
    
    # -0.5 1.5-2.3
    soft_mask = np.logical_and(channels_array>=50, channels_array<400)
    #soft_mask_two = np.logical_or(channels_array>230, channels_array<150)

    soft_counts= channels_array[soft_mask]

    hard_mask = np.logical_and(channels_array>=400, channels_array<=999)

    hard_counts = counts_array[hard_mask]

    bg_hdul = fits.open(bg_file)
    bg_counts_array = bg_hdul[1].data['COUNTS']
    bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
    
    bg_hard_counts = bg_counts_array[hard_mask]
    bg_soft_counts = bg_counts_array[soft_mask]

    scale_factor = exp_time/bg_exp_time

    net_soft_counts = np.sum((soft_counts-(bg_soft_counts*scale_factor))/exp_time)
    net_hard_counts = np.sum((hard_counts-(bg_hard_counts*scale_factor))/exp_time)

    hardness = str(net_hard_counts/(net_soft_counts+net_hard_counts))

elif grs: 

    hard = None 
    soft = None 

    with open(f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/{observation_ID}/hard.txt', 'r') as fx: 
        for line in fx: 
            if '#Net count rate (cts/s) for Spectrum:1' in line: 
                line_list = re.sub(' +', ',', line).split(',')
                hard = float(line_list[6])

    with open(f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/{observation_ID}/soft.txt', 'r') as fx: 
        for line in fx: 
            if '#Net count rate (cts/s) for Spectrum:1' in line: 
                line_list = re.sub(' +', ',', line).split(',')
                soft = float(line_list[6])
    
    hardness = str(hard/(hard+soft)) 

results_line = ','.join([str(i) for i in [observation_ID, net_count_rate, hardness, gamma, nthcomp_norm, kTe, Tin, diskbb_norm]])

if maxi: 
    with open(maxi_results, 'a') as f4:
        f4.write(results_line+'\n')

elif grs: 
    with open(grs_results, 'a') as f4: 
        f4.write(results_line+'\n')

os.remove(log_file)