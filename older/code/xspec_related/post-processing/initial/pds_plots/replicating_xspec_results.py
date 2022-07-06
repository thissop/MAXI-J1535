'''

testing notes

1050360103_0
/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0-bin.pds

/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/replicating_xspec_results.py

'''


import numpy as np
import os
import pandas as pd

import xspec 
from xspec import *

from tqdm import tqdm 

import matplotlib.pyplot as plt
all_ids = list(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv')['full_id'])

#np.random.shuffle(all_ids)

pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
#fak_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'

plot_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/plots_with_model/plots'
data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw'

# fix above two

Xset.chatter = 0
Xset.logChatter = 10
Fit.query = "no"

for full_id in tqdm(all_ids): 
    #full_id = '1050360104_5'
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    pds_file = pds_temp.replace('+++', obs_id)
    pds_file = pds_file.replace('***', gti)

    s1 = Spectrum(pds_file)

    # fix path of spectrum files! 

    s1.ignore('**-0.2')
    s1.ignore('100.-**')

    m1 = Model("loren+loren", modName='m1')
    
    m1.lorentz.LineE = 0
    m1.lorentz.LineE.frozen = True
    m1.lorentz_2.LineE = 0
    m1.lorentz_2.LineE.frozen = True
    
    Fit.perform()

    Plot.splashPage = False
   
    save_data = 'specfit.qdp'
    
    if (os.path.isfile(save_data)):
        os.remove(save_data)
    
    # following Andy Beardmore idea
    Plot.device = '/null'
    Plot.add = True
    Plot.xAxis = "keV"
    Plot.addCommand(f'wd {save_data}')
    Plot("ld") 

    ncomp = len(m1.componentNames)

    names = ['e','de','rate','rate_err','total']
    
    for j in range(ncomp):
        names.append(f'model{j}')

    df = pd.read_table('specfit.qdp',skiprows=3,names=names, delimiter=' ')
    
    # get actual pds data now

    Plot.commands = ()
    Plot('data')

    x = Plot.x()
    y = Plot.y()
    xerr = Plot.xErr()
    yerr = Plot.yErr()

    df['x'] = x
    df['y'] = y
    df['xerr'] = xerr
    df['yerr'] = yerr

    data_log = data_dir + '/' + full_id + '_plot-data.csv'
    df.to_csv(data_log, index=False)

    AllModels.clear()
    AllData -= "*"
    Plot.commands = ()