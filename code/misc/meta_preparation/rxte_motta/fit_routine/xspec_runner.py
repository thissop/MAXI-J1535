# /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/routine_executor.py
import xspec 
from xspec import *

def run_routine(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                nH_data:str = './code/misc/meta_preparation/rxte_motta/fit_routine/preparation/nH_dict.csv', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results'): 

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+data_dir[2:]

    if nH_data[0:6]=='./code': 
        nH_data = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+nH_data[2:]

    if log_path[0:6] == './code': 
        log_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+log_path[2:]

    warnings.warn('bouma idea: jupyter notebook vs python file paths')

    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    bg_files = key_df['bg_file']
    objects = key_df['object']
    responses = key_df['resp_file']

    nH_df = pd.read_csv(nH_data)
    nH_sources = nH_df['source']
    nH_values = nH_df['nH']

    log_temp = ''

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    for index in tqdm(range(len(key_df.index))): 
        full_id = ids[index]
        id_list = full_id.split('_')
        prop_num = id_list[0]

        source_name = objects[index]

        data_dir = data_dir+prop_num+'/'

        s1 = Spectrum(data_dir+source_spectrums[index])
        
        s1.response = data_dir+responses[index]

        s1.ignore("**-3.0") 
        s1.ignore('45.-**')

        AllData.ignore("bad")

        m1 = Model("tbabs*(nthcomp+diskbb)")

        # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
        # print(m1.TBabs.parameterNames) # ['nH']
        # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
        # print(m1.diskbb.parameterNames) # ['Tin', 'norm']
        
        m1.TBabs.nH = nH_values[np.where(nH_sources==source_name)]
        m1.TBabs.nH.frozen = True 

        m1.nthComp.Gamma.values = ', , 1.1 1.2 3.5 4'
        m1.nthComp.kT_e = 50
        m1.nthComp.kT_e.frozen = True
        m1.nthComp.kT_bb.link = m1.diskbb.Tin 
        m1.nthComp.inp_type = 1
        m1.nthComp.inp_type.frozen = True
        m1.nthComp.Redshift = 0
        m1.nthComp.Redshift.frozen = True

        warnings.warn('red shift?')

        m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

        Fit.nIterations = 300
        Fit.statMethod = "pgstat"

        Fit.perform()

        logFile = Xset.openLog(log_path+'/'+full_id+'.txt')
        s1.show()
        m1.show()
        Fit.show()
        Xset.closeLog()

        AllModels.clear()
        AllData -= "*"

        break

        # go scrape that data before running another iteration, delete log. 
run_routine()