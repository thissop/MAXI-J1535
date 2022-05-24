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

move_them()