# wsl of this file: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/fix_pds_plot_paths.py

# wsl base: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/
# wsl base two: /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***.jsgrp
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm 
from astropy.table import Table

ids_file = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv'
ids = np.array(pd.read_csv(ids_file)['full_id'])

pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
#fak_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'

for full_id in tqdm(ids): 
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    pds = pds_temp.replace('+++', obs_id).replace('***', gti)
    hdul = fits.open(pds, mode='update')
    
    t = Table.read(hdul[1])  

    # fix rmf
    fak = pds.replace('-bin.pds', '-fak.rsp')
    t.meta['RESPFILE'] = fak

    # write changes 

    hdul[1] = fits.table_to_hdu(t) 

    hdul.flush()
        
    hdul.close()