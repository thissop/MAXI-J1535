# wsl of this file: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/fix_paths.py

# wsl base: /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/
# wsl base two: /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***.jsgrp
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm 
from astropy.table import Table


ids_file = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv'
ids = np.array(pd.read_csv(ids_file)['full_id'])
data_root = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/'

for full_id in tqdm(ids): 
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    jsgrp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***.jsgrp'.replace('+++', obs_id).replace('***', gti)
    hdul = fits.open(jsgrp, mode='update')
    
    t = Table.read(hdul[1])  
    
    # fix bg 
    bg = t.meta['BACKFILE']
    t.meta['BACKFILE'] = jsgrp.replace('jsgrp','bg')

    # fix rmf
    rmf =t.meta['RESPFILE']
    t.meta['RESPFILE'] = data_root + rmf

    # fix arf
    arf = t.meta['ANCRFILE']
    t.meta['ANCRFILE'] = data_root + arf 

    hdul[1] = fits.table_to_hdu(t) 

    hdul.flush()
        
    hdul.close()