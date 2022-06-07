def run_corrections(): 

    import os 
    from astropy.io import fits 
    from tqdm import tqdm 
    import pandas as pd
    linux = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'

    df = pd.read_csv(linux+'code/misc/meta_preparation/rxte_motta/fits_key.csv')

    os.chdir(linux+'code/xspec_related/pycorr')

    #df = df.iloc[[0,1]]

    obsids = df['obsid']
    spec_files = df['spectral_file']

    for index in tqdm(range(len(obsids))): 

        obsid = obsids[index]
        spec_file = spec_files[index]

        file_to_correct = linux+'data/processed/2022/meta_qpo/motta_spectral_files/'+obsid+'/'+spec_file

        hdul = fits.open(file_to_correct)
        mjd = int(hdul[1].header['MJDREFI']) 
        if mjd <= 51259: 
            epoch = '3o'
        else: 
            epoch = '45'

        os.system('python pcacorr.py -p 2 -e '+epoch+' '+file_to_correct)

run_corrections()