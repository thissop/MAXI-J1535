def returnConfidenceIntervals(IDs,path_temp,param_nums,out_lists):
    #Import(s)
    import string
    import re
    import os

    #Action
    for item in IDs:
        obsid = item
        path = path_temp.replace('++++++++++',obsid)
        if os.path.exists(path) == True:
            for elem in param_nums:
                temporarylist = []
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
                                if linelist[0] == str(elem):
                                    lower = linelist[3]
                                    upper = linelist[4]
                                    lower = lower.replace('(','')
                                    upper = upper.replace(')','')
                                    
                                    if linelist[2] == '0':
                                        if linelist[1] != '0':
                                            upper = 'PHUZ'
                                            lowerandupper = str(abs(float(lower)))+':'+upper
                                            obsidandci = str(obsid)+':'+lowerandupper
                                            temporarylist.append(obsidandci)
                                        else:
                                            lowerandupper='PHLZ:PHUZ'
                                            obsidandci = str(obsid)+':'+lowerandupper
                                            temporarylist.append(obsidandci)
                                    elif linelist[1] == '0':
                                        if linelist[2] != 0:
                                            lower = 'PHLZ'
                                            lowerandupper = lower+':'+str(abs(float(upper)))
                                            obsidandci = str(obsid)+':'+lowerandupper
                                            temporarylist.append(obsidandci)
                                    else:
                                        lowerandupper = str(abs(float(lower)))+':'+str(abs(float(upper)))
                                        obsidandci = str(obsid)+':'+lowerandupper
                                        temporarylist.append(obsidandci)
                                    
                if len(temporarylist) == 0:
                    failederrorstring = str(obsid)+':NaN:NaN'
                    out_lists[(param_nums.index(elem))].append(failederrorstring)
                    break

                else:
                    for element in temporarylist: 
                        if 'PHLZ' not in element:
                            if 'PHUZ' not in element: 
                                out_lists[(param_nums.index(elem))].append(element) 
                                break
                        if 'PHLZ' or 'PHUZ' in element:
                            out_lists[(param_nums.index(elem))].append(element) 
                            break

def returnCountRates(IDs,path_temp,channel_ints,out_list): 
    #Import(s)
    import numpy as np
    from astropy.io import fits
    import os
    import shutil

    #Action 
    for item in IDs:
        obsid = item
        path = path_temp.replace('++++++++++',obsid)
        if os.path.exists(path)==True:
            orig = path
            temp_file = path.replace('.jsgrp','(temp).fits') 
            shutil.copyfile(orig, temp_file)
            hdul = fits.open(temp_file)
            channels_list = hdul[1].data['CHANNEL']
            counts_list = hdul[1].data['COUNTS']
            exp_time = float(hdul[1].header['EXPOSURE'])
            
            restricted_counts_list = []

            for elem in channel_ints:
                sub_interval = np.array([])
                l_index = int((elem.split(':'))[0])
                u_index = int((elem.split(':'))[1])
                sub_interval = list(counts_list[l_index:u_index])
                restricted_counts_list.extend(sub_interval)

            count_rate = sum(restricted_counts_list)/exp_time
            os.remove(temp_file)

            out_list.append((obsid+':'+str(count_rate)))

def returnDates(IDs,path_temp,out_list): 
    #Import(s)
    import astropy
    from astropy.io import fits
    import os
    import shutil

    #Action
    for item in IDs:
        obsid = item
        path = path_temp.replace('++++++++++',obsid)
        if os.path.exists(path)==True:
            orig = path
            target = path.replace('.jsgrp','(temp).fits') 
            shutil.copyfile(orig, target)
            hdul = fits.open(target)
            obsdate = float(hdul[1].header['MJDSTART'])
            out_list.append(str(obsid)+':'+str(obsdate))
            os.remove(target)

def returnFitResults(IDs,path_temp,fit_stat,fit_params,out_lists,rfsl):
    #imports 
    import re
    import os

    #Action
    reducedfitstats = rfsl
    for item in IDs:
        obsid = item
        path = path_temp.replace('++++++++++',obsid)
        if os.path.exists(path) == True:
            for elem in fit_params:
                with open(path,'r') as f:
                    component = (elem.split(':'))[0]
                    for line in f:
                        if component in line:
                            parameter = (elem.split(':'))[1]
                            if parameter in line:
                                valueindex = int((elem.split(':'))[2])
                                linelist = (re.sub(' +',',',line)).split(',')
                                value = float(linelist[valueindex])
                                elemindex = fit_params.index(elem)
                                value = obsid+':'+str(value)
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
                        reducedfitstats.append(reducedfitstat)

def returnHardnessRatios(IDs,path_temp,n_channel_ints,d_channel_ints,out_list):
    #Import(s)
    import numpy as np
    from astropy.io import fits
    import os
    import shutil

    #Action 
    for item in IDs:
        obsid = item
        path = path_temp.replace('++++++++++',obsid)
        if os.path.exists(path)==True:
            orig = path
            if path[:-6] == '.jsgrp':
                temp_file = path.replace('.jsgrp','(temp).fits') 
            elif path[:-5] == '.fits':
                temp_file = path.replace('.jsgrp','(temp).fits') 
            else:
                temp_file = path+'(temp).fits'
            shutil.copyfile(orig, temp_file)
            hdul = fits.open(temp_file)
            channels_list = hdul[1].data['CHANNEL']
            counts_list = hdul[1].data['COUNTS']
            
            #Get sum of counts for numerator
            numerator_counts = []
            for elem in n_channel_ints:
                sub_interval = np.array([])
                l_index = int((elem.split(':'))[0])
                u_index = int((elem.split(':'))[1])
                sub_interval = list(counts_list[l_index:u_index])
                numerator_counts.extend(sub_interval)

            #Get sum of counts for denominator
            denominator_counts = []
            for elem in d_channel_ints:
                sub_interval = np.array([])
                l_index = int((elem.split(':'))[0])
                u_index = int((elem.split(':'))[1])
                sub_interval = list(counts_list[l_index:u_index])
                denominator_counts.extend(sub_interval)

            hardness_ratio = sum(numerator_counts)/sum(denominator_counts)
            out_list.append((obsid+':'+str(hardness_ratio)))
            os.remove(temp_file)