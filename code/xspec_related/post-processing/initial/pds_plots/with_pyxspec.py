'''

testing notes

1050360103_0
/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0-bin.pds

/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/with_pyxspec.py

'''


import numpy as np
import os
import pandas as pd

import xspec 
from xspec import *

from tqdm import tqdm 

def pyxspec_plot(): 

    import matplotlib.pyplot as plt

    all_ids = list(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/good_ids.csv')['full_id'])

    pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
    fak_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'

    plot_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/post-processing/initial/pds_plots/plot_dir'

    # fix above two

    Xset.chatter = 0
    #Xset.logChatter = 10
    Fit.query = "no"

    for full_id in tqdm(all_ids): 
        full_id = '1050360104_0'
        id_list = full_id.split('_')
        obs_id = id_list[0]
        gti = id_list[1]

        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', gti)

        fak_file = fak_temp.replace('+++', obs_id)
        fak_file = fak_file.replace('***', gti)

        s1 = Spectrum(pds_file)

        # fix path of spectrum files! 

        s1.ignore('**-0.02')
        s1.ignore('100.-**')

        m1 = Model("loren+loren")


        m1.lorentz.LineE = 0
        m1.lorentz.LineE.frozen = True
        m1.lorentz_2.LineE = 0
        m1.lorentz_2.LineE.frozen = True

        
        
        Fit.perform()


        Plot.splashPage = False

        Plot.xAxis = "keV"
        Plot("data")

        plot_path = plot_dir + '/' + obs_id + '.png'
        
        x = Plot.x()
        y = Plot.y()

        plt.style.use("/mnt/c/Users/Research/Documents/GitHub/sunnyhills/other/aesthetics/science.mplstyle")
        fig, ax = plt.subplots(figsize=(5,3))

        ax.scatter(x,y, s=3)

        ax.set(xlim=(1,20), xscale='log')#, yscale='log')

        plt.savefig(plot_path)


        break 


pyxspec_plot()