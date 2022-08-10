#Import(s)
import os
import re
from personalastropy.xspectools.XSPECtoolsv2 import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#Action

dpt = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
nlft = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/++++++++++_+.log'

#Get nthcomp information
#get ids
all_nthcomp_ids = []
with open('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/all_seg_ids.txt','r') as f:
    for line in f:
        if '#' not in line:
            line = line.replace('\n','')
            line_list = line.split('_')
            obsid = line_list[0]
            gti = line_list[1]
            
            data_path_temp = dpt
            data_path = data_path_temp.replace('++++++++++',obsid)
            data_path = data_path.replace('+',gti)
            
            log_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/++++++++++_+.log'
            log_file = log_temp.replace('++++++++++',obsid)
            log_file = log_file.replace('+',gti)

            if os.path.exists(data_path)==True and os.path.exists(log_file)==True:
                with open(log_file,'r') as f2:
                    for line2 in f2:
                        if '#Net count rate (cts/s) for Spectrum:1' in line2:
                            line_list2 = (re.sub(' +',',',line2)).split(',')
                            file_frac = line_list2[9]
                            if '(' in file_frac:
                                file_frac = float(file_frac.replace('(',''))
                                if file_frac > 50:
                                    all_nthcomp_ids.append(line)

all_nthcomp_ids = list(set(all_nthcomp_ids))

nthcomp_mjds = []
returnDates(all_nthcomp_ids,dpt,nthcomp_mjds)

#get count_rates 
count_rates = []
returnCountRates(all_nthcomp_ids,dpt,['50:999'],bg_path_temp=dpt.replace('.jsgrp','.bg'),out_list=count_rates)

count_rates_only = []
count_rate_dates = []
for item in count_rates:
    item_list = item.split(':')
    count_rate = float(item_list[1])
    count_rates_only.append(count_rate)
    for elem in nthcomp_mjds:
        elem_list = elem.split(':')
        if item_list[0]==elem_list[0]:
            count_rate_dates.append(float(elem_list[1]))

#get the nthcomp error_results
all_tins = []
all_diskbb_norms = []
all_gammas = []
all_nthcomp_norms = []
all_rpgs = []

returnFitResults(IDs=all_nthcomp_ids,path_temp=nlft,fit_stat='pgstat',fit_params=['diskbb:Tin:6','diskbb:norm:5','nthComp:Gamma:5','nthComp:norm:5'],out_lists=[all_tins,all_diskbb_norms,all_gammas,all_nthcomp_norms],rfsl=all_rpgs)

cleaned_rpgs2 = []
cleaned_rpgs_only = []
for item in all_rpgs:
    item_list = item.split(':')
    rpg = float(item_list[1])
    if rpg < 1.4 and rpg > 0.6:
        cleaned_rpgs2.append(item_list[0])
        cleaned_rpgs_only.append(rpg)

raw_tin_error_results = []
raw_gamma_error_results = []
raw_diskbb_norm_error_results = []
raw_nthcomp_norm_error_results = []

#Get 'raw' error results
elf_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/error++++++++++_+.log'
returnConfidenceIntervals(IDs=all_nthcomp_ids,path_temp=elf_temp,param_nums=[2,4,3,9],out_lists=[raw_tin_error_results,raw_gamma_error_results,raw_diskbb_norm_error_results,raw_nthcomp_norm_error_results])


#Get cleaned values with errorbars
tin_clean = returnCleanErrorResults(x=raw_tin_error_results,y=nthcomp_mjds,z=all_tins)

final_tin_dates = tin_clean[0]
final_tin_vals = tin_clean[1]
final_tin_errors = tin_clean[2]

gamma_clean = returnCleanErrorResults(x=raw_gamma_error_results,y=nthcomp_mjds,z=all_gammas)

final_gamma_dates = gamma_clean[0]
final_gamma_vals = gamma_clean[1]
final_gamma_errors = gamma_clean[2]

diskbb_norm_clean = returnCleanErrorResults(x=raw_diskbb_norm_error_results,y=nthcomp_mjds,z=all_diskbb_norms)
final_diskbb_norm_dates = diskbb_norm_clean[0]
final_diskbb_norm_vals = diskbb_norm_clean[1]
final_diskbb_norm_errors = diskbb_norm_clean[2]

