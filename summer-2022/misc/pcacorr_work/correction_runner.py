def run_corrections(): 

    import os 
    from astropy.io import fits 
    from tqdm import tqdm 
    import pandas as pd
    linux = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'

    df = pd.read_csv(linux+'code/misc/meta_preparation/rxte_motta/fits_key.csv')

    os.chdir(linux+'code/xspec_related/pycorr')

    #df  = df.iloc[[0,1,2,3,4,5]]

    for obsid, spec_file in tqdm(zip(df['obsid'], df['spectral_file'])): 

        #hdul = fits.open()
        #mjd = int(hdul[1].header['MJDREFI']) 

        file_to_correct = linux+'data/processed/2022/meta_qpo/motta_spectral_files/'+obsid+'/'+spec_file

        os.system('python pcacorr.py '+file_to_correct)

run_corrections()