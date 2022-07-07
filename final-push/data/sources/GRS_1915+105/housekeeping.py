def reformat_spectral_directory(root:str='./final-push/data/sources/GRS_1915+105/spectral/external_spectra/'): 
    r'''
    
    this function is irrelevant now because it's been executed
    
    '''
    import os 
    import shutil
    from tqdm import tqdm 

    if root[-1]!='/':
        root+='/'
    
    obsids = [i for i in os.listdir(root) if i != 'Users'] 
    for obsid in tqdm(obsids): 
        sub_dir = root+'Users/users/mariano/liang/GRS1915_C/'+obsid+'/' 
        for f in os.listdir(sub_dir): 
            shutil.copyfile(sub_dir+f, root+obsid+'/'+f)

