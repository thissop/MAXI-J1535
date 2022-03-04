def make_pds(key, pds_temp, fak_temp, plot_dir):
    import numpy as np
    import os
    import pandas as pd
    from astropy.io import fits
    import matplotlib.pyplot as plt

    df = pd.read_csv(key)
    ids = np.array(df['full_id'])
    np.random.shuffle(ids) 

    for obs_id in ids: 
        split_id = obs_id.split('_')
        obs_id = split_id[0]
        gti = split_id[1]
    
        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', gti)

        fak_file = fak_temp.replace('+++', obs_id)
        fak_file = fak_file.replace('***', gti)

        hdul_fak = fits.open(fak_file)
        df_x = pd.DataFrame(hdul_fak[1].data)
        lowers = np.array(df_x['E_MIN'])
        uppers = np.array(df_x['E_MAX'])
        combined = np.transpose((lowers, uppers))
        frequencies = np.median(combined, axis=1) 
       

        hdul_pds = fits.open(pds_file)
        
        df_y = pd.DataFrame(hdul_pds[1].data)
        
        rates = np.array(df_y['RATE'])

        mask = np.logical_and(frequencies>0.1, frequencies<20)

        plt.scatter(frequencies[mask], rates[mask])
        plt.plot(frequencies[mask], rates[mask], lw=0.5, color='indianred', zorder=0)
        plt.show()

        #plt.(np.mean())
        #plt.show()
        break 
        #plt.scatter(df_x[''])

key = './code/xspec_related/good_ids.csv'
pds_temp = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus\+++\jspipe\js_ni+++_0mpu7_silver_GTI***_BAND1-bin.pds"
fak_temp = pds_temp.replace('bin.pds','fak.rsp')
plot_dir = './code/xspec_related/qpo_routines/make_vetting_plots/plots/'
make_pds(key, pds_temp, fak_temp, plot_dir)