# /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/routine_executor.py
import xspec 
from xspec import *
import pandas as pd
from tqdm import tqdm

all_ids = list(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv')['full_id'])

spectral_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***.jsgrp'
log_temp = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/logs'


Xset.chatter = 0
Xset.logChatter = 10
Fit.query = "no"

for full_id in tqdm(all_ids): 

    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    jsgrp = spectral_temp.replace('+++', obs_id).replace('***', gti)

    s1 = Spectrum(jsgrp)
    s1.ignore("**-0.5")
    s1.ignore("1.5-2.3")
    s1.ignore("10.0-**")
    AllData.ignore("bad")

    m1 = Model("tbabs*(simpl*diskbb)")
    AllModels.setEnergies(".01 200. 1000 log")
    # print(m1.componentNames) # ['TBabs', 'simpl', 'diskbb']
    # print(m1.TBabs.parameterNames) # ['nH']
    # print(m1.simpl.parameterNames) # ['Gamma', 'FracSctr', 'UpScOnly']
    # print(m1.diskbb.parameterNames) # ['Tin', 'norm']
    m1.TBabs.nH = 3.2107
    m1.TBabs.nH.frozen = True 

    m1.simpl.Gamma.values = [2.0,0.05,1.1,1.4,3.5,4.]
    m1.simpl.FracSctr.values = [0.1,0.01,0.001,0.01,0.9,1.]
    m1.simpl.UpScOnly = 1
    m1.simpl.UpScOnly.frozen = True

    m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

    Fit.nIterations = 250
    Fit.statMethod = "pgstat"

    Fit.perform()

    logFile = Xset.openLog(log_temp+'/'+full_id+'.txt')
    s1.show()
    m1.show()
    Fit.show()
    Xset.closeLog()

    AllModels.clear()
    AllData -= "*"
    
    # make plot....compress dir after --> next time (before paper?)