# cSpell: disable
# this file's wsl path: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/misc/count_rates_better/core.py

wsl_base = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535'

def make_file(ignore_ranges: str = "default"): 
    '''
    Args: 
        ignore_params: default ignores channels equivalent to ignore **-0.5 1.5-2.3 10.0-** in xspec
                       keep-middle ignores channels equivalent to ignore **-0.5 10.0-** in xspec 
    '''    

    import pandas as pd
    import numpy as np
    from astropy.io import fits
    from tqdm import tqdm 
    import pickle 
    #from rebin import rebin

    ''' 
    
    from xspec prompt: # don't incorporate ignore bad

    Noticed Channels:  [22-54],[83-254]
    ignore **-0.5 1.5-2.3 10.0-**
    21 channels (1-21) ignored in spectrum #     1
    28 channels (55-82) ignored in spectrum #     1
    58 channels (255-312) ignored in spectrum #     1
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Noticed Channels:  [22-254]
    ignore **-0.5 1.5-2.3 10.0-**
    21 channels (1-21) ignored in spectrum #     1
    58 channels (255-312) ignored in spectrum #     1

    '''

    key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv'
    data_dir = "/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus"

    full_ids = np.array(pd.read_csv(key)['full_id'])

    out_dict = {'freq_ranges':[], 
                'freq_medians':[],
                'classes':[],
                'rebin_counts':{}}

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
        freqs_arr = channels_array/100.0
        # -0.5 1.5-2.3 # NICER contains one instrument, the X-ray Timing Instrument (XTI), sensitive in the 0.2–12 keV range, described in detail in Gendreau et al. (2016)

        soft_mask = []
        soft_mask_one = np.logical_and(channels_array>=50, channels_array<400)

        if ignore_ranges == 'default': # [0.5-1.5) U [2.3, 4) U [4-10.0)
            soft_mask_two = np.logical_or(channels_array>230, channels_array<150)
            counter = 0
            for i, j in zip(soft_mask_one, soft_mask_two): 
                if i==j and i==True: 
                    soft_mask.append(counter)
                counter+=1 
            
        elif ignore_ranges == 'keep-middle': 
            print('future development not finished yet')
            raise 

        hard_mask = channels_array[np.logical_and(channels_array>=400, channels_array<=999)]
        
        bg_hdul = fits.open(bg_file)
        bg_counts_array = bg_hdul[1].data['COUNTS']
        bg_exp_time = float(bg_hdul[1].header['EXPOSURE'])
        
        scale_factor = exp_time/bg_exp_time

        net_counts = (counts_array-(bg_counts_array*scale_factor))/exp_time

        #hardness_numerator = (hard_counts-(bg_hard_counts/bg_exp_time*exp_time))
        
        ### rebinning 

        lower = 0
        soft_rebin_indices = []
        while lower < 269-38-1-269%38: # seems really unness 
            # 7 soft bins in new set out of 25, each will be sum worth of 38 items from orig soft array of length 269 (last will have 269%3 extra) 

            soft_rebin_indices.append(soft_mask[lower:lower+38])
            lower+=38

        soft_rebin_indices.append(soft_mask[lower:])

        lower = 0
        hard_rebin_indices = []
        while lower < 600-33-1-600%33:
            # 15 hard bins in new set out of 25, each will be sum worth of 33 items from orig hard array of length 600 (last will have 600%3 extra)
            hard_rebin_indices.append(hard_mask[lower:lower+33])
            lower+=33

        hard_rebin_indices.append(hard_mask[lower:])

        rebin_counts = []
        rebin_ranges = []
        rebin_medians = []
        rebin_classes = []

        for cell in soft_rebin_indices: 
            cell_sum = np.sum(net_counts[cell])

            rebin_counts.append(cell_sum)
            low_freq = freqs_arr[cell[0]]
            high_freq = freqs_arr[cell[-1]]
            inclusive_range = (low_freq, high_freq)
            rebin_ranges.append(inclusive_range)
            median_freq = np.median(freqs_arr[cell])
            rebin_medians.append(median_freq)
            rebin_classes.append('SOFT')

        for cell in hard_rebin_indices: 
            cell_sum = np.sum(net_counts[cell])
            rebin_counts.append(cell_sum)
            inclusive_range = (freqs_arr[cell[0]], freqs_arr[cell[-1]])
            rebin_ranges.append(inclusive_range)
            median_freq = np.median(freqs_arr[cell])
            rebin_medians.append(median_freq)
            rebin_classes.append('HARD')

        out_dict['rebin_counts'][full_id] = rebin_counts

        if full_id == full_ids[0]: 
            out_dict['freq_medians'] = rebin_medians
            out_dict['classes'] = rebin_classes
            out_dict['freq_ranges'] = rebin_ranges

        '''
        >>> print([len(i) for i in soft_rebin_indices])
        [38, 38, 38, 38, 38, 38, 41]
        >>> print([len(i) for i in hard_rebin_indices])
        [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 39]
        '''

    with open(wsl_base+'/rebin_data_dict_25.pickle', 'wb') as handle:
        pickle.dump(out_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

make_file()