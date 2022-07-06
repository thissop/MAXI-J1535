def returnDates(IDs,path_temp,out_list): 
    #Import(s)
    import astropy
    from astropy.io import fits
    import os
    import shutil

    #Action
    for item in IDs:
        obs_id = item.split('_')[0]
        gti = item.split('_')[1]
        seg_id = item
        path = path_temp.replace('++++++++++',obs_id)
        path = path.replace('+',gti)
        if os.path.exists(path)==True:
            orig = path
            target = path.replace('.jsgrp','(temp).fits') 
            shutil.copyfile(orig, target)
            hdul = fits.open(target)
            obsdate = float(hdul[1].header['MJDSTART'])
            out_list.append(str(seg_id)+':'+str(obsdate))
            os.remove(target)

def returnFitResults(IDs,path_temp,fit_stat,fit_params,out_lists,rfsl):
    #imports 
    import re
    import os

    #Action
    reducedfitstats = rfsl
    for item in IDs:
        obs_id = item.split('_')[0]
        gti = item.split('_')[1]
        seg_id = item
        path = path_temp.replace('++++++++++',obs_id)
        path = path.replace('+',gti)
        if os.path.exists(path) == True:
            for elem in fit_params:
                i = 0
                with open(path,'r') as f:
                    component = (elem.split(':'))[0]
                    for line in f:
                        if component in line:
                            parameter = (elem.split(':'))[1]
                            if parameter in line:
                                if i == 0:
                                    i = 1
                                    valueindex = int((elem.split(':'))[2])
                                    linelist = (re.sub(' +',',',line)).split(',')
                                    value = float(linelist[valueindex])
                                    elemindex = fit_params.index(elem)
                                    value = seg_id+':'+str(value)
                                    out_lists[elemindex].append(value)
        #Get fitstatistic
        with open(path,'r') as f:
            if fit_stat=='pgstat':
                listoflines = []
                for line in f:
                    listoflines.append(line.replace('\n',''))
                
                for element in listoflines:
                    if '#Fit statistic  : PG-Statistic' in element:
                        elementindex = int(listoflines.index(element))
                        elementlist = (re.sub(' +',',',element)).split(',')
                        fitstat = float(elementlist[4])
                        dofline = listoflines[(elementindex+3)]
                        doflinelist = (re.sub(' +',',',dofline)).split(',')
                        dof = float(doflinelist[7])
                        reducedfitstat = fitstat/dof
                        reducedfitstats.append(seg_id+':'+str(reducedfitstat))

