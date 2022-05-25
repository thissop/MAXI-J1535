def move_them(data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files'):
    import os 
    import shutil
    from tqdm import tqdm 


    for dir in tqdm(os.listdir(data_dir)): 
        obsid_dir = data_dir+'/'+dir
        if dir != '.gitkeep':
            for file in os.listdir(obsid_dir): 
                if file!='.gitkeep': 
                    if file[-4:]=='.rsp': 
                        initial_path = obsid_dir+'/'+file
                        new_path = data_dir+'/'+file

                        shutil.copyfile(initial_path, new_path)
                        os.remove(initial_path)

#move_them()

import pandas as pd

def change_resp_paths(data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                      key_df:str=pd.read_csv('./code/misc/meta_preparation/rxte_motta/fits_key.csv'), 
                      wsl_data_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/data/processed/2022/meta_qpo/motta_spectral_files/'): 
    import os 
    import shutil
    from tqdm import tqdm 
    from astropy.io import fits

    import pandas as pd
    import numpy as np

    if data_dir[-1]!='/': 
        data_dir+='/'

    obsids = np.array(key_df['obsid'])
    resp_files = np.array(key_df['resp_file'])
    key_objects = np.array(key_df['object'])

    for dir in tqdm(os.listdir(data_dir)): 
    #for dir in os.listdir(data_dir): 
        obsid_dir = data_dir+dir+'/'
        if dir != '.gitkeep' and '.rsp' not in dir:
            match_index = np.where(obsids==dir)[0]
            for file in os.listdir(obsid_dir): 
                if file!='.gitkeep': 
                    end = file.split('_')[-1]
                    if end=='s2.pha' or end=='b2.pha': 
                        
                        file_path = obsid_dir+file

                        new_resp_path = wsl_data_dir+resp_files[match_index][0]
                        #print(new_resp_path)

                        fits.setval(file_path, 'RESPFILE', value=new_resp_path, ext=1)

                        # RESPFILE in hdul[1].header

change_resp_paths()