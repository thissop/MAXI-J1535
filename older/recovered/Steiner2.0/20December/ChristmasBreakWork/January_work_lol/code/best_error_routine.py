#Import(s)
from personalastropy.xspectools.XSPECtoolsv2 import *
import os
import re

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

all_tins = []
all_rpgs = []
returnFitResults(IDs=all_nthcomp_ids,path_temp=nlft,fit_stat='pgstat',fit_params=['diskbb:Tin:6'],out_lists=[all_tins],rfsl=all_rpgs)

cleaned_rpgs2 = []
cleaned_rpgs_only = []
for item in all_rpgs:
    item_list = item.split(':')
    rpg = float(item_list[1])
    if rpg < 1.4 and rpg > 0.6:
        cleaned_rpgs2.append(item_list[0])
        cleaned_rpgs_only.append(rpg)

bap = best_error_routine(IDs=cleaned_rpgs2,path_temp='/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/full_run_two/nthcomp/logs/error++++++++++_+.log',param_num=2,date_strings=nthcomp_mjds,value_strings=all_tins)




