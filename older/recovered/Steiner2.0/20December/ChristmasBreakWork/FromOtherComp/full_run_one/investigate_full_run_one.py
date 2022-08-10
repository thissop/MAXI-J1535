#Import(s)
import os
from personalastropy.xspectools.XSPECtoolsv2 import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

#Action

#Get ids
sids = []
with open('/home/thaddaeus/FMU/Steiner/ChristmasBreak/all_seg_ids.txt','r') as f:
    for line in f:
        line = line.replace('\n','')
        
        path1 = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/++++++++++_+.log'
        path2 = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/cflux++++++++++_+.log'
        
        obsid = line.split('_')[0]
        gti = line.split('_')[1]

        path_a = path1.replace('++++++++++',obsid)
        path_a = path_a.replace('+',gti)
        
        path_b = path2.replace('++++++++++',obsid)
        path_b = path_b.replace('+',gti)

        if os.path.exists(path_a)==True and os.path.exists(path_b)==True:
            sids.append(line)

#Simple plot

'/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/cflux1050360103_0.log'

gammas = []
tins = []
rpgs = []
returnFitResults(IDs=sids,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/++++++++++_+.log',fit_stat='pgstat',fit_params=['Gamma:nthcomp:5','Tin:diskbb:6'],out_lists=[gammas,tins],rfsl=rpgs)

cfluxes = []
c_rpgs = []
returnFitResults(IDs=sids,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/cflux++++++++++_+.log',fit_stat='pgstat',fit_params=['lg10Flux:cflux:6'],out_lists=[cfluxes],rfsl=c_rpgs)

for item in cfluxes:
    print(item)

final_seg_ids_list = []
for item in rpgs:
    floater = float(item.split(':')[1])
    if floater < 1.4 and floater > 0.6: #and floater > 0.98
        final_seg_ids_list.append(item.split(':')[0])

for elem in final_seg_ids_list:
    print(elem)
print(len(final_seg_ids_list))

gammas2 = []
tins2 = []
rpgs2 = []
returnFitResults(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/++++++++++_+.log',fit_stat='pgstat',fit_params=['Gamma:nthComp:5','Tin:diskbb:6'],out_lists=[gammas2,tins2],rfsl=rpgs2)

cfluxes2 = []
c_rpgs2 = []
returnFitResults(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/cflux++++++++++_+.log',fit_stat='pgstat',fit_params=['lg10Flux:cflux:6'],out_lists=[cfluxes2],rfsl=c_rpgs2)


gammas3 = []
tins3 = []
rpgs3 = []

cfluxes3 = []

for item in gammas2:
    item = float(item.split(':')[1])
    gammas3.append(item)

for item in tins2:
    item = float(item.split(':')[1])
    tins3.append(item)

for item in rpgs2:
    item = float(item.split(':')[1])
    rpgs3.append(item)

for item in cfluxes2:
    item = float(item.split(':')[1])
    cfluxes3.append(item)

mjds = []
returnDates(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp',out_list=mjds)

mjds2 = []
for item in mjds:
    item = float(item.split(':')[1])
    mjds2.append(item)

print(len(gammas3),len(tins3),len(cfluxes3),len(rpgs3),len(mjds2))

bap = [gammas3,tins3,cfluxes3,rpgs3,mjds2]
for item in bap:
    item = np.array(item)


#Plot up the results

fig, axs = plt.subplots(4,1,sharex=True)

axs[0].plot(mjds2,cfluxes3,color='maroon',alpha=0.3,lw=1)
axs[0].plot(mjds2,cfluxes3,color='maroon',lw=0,marker='o',ms=3)
axs[0].set_ylabel('Unabs. Total F'+r'$F_{\chi}$')
axs[0].xaxis.set_minor_locator(MultipleLocator(20))
axs[0].yaxis.set_minor_locator(MultipleLocator(0.3))


axs[1].plot(mjds2,gammas3,color='tomato',ms=3,alpha=0.3,lw=1)
axs[1].plot(mjds2,gammas3,color='tomato',marker='o',ms=3,lw=0)
axs[1].set_ylabel(r'$\Gamma$')
axs[1].xaxis.set_minor_locator(MultipleLocator(20))
axs[1].yaxis.set_minor_locator(MultipleLocator(0.5))

axs[2].plot(mjds2,tins3,color='seagreen',ms=3,lw=1,alpha=0.3)
axs[2].plot(mjds2,tins3,color='seagreen',marker='o',ms=3,lw=0)
axs[2].set_ylabel(('k'+r'$T_{in}$'+'(keV)'))
axs[2].xaxis.set_minor_locator(MultipleLocator(20))
axs[2].yaxis.set_minor_locator(MultipleLocator(0.1))

axs[3].scatter(mjds2,rpgs3,label='0.98-1.10',c='indianred',s=3)
x_vals = np.linspace(min(mjds2)-30,max(mjds2)+30,4)
y_vals = np.array([1,1,1,1])
axs[3].plot(x_vals,y_vals,color='grey',lw=1) 
axs[3].legend()
axs[3].set_xlabel('Time (MJD)')
axs[3].set_ylabel(('Red. '+r'$\chi^{2}$'))
axs[3].xaxis.set_minor_locator(MultipleLocator(20))
axs[3].yaxis.set_minor_locator(MultipleLocator(0.15))

plt.show()

print(final_seg_ids_list)