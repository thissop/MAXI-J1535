# /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/routine_executor.py

def run_routine(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                download_dir:str='./code/misc/meta_preparation/rxte_motta/downloader/motta_spectral_files'): 

    import xspec 
    from xspec import *
    import pandas as pd
    from tqdm import tqdm
    import warnings

    if download_dir[-1]!='/': 
        download_dir+='/'

    key_df = pd.read_csv(fits_key)
    source_spectrums = key_df['spectral_file']
    bg_files = key_df['bg_file']
    objects = key_df['object']

    log_temp = ''

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    for index in tqdm(range(len(key_df.index))): 

        id_list = full_id.split('_')
        prop_num = id_list[0]

        data_dir = download_dir+prop_num+'/'

        s1 = Spectrum(data_dir+source_spectrums[index])
        s1.ignore("**-3.0") 
        s1.ignore('45.-**')

        AllData.ignore("bad")

        m1 = Model("tbabs*(nthcomp+diskbb)")

        # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
        # print(m1.TBabs.parameterNames) # ['nH']
        # print(m1.simpl.parameterNames) # ['Gamma', 'FracSctr', 'UpScOnly']
        # print(m1.diskbb.parameterNames) # ['Tin', 'norm']
        
        m1.TBabs.nH = 3.2107
        m1.TBabs.nH.frozen = True 

        m1.simpl.Gamma.values = [2.0,0.05,1.1,1.4,3.5,4.]
        m1.simpl.FracSctr.values = [0.1,0.01,0.001,0.01,0.9,1.]
        m1.simpl.UpScOnly = 1

        m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

        Fit.nIterations = 300
        Fit.statMethod = "pgstat"

        Fit.perform()

        logFile = Xset.openLog(log_temp+'/'+full_id+'.txt')
        s1.show()
        m1.show()
        Fit.show()
        Xset.closeLog()

        AllModels.clear()
        AllData -= "*"

        # go scrape that data before running another iteration, delete log. 
