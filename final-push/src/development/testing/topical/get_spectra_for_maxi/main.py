import pandas as pd
import numpy as np
from astropy.io import fits
from tqdm import tqdm 
from rebin import rebin

observation_IDs = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_QPO-Input.csv')['observation_ID'])

master_counts = []

for observation_ID in tqdm(observation_IDs): 
    obsid_list = observation_ID.split('_')
    obsid = obsid_list[0]
    gti = obsid_list[1]
    hdul = fits.open(f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp')
    #print(list(hdul[0].header))
    #print(list(hdul[1].header))
    #print(hdul.info())
    '''
    No.    Name      Ver    Type      Cards   Dimensions   Format
    0  PRIMARY       1 PrimaryHDU       5   ()      
    1  SPECTRUM      1 BinTableHDU     70   1501R x 4C   [J, J, I, I] 
    '''

    #hdul.info()
    data = pd.DataFrame(hdul[1].data)
    mask = np.logical_and(data.index>=50, data.index<=999)
    exp = hdul[1].header['EXPOSURE'] # correct for background subtraction
    chan, counts = (np.array(data[i])[mask] for i in ['CHANNEL', 'COUNTS'])

    bg_hdul = hdul = fits.open(f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp')
    bg_counts = np.array(pd.DataFrame(bg_hdul[1].data)['COUNTS'])[mask]
    bg_exp = bg_hdul[1].header['EXPOSURE']
    counts = counts-(bg_counts*exp/bg_exp)/exp

    rebin_counts = rebin(counts, factor=50, func=np.sum)

    if rebin_counts.shape[0]!=19: 
        raise Exception(f'{observation_ID} is Wrong Size when Rebinned!')

    df = pd.DataFrame(np.transpose([chan, counts]), columns=['CHANNEL', 'COUNTS'])

    df.to_csv(f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/MAXI_J1535-571/raw_spectral/{observation_ID}.csv', index=False)    
    
    master_counts.append(rebin_counts)

df = pd.DataFrame()
df['observation_ID'] = observation_IDs
master_counts = np.transpose(master_counts)
for i in range(19):
    df[f'rebin_channel_{i}'] = master_counts[i]

df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Rebin-Spectra.csv', index=False)


'''
background subtracted rebinned source count rates

'''