nthcomp_norm_clean = returnCleanErrorResults(x=raw_nthcomp_norm_error_results,y=nthcomp_mjds,z=all_nthcomp_norms)
final_nthcomp_norm_dates = nthcomp_norm_clean[0]
final_nthcomp_norm_vals = nthcomp_norm_clean[1]
final_nthcomp_norm_errors = nthcomp_norm_clean[2]

#total flux

cfluxes = []
c_rpgs = []
returnFitResults(IDs=all_nthcomp_ids,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/cflux++++++++++_+.log',fit_stat='pgstat',fit_params=['lg10Flux:cflux:6'],out_lists=[cfluxes],rfsl=c_rpgs)

raw_cflux_error_results = []
returnConfidenceIntervals(IDs=cleaned_rpgs2,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/cflux_error++++++++++_+.log',param_nums=[4],out_lists=[raw_cflux_error_results])
cer_clean = returnCleanErrorResults(x=raw_cflux_error_results,y=nthcomp_mjds,z=cfluxes) # it said cfluxes but that wasn't defined? 

cer_dates = cer_clean[0]
cer_vals = cer_clean[1]
cer_errors = cer_clean[2]

###########
#get cwz error arrays and such for them

cwz_tin_dates = tin_clean[3]
cwz_tin_vals = tin_clean[4]

cwz_gamma_dates = gamma_clean[3]
cwz_gamma_vals = gamma_clean[4]

cwz_diskbb_norm_dates = diskbb_norm_clean[3]
cwz_diskbb_norm_vals = diskbb_norm_clean[4]

cwz_nthcomp_norm_dates = nthcomp_norm_clean[3]
cwz_nthcomp_norm_vals = nthcomp_norm_clean[4]

#cwz total flux

cwz_cer_dates = cer_clean[3]
cwz_cer_vals = cer_clean[4]

#########


#get reduced pg-stat values for all nthcomp dates

rpgs_dates_only = []
for item in cleaned_rpgs2:
    for elem in nthcomp_mjds:
        elem_list = elem.split(':')
        if elem_list[0]==item:
            rpgs_dates_only.append(float(elem_list[1]))



#Get sipl information
all_simpl_ids = []
with open('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/all_seg_ids.txt','r') as f:
    for line in f:
        if '#' not in line:
            line = line.replace('\n','')
            line_list = line.split('_')
            obsid = line_list[0]
            gti = line_list[1]
            
            data_path_temp = dpt
            data_path = data_path_temp.replace('++++++++++',obsid)
            data_path = data_path.replace('+',gti)
            
            log_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/simpl/logs/simpl++++++++++_+.log'
            log_file = log_temp.replace('++++++++++',obsid)
            log_file = log_file.replace('+',gti)

            if os.path.exists(data_path)==True and os.path.exists(log_file)==True:
                all_simpl_ids.append(line)
all_simpl_ids = list(set(all_simpl_ids))

simpl_log_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/simpl/logs/simpl++++++++++_+.log'
simpl_error_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/simpl/logs/simpl_error++++++++++_+.log'

frac_sctrs = []
simpl_rpgs = []
returnFitResults(IDs=all_simpl_ids,path_temp=simpl_log_temp,fit_stat='pgstat',fit_params=['simpl:FracSctr:5'],out_lists=[frac_sctrs],rfsl=simpl_rpgs)

simpl_ids2 = []
for item in simpl_rpgs:
    item_list = item.split(':')
    seg_id = item_list[0]
    rpg = float(item_list[1])
    if rpg > 0.6 and rpg < 1.4:
        simpl_ids2.append(seg_id)

frac_sctrs2 = []
simpl_rpgs2 = []
returnFitResults(IDs=simpl_ids2,path_temp=simpl_log_temp,fit_stat='pgstat',fit_params=['simpl:FracSctr:5'],out_lists=[frac_sctrs2],rfsl=simpl_rpgs2)

fs_ebs = []
returnConfidenceIntervals(IDs=simpl_ids2,path_temp=simpl_error_temp,param_nums=[3],out_lists=[fs_ebs])

simpl_mjds = []
returnDates(simpl_ids2,dpt,simpl_mjds)

#Extract error information for simpl
failed_fs_errors = []
cwz_fs_errors = [] #consistent with zero vals
good_fs_errors = []

for elem in fs_ebs:
    elem_list = elem.split(':')
    if elem_list[1] == 'PHLZ' or elem_list[2] == 'PHUZ':
        cwz_fs_errors.append(elem)
    elif str(elem_list[1]) != 'NaN':
        good_fs_errors.append(elem)
    else: 
        failed_fs_errors.append(elem)

fs_lowers = []
fs_uppers = []
good_fs_error_dates = []
good_fs_vals = []
good_fs_rpgs = []

for elem in good_fs_errors:
    elem_list = elem.split(':')
    seg_id = elem_list[0]
    fs_lower = float(elem_list[1])
    fs_lowers.append(fs_lower)
    fs_upper = float(elem_list[2])
    fs_uppers.append(fs_upper)
    for element in simpl_mjds:
        element_list = element.split(':')
        if seg_id == element_list[0]:
            date = float(element.split(':')[1])
            good_fs_error_dates.append(date)
    for element in frac_sctrs2:
        element_list = element.split(':')
        if seg_id == element_list[0]: 
            frac_scat = float(element.split(':')[1])
            good_fs_vals.append(100*frac_scat)
    for element in simpl_rpgs2:
        element_list = element.split(':')
        if seg_id == element_list[0]:
            rpg = float(element_list[1])
            good_fs_rpgs.append(rpg)

fs_errors = 100*np.array((fs_lowers,fs_uppers))

######
#Get cwz vals and dates
cwz_fs_dates = []
cwz_fs_vals = []
cwz_fs_rpgs = []

for elem in cwz_fs_errors:
    elem_list = elem.split(':')
    seg_id = elem_list[0]
    for element in simpl_mjds:
        element_list = element.split(':')
        if seg_id == element_list[0]:
            date = float(element.split(':')[1])
            cwz_fs_dates.append(date)
    for element in frac_sctrs2:
        element_list = element.split(':')
        if seg_id == element_list[0]: 
            frac_scat = float(element.split(':')[1])
            cwz_fs_vals.append(100*frac_scat)
    for element in simpl_rpgs2:
        element_list = element.split(':')
        if seg_id == element_list[0]:
            rpg = float(element_list[1])
            cwz_fs_rpgs.append(rpg)
######

#Plot it all!
def cuneo_plot():
    fig, axs = plt.subplots(7,1,sharex=True)
    for i in range(0,7):
        axs[i].tick_params(axis='both',which='major',labelsize=4)

    #Count rate (c/s)
    axs[0].scatter(count_rate_dates,count_rates_only,c='indianred',marker='o',s=3,label='NICER (0.5-10 keV)')
    axs[0].set_ylabel('Count rate (c/s)',fontsize=4)
    axs[0].set_ylim(bottom=0)
    axs[0].set_yscale('symlog')
    axs[0].set_yticks(ticks=[1,10,100,1000])
    axs[0].legend(loc='upper right',fontsize=4)

    #Unabs. Flux
    axs[1].scatter(cwz_cer_dates,cwz_cer_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[1].errorbar(cer_dates,cer_vals,yerr=cer_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[1].set_ylabel('Unabs. Total '+r'$F_{\chi}$',fontsize=4)
    axs[1].set_yticks(ticks=[-11,-10,-9,-8,-7])
    axs[1].set_yticklabels(labels=[r'$10^{-11}$',r'$10^{-10}$',r'$10^{-9}$',r'$10^{-8}$',r'$10^{-7}$'])
    axs[1].yaxis.set_minor_locator(MultipleLocator(0.5))
    axs[1].set_ylim(-12,-6)

    #Compt. F_{\chi} (%)
    axs[2].scatter(cwz_fs_dates,cwz_fs_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[2].errorbar(good_fs_error_dates,good_fs_vals,yerr=fs_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[2].set_ylabel('Compt. '+r'$F_{\chi}$'+' (%)',fontsize=4)
    axs[2].set_yticks([0,50,100])
    axs[2].set_ylim(-20,120)
    axs[2].yaxis.set_minor_locator(MultipleLocator(10))

    #Inner Disk Temp
    axs[3].scatter(cwz_tin_dates,cwz_tin_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[3].errorbar(final_tin_dates,final_tin_vals,yerr=final_tin_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[3].set_ylabel('k'+r'$T_{in}$'+'(keV)',fontsize=4)
    axs[3].set_yticks([0.0,0.2,0.4,0.6])
    axs[3].yaxis.set_minor_locator(MultipleLocator(0.1))
    axs[3].set_ylim(-0.1,0.7)
   
    #Gamma
    axs[4].scatter(cwz_gamma_dates,cwz_gamma_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[4].errorbar(final_gamma_dates,final_gamma_vals,yerr=final_gamma_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[4].set_ylabel(r'$\Gamma$',fontsize=4)
    axs[4].set_yticks([1.5,2,2.5])
    axs[4].yaxis.set_minor_locator(MultipleLocator(0.25))
    axs[4].set_ylim(1,3)

    #nhtcomp red. \chi^{2} plot
    axs[5].scatter(rpgs_dates_only,cleaned_rpgs_only,color='indianred',s=3,marker='o',label='nthcomp model')
    x_vals = np.linspace((min(good_fs_error_dates)),(max(good_fs_error_dates)),5)
    y_vals = np.array([1,1,1,1,1])
    axs[5].plot(x_vals,y_vals,color='lightgrey',lw=1)
    axs[5].set_ylabel('Red. '+r'$\chi^{2}$',fontsize=4)
    axs[5].yaxis.set_minor_locator(MultipleLocator(0.05))
    axs[5].set_yticks([0.6,0.8,1,1.2,1.4])
    axs[5].set_ylim(0.4,1.6)
    axs[5].legend(loc='upper right',fontsize=4)

    #Simpl red. \chi^{2} plot
    axs[6].scatter(cwz_fs_dates,cwz_fs_rpgs,color='indianred',s=3,marker='o')
    axs[6].scatter(good_fs_error_dates,good_fs_rpgs,color='indianred',s=3,marker='o',label='simpl model')
    x_vals = np.linspace((min(good_fs_error_dates)),(max(good_fs_error_dates)),5)
    y_vals = np.array([1,1,1,1,1])
    axs[6].plot(x_vals,y_vals,color='lightgrey',lw=1)
    axs[6].set_ylabel('Red. '+r'$\chi^{2}$',fontsize=4)
    axs[6].yaxis.set_minor_locator(MultipleLocator(0.05))
    axs[6].set_yticks([0.6,0.8,1,1.2,1.4])
    axs[6].set_ylim(0.4,1.6)
    axs[6].legend(loc='upper right',fontsize=4)
    axs[6].set_xlabel('Time (MJD)',fontsize=5)
    axs[6].xaxis.set_minor_locator(MultipleLocator(20))


    plt.subplots_adjust(hspace=0)
    plt.show()

def nthcomp_plot():
    fig, axs = plt.subplots(7,1,sharex=True)
    for i in range(0,7):
        axs[i].tick_params(axis='both',which='major',labelsize=4)

    #Count rate (c/s)
    axs[0].scatter(count_rate_dates,count_rates_only,c='indianred',marker='o',s=3,label='NICER (0.5-10 keV)')
    axs[0].set_ylabel('Count rate (c/s)',fontsize=4)
    axs[0].set_ylim(bottom=0)
    axs[0].set_yscale('symlog')
    axs[0].set_yticks(ticks=[1,10,100,1000])
    axs[0].legend(loc='upper right',fontsize=4)

    #Unabs. Flux
    axs[1].scatter(cwz_cer_dates,cwz_cer_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[1].errorbar(cer_dates,cer_vals,yerr=cer_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[1].set_ylabel('Unabs. Total '+r'$F_{\chi}$',fontsize=4)
    axs[1].set_yticks(ticks=[-11,-10,-9,-8,-7])
    axs[1].set_yticklabels(labels=[r'$10^{-11}$',r'$10^{-10}$',r'$10^{-9}$',r'$10^{-8}$',r'$10^{-7}$'])
    axs[1].yaxis.set_minor_locator(MultipleLocator(0.5))
    axs[1].set_ylim(-12,-6)

    #Inner Disk Temp
    axs[2].scatter(cwz_tin_dates,cwz_tin_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[2].errorbar(final_tin_dates,final_tin_vals,yerr=final_tin_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[2].set_ylabel('k'+r'$T_{in}$'+'(keV)',fontsize=4)
    axs[2].set_yticks([0.0,0.2,0.4,0.6])
    axs[2].yaxis.set_minor_locator(MultipleLocator(0.1))
    axs[2].set_ylim(-0.1,0.7)
   
    #Gamma
    axs[3].scatter(cwz_gamma_dates,cwz_gamma_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[3].errorbar(final_gamma_dates,final_gamma_vals,yerr=final_gamma_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[3].set_ylabel(r'$\Gamma$',fontsize=4)
    axs[3].set_yticks([1.5,2,2.5])
    axs[3].yaxis.set_minor_locator(MultipleLocator(0.25))
    axs[3].set_ylim(1,3)

    #diskbb norm
    axs[4].scatter(cwz_diskbb_norm_dates,cwz_diskbb_norm_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[4].errorbar(final_diskbb_norm_dates,final_diskbb_norm_vals,yerr=final_diskbb_norm_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[4].set_ylabel('diskbb norm',fontsize=4)
    axs[4].set_yscale('log')

    #nthcomp norm
    axs[5].scatter(cwz_nthcomp_norm_dates,cwz_nthcomp_norm_vals,s=3,color='forestgreen',alpha=0.8,marker='^')
    axs[5].errorbar(final_nthcomp_norm_dates,final_nthcomp_norm_vals,yerr=final_nthcomp_norm_errors,elinewidth=0.5,lw=0,ms=3,marker='o',color='indianred')
    axs[5].set_ylabel('nthcomp norm',fontsize=4)
    axs[5].set_yscale('log')

    #nhtcomp red. \chi^{2} plot
    axs[6].scatter(rpgs_dates_only,cleaned_rpgs_only,color='indianred',s=3,marker='o',label='nthcomp model')
    x_vals = np.linspace((min(good_fs_error_dates)),(max(good_fs_error_dates)),5)
    y_vals = np.array([1,1,1,1,1])
    axs[6].plot(x_vals,y_vals,color='lightgrey',lw=1)
    axs[6].set_ylabel('Red. '+r'$\chi^{2}$',fontsize=4)
    axs[6].yaxis.set_minor_locator(MultipleLocator(0.05))
    axs[6].set_yticks([0.6,0.8,1,1.2,1.4])
    axs[6].set_ylim(0.4,1.6)
    axs[6].legend(loc='upper right',fontsize=4)

    plt.subplots_adjust(hspace=0)
    plt.show()


def write_temp_and_lumin():
    #Import(s)
    import pandas as pd
    
    #Action
    zipped_list = list(zip(final_tin_vals,cer_vals))

    df = pd.DataFrame(zipped_list,columns=['Temp (keV)','Luminosity (log10Flux: erg/cm^{2}/s'])
    df.to_csv('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/temp_vs_lumin.csv',index=False)


#nthcomp_plot()

'''
LOL. Coming back to this on July 8th, 2021, ~7 months later to use the data
from this routine. 
'''

def extract_and_return_data():
    # Import(s)
    import pandas as pd
    import numpy as np
    
    # Action
    
    zipped = list(zip(count_rate_dates, count_rates_only, cer_dates, cer_vals, 
                      final_tin_dates, final_tin_vals, rpgs_dates_only, 
                      cleaned_rpgs_only, final_gamma_dates,final_gamma_vals))

    col_names = ['count_rate_dates', 'count_rates_only', 'cer_dates', 'cer_vals', 
                 'final_tin_dates', 'final_tin_vals', 'rpgs_dates_only', 
                'cleaned_rpgs_only', 'final_gamma_dates', 'final_gamma_vals']
                
    df = pd.DataFrame(zipped, columns=col_names)
    fp = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/first_network/using_dec_data/dec_results.csv'
    df.to_csv(fp, index=False)
    
extract_and_return_data()

    
    
    