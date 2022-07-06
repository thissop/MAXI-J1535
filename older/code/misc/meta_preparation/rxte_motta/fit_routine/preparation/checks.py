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
    source_percents = []
    
    spectral_files = []
    bg_files = []

    background_count_rates = [] # reject >= 5
    bg_source_ratios = [] # reject < 10, equals (bg counts+source counts)/bg counts
    exposure_times = [] # reject < 60 s
    net_source_counts = [] # reject < 5000


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

                        background_count_rates.append(bg_sum/bg_exposure)

                        scaled_bg_counts = (bg_sum*(exposure/bg_exposure))
                        bg_source_ratio = (scaled_bg_counts+source_sum)/scaled_bg_counts

                        bg_source_ratios.append(bg_source_ratio)

                        net_source = source_sum - scaled_bg_counts
                        net_source_counts.append(net_source)

                        source_percent = 100*(source_sum / (scaled_bg_counts+source_sum))
                        source_percents.append(source_percent)

                        spectral_files.append(file)
                        bg_files.append(file.replace('s2.pha', 'b2.pha'))

    zipped = list(zip(obsids,objects,instruments,resp_files,obs_dates,obs_times,time_starts,source_percents,spectral_files,bg_files,background_count_rates,bg_source_ratios,exposure_times,net_source_counts))
    cols = ['obsid','object','instrument','resp_file','obs_date','obs_time','time_start','source_percent','spectral_file','bg_file','background_count_rate','bg_source_ratio','exposure_time','net_source_count']
    out_df = pd.DataFrame(zipped, columns=cols)
    out_df.to_csv(out_file, index=False)

#gather_information()

def evaluate_cuts(info: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv'): 
    import pandas as pd
    import numpy as np

    df = pd.read_csv(info)

    # reject >= 5
    # reject < 10, equals (bg counts+source counts)/bg counts
    # reject < 60 s
    # reject < 5000

    print('SAMPLE REDUCTION RESULTS')
    print('0. Initial Size:', len(df.index))
    df = df.iloc[np.where(df['bg_source_ratio']>10)]
    print('1. (bg counts+source counts)/(bg counts) > 10:', len(df.index))
    df = df.iloc[np.where(df['exposure_time']>60)]
    print('2. exposure time > 60 s:', len(df.index))
    df = df.iloc[np.where(df['net_source_count']>5000)]
    print('3. Net Source Counts > 5000:', len(df.index))
    bad_df = df.iloc[np.where(df['background_count_rate']<5)]
    print('4. bg cts/s < 5:', len(bad_df.index))

    import matplotlib.pyplot as plt

    plt.style.use('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/misc/stolen_science.mplstyle?token=GHSAT0AAAAAABP54PQO2X2VXMNS256IWOBOYRNCFBA')
    fig, ax = plt.subplots(figsize=(6,7))

    objects = list(set(df['object']))
    counts = [len(np.where(df['object']==i)[0]) for i in objects]

    mask = np.argsort(counts)[::-1]

    objects, counts = (np.array(objects)[mask], np.array(counts)[mask])

    ax.bar(objects, counts)

    ax.set_xticklabels([i.replace('_',' ') for i in objects], rotation=90)

    ax.set(ylabel='Observation Count')
    
    plt.tight_layout()
    plt.savefig('sources.png', dpi=150)
        
evaluate_cuts()