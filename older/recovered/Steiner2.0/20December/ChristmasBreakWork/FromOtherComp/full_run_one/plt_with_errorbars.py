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
        path3 = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/error++++++++++_+.log'
        path4 = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'

        obsid = line.split('_')[0]
        gti = line.split('_')[1]

        path_a = path1.replace('++++++++++',obsid)
        path_a = path_a.replace('+',gti)
        
        path_b = path2.replace('++++++++++',obsid)
        path_b = path_b.replace('+',gti)

        path_c = path3.replace('++++++++++',obsid)
        path_c = path_c.replace('+',gti)

        path_d = path4.replace('++++++++++',obsid)
        path_d = path_d.replace('+',gti)

        if os.path.exists(path_a)==True and os.path.exists(path_b)==True:
            if os.path.exists(path_c) == True and os.path.exists(path_d)==True:
                sids.append(line)
sids = list(set(sids))
#Investigate error

tins = []
rpgs = []
returnFitResults(IDs=sids,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/++++++++++_+.log',fit_stat='pgstat',fit_params=['Tin:diskbb:6'],out_lists=[tins],rfsl=rpgs)

final_seg_ids_list = []
for item in rpgs:
    floater = float(item.split(':')[1])
    if floater < 1.4 and floater > 0.6: #and floater > 0.98
        final_seg_ids_list.append(item.split(':')[0])

tins2 = []
gammas2 = []
rpgs2 = []
returnFitResults(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/++++++++++_+.log',fit_stat='pgstat',fit_params=['Tin:diskbb:6','Gamma:nthComp:5'],out_lists=[tins2,gammas2],rfsl=rpgs2)

tin_error_bars = []
gamma_error_bars = []
returnConfidenceIntervals(final_seg_ids_list,'/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/error++++++++++_+.log',param_nums=[2,4],out_lists=[tin_error_bars,gamma_error_bars])


mjds = []
returnDates(IDs=final_seg_ids_list,path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp',out_list=mjds)

cfluxes = []
cflux_rpgs = []
returnFitResults(final_seg_ids_list,'/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_one/logs/cflux_first40_++++++++++_+.log',fit_stat='pgstat',fit_params=['cflux:lg10Flux:6'],out_lists=[cfluxes],rfsl=cflux_rpgs)

cflux_dates = []
cflux_vals = []

for item in cfluxes:
    item_list = item.split(':')
    seg_id = item_list[0]
    for elem in mjds:
        elem_list = elem.split(':')
        if seg_id == elem_list[0]:
            cflux_dates.append(float(elem_list[1]))
            cflux_vals.append(float(item_list[1]))

#Do the tin error work
failed_tin_errors = []
cwz_tin_errors = [] #consistent with zero vals
good_tin_errors = []

for elem in tin_error_bars:
    elem_list = elem.split(':')
    if elem_list[1] == 'PHLZ' or elem_list[2] == 'PHUZ':
        cwz_tin_errors.append(elem)
    elif str(elem_list[1]) != 'NaN':
        good_tin_errors.append(elem)
    else: 
        failed_tin_errors.append(elem)

tin_lowers = []
tin_uppers = []
good_tin_error_dates = []
good_tin_vals = []

for elem in good_tin_errors:
    elem_list = elem.split(':')
    seg_id = elem_list[0]
    tin_lower = float(elem_list[1])
    tin_lowers.append(tin_lower)
    tin_upper = float(elem_list[2])
    tin_uppers.append(tin_upper)
    for element in mjds:
        if seg_id in element:
            date = float(element.split(':')[1])
            good_tin_error_dates.append(date)
    for element in tins2:
        if seg_id in element: 
            tin = float(element.split(':')[1])
            good_tin_vals.append(tin)

tin_errors = np.array((tin_lowers,tin_uppers))

#Do the gamma error work
failed_gamma_errors = []
cwz_gamma_errors = [] #consistent with zero vals
good_gamma_errors = []

for elem in gamma_error_bars:
    elem_list = elem.split(':')
    if elem_list[1] == 'PHLZ' or elem_list[2] == 'PHUZ':
        cwz_gamma_errors.append(elem)
    elif str(elem_list[1]) != 'NaN':
        good_gamma_errors.append(elem)
    else: 
        failed_gamma_errors.append(elem)

gamma_lowers = []
gamma_uppers = []
good_gamma_error_dates = []
good_gamma_vals = []

for elem in good_gamma_errors:
    elem_list = elem.split(':')
    seg_id = elem_list[0]
    gamma_lower = float(elem_list[1])
    gamma_lowers.append(gamma_lower)
    gamma_upper = float(elem_list[2])
    gamma_uppers.append(gamma_upper)
    for element in mjds:
        if seg_id in element:
            date = float(element.split(':')[1])
            good_gamma_error_dates.append(date)
    for element in gammas2:
        if seg_id in element: 
            gamma = float(element.split(':')[1])
            good_gamma_vals.append(gamma)

gamma_errors = np.array((gamma_lowers,gamma_uppers))

#Plot

fig, axs = plt.subplots(5,1,sharex=True)

#axs[1].plot(cflux_dates,cflux_vals,color='indianred',alpha=0.3,lw=1)
axs[1].plot(cflux_dates,cflux_vals,color='indianred',lw=0,marker='o',ms=3)

axs[2].errorbar(good_gamma_error_dates,good_gamma_vals,yerr=gamma_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
axs[2].set_ylabel(r'$\Gamma$')

axs[3].errorbar(good_tin_error_dates,good_tin_vals,yerr=tin_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
axs[3].set_ylabel(('k'+r'$T_{in}$'))

axs[4].set_xlabel('Time (MJD)')

plt.subplots_adjust(hspace=0)
plt.show()

