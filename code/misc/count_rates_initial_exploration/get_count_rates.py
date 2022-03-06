# cSpell: disable
# this file's wsl path: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/misc/count_rates_initial_exploration/get_count_rates.py


def make_count_rates_file(): 
    
    import pandas as pd
    import numpy as np
    from astropy.io import fits
    from tqdm import tqdm 
    #from rebin import rebin

    out_df = pd.DataFrame()

    key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv'
    data_dir = "/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus"
    wsl_base = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535'

    full_ids = np.array(pd.read_csv(key)['full_id'])
    for full_id in tqdm(full_ids): 
        id_list = full_id.split('_')
        obsid = id_list[0]
        gti = id_list[1]    

        data_file = data_dir + '/' + obsid + '/jspipe/js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
        bg_file = data_file.replace('.jsgrp', '.bg')

        data_hdul = fits.open(data_file)
        
        counts_array = np.array(data_hdul[1].data['COUNTS'])
        exp_time = float(data_hdul[1].header['EXPOSURE'])
        channels_array = np.array(data_hdul[1].data['CHANNEL'])
        
        # -0.5 1.5-2.3
        soft_mask_one = np.logical_and(channels_array>=50, channels_array<400)
        soft_mask_two = np.logical_or(channels_array>230, channels_array<150)

        counter = 0
        soft_mask = []
        for i, j in zip(soft_mask_one, soft_mask_two): 
            if i==j and i==True: 
                soft_mask.append(counter)
            counter+=1 

        soft_counts= channels_array[soft_mask]

        hard_mask = np.logical_and(channels_array>=400, channels_array<=999)

        hard_counts = counts_array[hard_mask]

        bg_hdul = fits.open(bg_file)
        bg_counts_array = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        bg_hard_counts = bg_counts_array[hard_mask]
        bg_soft_counts = bg_counts_array[soft_mask]

        scale_factor = exp_time/bg_exp_time

        net_soft_counts = (soft_counts-(bg_soft_counts*scale_factor))/exp_time
        net_hard_counts = (hard_counts-(bg_hard_counts*scale_factor))/exp_time

        #hardness_numerator = (hard_counts-(bg_hard_counts/bg_exp_time*exp_time))
        net_counts = np.concatenate((net_soft_counts, net_hard_counts))
        
        #rebinned = rebin(net_counts, 17, func=np.sum)
        # do rebinning in google collab 
        out_df[full_id] = net_counts

    out_df.transpose()
    out_df.to_csv(wsl_base+'/code/misc/count_rates_initial_exploration/count_rates.csv', index=False)

make_count_rates_file()