def check_objects(top_dir:str=''): 
    import os 
    from astropy.io import fits
    from tqdm import tqdm 

    if top_dir[-1]!='/': 
        top_dir+='/'

    objects = []
    for dir in tqdm(os.listdir(top_dir)): 
        if dir!='.gitkeep': 
            data_dir = top_dir+dir+'/'
            for file in os.listdir(data_dir):
                if 's0' in file: 
                    hdul = fits.open(data_dir+file)
                    hdul_keys = list(hdul[0].header)
                    if 'OBJECT' in hdul_keys: 
                        objects.append(str(hdul[0].header['OBJECT'])) 
                    else: 
                        print("NO OBJECT!", file)

    print(list(set(objects))) 
    '''
    'MAXI_J1543-564', ??'ASM_J1748-2848', 'XTE_J1650-500', 'MAXI_J1659-152', 
    'XTE_J1817-330', '4U_1630-47', 'GRO_J1655-40', 'H1743-322', 
    'XTE_J1829-098', 'XTE_J1746-319', 'XTE_J1859+226', 'GX_339-4', 
    'H_1743-322', 'XTE_J1748-2848', '4U1543-47', 'XTE_J1550-564', 
    'GX339-4', 'SWIFT_J1753.5-0127', 'XTE_J1752-223'
    '''

#check_objects('./code/misc/meta_preparation/rxte_motta/downloader/downloads')

def gather_information(top_dir: str='./code/misc/meta_preparation/rxte_motta/downloader/motta_spectral_files', 
                    out_file: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv'): 
    import os 
    from astropy.io import fits
    from astropy.table import Table
    from tqdm import tqdm 
    import pandas as pd

    if top_dir[-1]!='/': 
        top_dir+='/'

    obsids = []
    objects = []
    instruments = []
    resp_files = []
    obs_dates = []
    obs_times = []
    time_starts = []
    net_source_counts = []
    source_percents = []
    exposure_times = []
    spectral_files = []
    bg_files = []

    for dir in tqdm(os.listdir(top_dir)): 
        if dir!='.gitkeep': 
            data_dir = top_dir+dir+'/'
            for file in os.listdir(data_dir):
                if 's2' in file: 
                    data_path = data_dir+file
                    hdul = fits.open(data_path)
                    hdul_keys = list(hdul[0].header)
                    if 'OBJECT' in hdul_keys: 
                        objects.append(str(hdul[1].header['OBJECT'])) 
                        obsids.append(dir)
                        instruments.append(str(hdul[1].header['INSTRUME']))
                        resp_files.append(str(hdul[1].header['RESPFILE']))
                        obs_dates.append(str(hdul[1].header['DATE-OBS']))
                        obs_times.append(str(hdul[1].header['TIME-OBS']))
                        time_starts.append(str(hdul[1].header['TSTART']))
                        exposure = float(hdul[1].header['EXPOSURE'])
                        exposure_times.append(exposure)

                        source_sum = sum(Table.read(hdul, hdu=1)['COUNTS'])

                        bg_hdul = fits.open(data_path.replace('s2.pha', 'b2.pha'))
                        bg_sum = sum(Table.read(bg_hdul, hdu=1)['COUNTS'])
                        bg_exposure = float(bg_hdul[1].header['EXPOSURE'])

                        net_source = source_sum - (bg_sum*(exposure/bg_exposure))
                        net_source_counts.append(net_source)

                        source_percent = 100*(source_sum / ((bg_sum*(exposure/bg_exposure))+source_sum))
                        source_percents.append(source_percent)

                        spectral_files.append(file)
                        bg_files.append(file.replace('s2.pha', 'b2.pha'))

    zipped = list(zip(obsids,objects,instruments,resp_files,obs_dates,obs_times,time_starts,net_source_counts,source_percents,exposure_times, spectral_files, bg_files))
    cols = ['obsid','object','instrument','resp_file','obs_date','obs_time','time_start','net_source_count','source_percent','exposure_time', 'spectral_file', 'bg_file']
    out_df = pd.DataFrame(zipped, columns=cols)
    out_df.to_csv(out_file, index=False)

gather_information()