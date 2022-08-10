#Import(s)
import os
from personalastropy.xspectools.XSPECtoolsv2 import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

#Action
def exp_times(seg_ids,path_temp):
    #Import(s)
    import astropy
    from astropy.io import fits
    import os
    import shutil
    import matplotlib.pyplot as plt 
    import seaborn as sns


    #Action
    etl = []
    
    for seg_id in seg_ids:
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        path = path_temp.replace('**********',obsid)
        path = path.replace('*',gti)
        if os.path.exists(path)==True: 
            orig = path
            target = path.replace('.jsgrp','(temp).fits')
            shutil.copyfile(orig, target)
            hdul = fits.open(target)
            exp_time = float(hdul[1].header['EXPOSURE'])
            etl.append(exp_time)
            os.remove(target)
            
    def plot_hist(x):
        sns.set_style('darkgrid')
        plt.hist(x)
        plt.xlabel('Exposure Time')
        plt.ylabel('Frequency')
        plt.show()
        plt.clf()

    plot_hist(etl)

def good_seg_ids(seg_ids,path_temp):
    #Import(s)
    import os
    import re

    #Action
    good_sids = []
    for seg_id in seg_ids:
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        path = path_temp.replace('**********',obsid)
        path = path.replace('*',gti)
        if os.path.exists(path)==True:  
            with open(path,'r') as f:
                for line in f:
                    if '#  Exposure Time:' in line: 
                        linelist = (re.sub(' +',',',line)).split(',')
                        exp_time = float(linelist[3])
                    if '#Net count rate (cts/s) for Spectrum' in line:
                        linelist = (re.sub(' +',',',line)).split(',')
                        ncr = float(linelist[9].replace('(',''))
        
            if exp_time > 100.0 and ncr > 50.0:
                    good_sids.append(seg_id)

    return good_sids

def plot_good_seg_ids(seg_ids,path_temp):
    #Import(s)
    import os

    #Action
    for seg_id in seg_ids:
        ls = seg_id.split('_')
        obs_id = ls[0]
        gti = ls[1]




#Action
'''EXECUTION ZONE'''
sids = []
with open('/home/thaddaeus/FMU/Steiner2.0/permanent/ALL_NICER_IDs.txt','r') as f:
    for line in f:
        if '#' not in line: 
            obsid = line.replace('\n','')
            path_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/**********/jspipe/js_ni**********_0mpu7_silver_GTI*.jsgrp'
            path = path_temp.replace('**********',obsid)
            for i in range(0,30):
                path = path.replace('*',str(i))
                if os.path.exists(path) == True:
                    seg_id = obsid+'_'+str(i)
                    sids.append(seg_id)

"""RUN FUNCS"""

iddds = []

with open('test.txt','r') as f:
    for line in f:
        line = line.replace('\n','')
        iddds.append(line)
gammas = []
tins = []
rpgs = []
returnFitResults(IDs=iddds,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/logs/++++++++++_GTI+.log',fit_stat='pgstat',fit_params=['Gamma:nthcomp:5','Tin:diskbb:6'],out_lists=[gammas,tins],rfsl=rpgs)


final_seg_ids_list = []
for item in rpgs:
    floater = float(item.split(':')[1])
    if floater < 1.975: #and floater > 0.98
        final_seg_ids_list.append(item.split(':')[0])

for elem in final_seg_ids_list:
    print(elem)
print(len(final_seg_ids_list))

gammas2 = []
tins2 = []
rpgs2 = []
returnFitResults(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/logs/++++++++++_GTI+.log',fit_stat='pgstat',fit_params=['Gamma:nthComp:5','Tin:diskbb:6'],out_lists=[gammas2,tins2],rfsl=rpgs2)

gammas3 = []
tins3 = []
rpgs3 = []

for item in gammas2:
    item = float(item.split(':')[1])
    gammas3.append(item)

for item in tins2:
    item = float(item.split(':')[1])
    tins3.append(item)

for item in rpgs2:
    item = float(item.split(':')[1])
    rpgs3.append(item)

mjds = []
returnDates(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp',out_list=mjds)

mjds2 = []
for item in mjds:
    item = float(item.split(':')[1])
    mjds2.append(item)

print(len(gammas3),len(tins3),len(rpgs3),len(mjds2))

bap = [gammas3,tins3,rpgs3,mjds2]
for item in bap:
    item = np.array(item)

sns.set_style('darkgrid')
fig, axs = plt.subplots(3,1,sharex=True)
axs[0].plot(mjds2,gammas3,color='tomato',ms=3,lw=1,alpha=0.5)
axs[0].plot(mjds2,gammas3,color='tomato',marker='o',ms=3,lw=1)
axs[0].set_ylabel('Gamma')
axs[0].xaxis.set_minor_locator(MultipleLocator(10))
axs[0].yaxis.set_minor_locator(MultipleLocator(0.2))

axs[1].plot(mjds2,tins3,color='seagreen',ms=3,lw=1,alpha=0.5)
axs[1].plot(mjds2,tins3,color='seagreen',marker='o',ms=3,lw=0)
axs[1].set_ylabel('Tin')
axs[1].xaxis.set_minor_locator(MultipleLocator(10))
axs[1].yaxis.set_minor_locator(MultipleLocator(0.1))

axs[2].scatter(mjds2,rpgs3,label='0.98-1.10',c='grey',s=3)
axs[2].legend()
axs[2].set_xlabel('Date (MJD)')
axs[2].set_ylabel('Red. pgstat')
axs[2].xaxis.set_minor_locator(MultipleLocator(10))
axs[2].yaxis.set_minor_locator(MultipleLocator(0.3))

plt.show()

print(final_seg_ids_list)