def best_error_routine(IDs,path_temp,param_num,date_strings,value_strings):
    #   Parameter Definitions:
    #   IDs: list of seg_ids ('obsid:gti')
    #   path_temp: path template of the error files, with the obsid and gti replaced with plus-signs like this: '++++++++++_+.log' 
    #   param_num: integer, model parameter number of the parameter in question
    #   date_strings: an output list from returnDates(), with the same length as IDs
    #   value_strings: an output list from returnFitResults(), with the same length as IDs

    #   Returns: 
    #   [0]: dates for good error points
    #   [1]: values for good error points
    #   [2]: good error array (dimensions set for yerr of matplotlib)
    #   [3]: dates for cwz error points
    #   [4]: values for cwz points
    #   [5]: cwz error array (dimensions set for yerr of matplotlib) ----- PHLZ/PHUZ values are set to 0.0


    #Import(s)
    import numpy as np
    import string
    import re
    import os

    #Action

    #Get raw error results
    raw_error_results = []

    for item in IDs:
        obsid = item.split('_')[0]
        gti = item.split('_')[1]
        seg_id = item

        path = path_temp.replace('++++++++++',obsid)
        path = path.replace('+',gti)

        if os.path.exists(path) == True:
            temp_list = []
            alphabet_list = list(string.ascii_lowercase)
            with open(path,'r') as f:
                for line in f:
                    if any(element in line for element in alphabet_list):
                            continue
                    else:
                        if len(line) > 3:
                            line = line.replace('#','')
                            line = line.replace('\n','')
                            linelist = (re.sub(' +',',',line)).split(',')
                            linelist = linelist[1:]
                            if linelist[0] == str(param_num):
                                lower = linelist[3]
                                upper = linelist[4]
                                lower = lower.replace('(','')
                                upper = upper.replace(')','')
                                
                                if linelist[2] == '0':
                                    if linelist[1] != '0':
                                        upper = 'PHUZ'
                                        lowerandupper = str(abs(float(lower)))+':'+upper
                                        seg_id_and_ci = seg_id+':'+lowerandupper
                                        temp_list.append(seg_id_and_ci)
                                    else:
                                        lowerandupper='PHLZ:PHUZ'
                                        seg_id_and_ci = seg_id+':'+lowerandupper
                                        temp_list.append(seg_id_and_ci)
                                elif linelist[1] == '0':
                                    if linelist[2] != 0:
                                        lower = 'PHLZ'
                                        lowerandupper = lower+':'+str(abs(float(upper)))
                                        seg_id_and_ci = seg_id+':'+lowerandupper
                                        temp_list.append(seg_id_and_ci)
                                else:
                                    lowerandupper = str(abs(float(lower)))+':'+str(abs(float(upper)))
                                    seg_id_and_ci = seg_id+':'+lowerandupper
                                    temp_list.append(seg_id_and_ci)
                                
            if len(temp_list) == 0:
                failederrorstring = seg_id+':NaN:NaN'
                raw_error_results.append(failederrorstring)
                break
                
            else:
                for element in temp_list: 
                    if 'PHLZ' not in element:
                        if 'PHUZ' not in element: 
                            raw_error_results.append(element) 
                            break
                    if 'PHLZ' or 'PHUZ' in element:
                        raw_error_results.append(element) 
                        break

    #Process the raw error results, return clean and ready to go lists
    failed_errors = []
    cwz_errors = [] #consistent with zero vals
    good_errors = []

    for error_string in raw_error_results:
        error_string_list = error_string.split(':')
        if error_string_list[1] == 'PHLZ' or error_string_list[2] == 'PHUZ':
            cwz_errors.append(error_string)
        elif str(error_string_list[1]) != 'NaN':
            good_errors.append(error_string)
        else: 
            failed_errors.append(error_string)
    
    #get the good error 
    lowers = []
    uppers = []
    good_error_dates = []
    good_vals = []

    for error_string in good_errors:
        error_string_list = error_string.split(':')
        seg_id = error_string_list[0]
        lower = float(error_string_list[1])
        lowers.append(lower)
        upper = float(error_string_list[2])
        uppers.append(upper)
        for date_string in date_strings:
            date_string_list = date_string.split(':')
            if seg_id == date_string_list[0]:
                date = float(date_string_list[1])
                good_error_dates.append(date)
        for value_string in value_strings:
            value_string_list = value_string.split(':')
            if seg_id == value_string_list[0]: 
                value = float(value_string_list[1])
                good_vals.append(value)

    good_errors_array = np.array((lowers,uppers))
    
    #CWZ Errors
    cwz_lowers = []
    cwz_uppers = []
    cwz_error_dates = []
    cwz_vals = []

    for error_string in cwz_errors:
        error_string_list = error_string.split(':')
        seg_id = error_string_list[0]
        
        if error_string_list[1]=='PHLZ':
            cwz_lower = 0.0
        else:
            cwz_lower = float(error_string_list[1])

        cwz_lowers.append(cwz_lower)

        if error_string_list[2]=='PHUZ':
            cwz_upper = 0.0
        else:
            cwz_upper = float(error_string_list[2])
        
        cwz_uppers.append(cwz_upper)

        for date_string in date_strings:
            date_string_list = date_string.split(':')
            if seg_id == date_string_list[0]:
                date = float(date_string_list[1])
                cwz_error_dates.append(date)
        for value_string in value_strings:
            value_string_list = value_string.split(':')
            if seg_id == value_string_list[0]: 
                cwz_value = float(value_string_list[1])
                cwz_vals.append(cwz_value)

    good_errors_array = np.array((lowers,uppers))

    cwz_errors_array = np.array((cwz_lowers,cwz_uppers))

    return good_error_dates,good_vals,good_errors_array, cwz_error_dates, cwz_vals, cwz_errors_array