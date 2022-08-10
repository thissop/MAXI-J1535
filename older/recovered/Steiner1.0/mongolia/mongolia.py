import os
import os.path
import re
import shutil
import sys

import astropy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

###LATE SEPTEMBER WORK###

def ivy():
    def investigate_gammas():
        x = []
        z = []
        pgs = []
        gammas = []
        goodfiles = []
        with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt','r') as f:
            for line in f:
                if '#' not in line:
                    line = line.replace('\n','')
                    if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log') == True:
                        x.append(line)

        for elem in x:
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+elem+'.log'
            with open(filename,'r') as f:
                for line in f:
                    z.append(line)    
                for element in z:
                    if 'PG-Statistic' in element:
                        pgelem = re.sub(' +',',',element)
                        pgelemlist = pgelem.split(',')
                        pgindex = z.index(element)
                        dofline = z[pgindex+3]
                        doflist = (re.sub(' +',',',dofline).split(','))
                        pgstat = float(pgelemlist[4])/float(doflist[7])
                        if pgstat > 5:
                            continue
                        elif pgstat < 5 and pgstat > 0.7:
                                pgs.append(pgstat)
                                goodfiles.append(elem)
                z.clear()
        
        for elem in goodfiles:
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+elem+'.log'
            with open(filename,'r') as f:
                for line in f:
                    z.append(line)    
                for element in z:
                    if 'Gamma' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        gamma = float(elemlist[5])
                        gammas.append(gamma)
                z.clear()

        for elem in gammas:
            if elem < 2:
                print(elem,goodfiles[gammas.index(elem)],pgs[gammas.index(elem)])
    def percents():
        x = []
        with open('/home/thaddaeus/FMU/Steiner/PGX/IDs.txt','r') as f:
            for line in f:
                if '#' not in line:
                    line = line.replace('\n','')
                    x.append(line)
        for elem in x:
            if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+elem+'/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.jsgrp'):
                jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+elem + \
                '/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.jsgrp' + '\n'
                bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                    elem+'/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.bg' + '\n'
                rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
                arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
                with open('mongolia.txt','a') as f:
                    f.write('data ' + jsgrp)
                    f.write('none'+'\n')
                    f.write('none' + '\n')
                    f.write(bg)
                    f.write(rmf)
                    f.write(arf)
                    f.write('ignore **-1 10.0-**'+'\n')
                    f.write('log '+'/home/thaddaeus/FMU/Steiner/mongolia/percent_logs/'+elem+'.log'+'\n')
                    f.write('show data'+'\n')
                    f.write('log none'+'\n')
                    f.write('data none'+'\n')
    def plot_percents():
        x = []
        countrates = []
        exptimes = []
        with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt','r') as f:
            for line in f:
                if '#' not in line:
                    line = line.replace('\n','')
                    if os.path.exists('/home/thaddaeus/FMU/Steiner/mongolia/percent_logs/'+line+'.log'):
                        x.append(line)
        for elem in x:
            with open('/home/thaddaeus/FMU/Steiner/mongolia/percent_logs/'+elem+'.log','r') as f:
                for line in f:
                    if 'Net count rate ' in line:
                        linelist = (re.sub(' +',',',line)).split(',')
                        percent = linelist[9]
                        percent = percent.replace('(','')
                        percent = float(percent)
                        if percent > 50:
                            countrates.append(percent)
                    if 'Background' not in line:
                        if 'Exposure Time:' in line:
                            linelist = (re.sub(' +',',',line)).split(',')
                            exp = float(linelist[3])
                            exptimes.append(exp)
        for elem in countrates:
            if elem > 75:
                print(x[countrates.index(elem)]+','+str(elem)+','+str(exptimes[countrates.index(elem)]))
        
        def plot():
            exptimes = np.array(exptimes)
            countrates = np.array(countrates)

            sns.set_style('darkgrid')
            fig, axes = plt.subplots(1,2)
            fig.suptitle('-For GTI0 Files-')
            
            sns.distplot(countrates,bins=25,kde=False,ax=axes[0])
            axes[0].set_title('Distribution of % Nicer Backgrounds')
            sns.distplot(exptimes,bins=25,kde=False,ax=axes[1])
            axes[0].set_ylabel('Number of Observations')
            axes[1].set_title('Distribution of Exposure Times')
            axes[1].set_ylabel('Number of Observations')
            plt.show()
    plot_percents()

def fit_commands_for_above_75_v1():
    key = []
    
    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp') == True:
                    key.append(obsid)
    #Write fit commands
    for obsid in key:
        #Some file definitions
        jsgrp = 'data /home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp'+'\n'
        bg = 'backgrnd /home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.bg'+'\n'
        rmf = 'response /home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf /home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open('mongolia.txt','a') as f:
            def tbfeosimpldiskbbrelxill():
                f.write('xspec'+'\n')
                f.write('xsect vern'+'\n')
                f.write('abun wilm'+'\n')
                f.write(jsgrp)
                f.write('none'+'\n')
                f.write('none' + '\n')
                f.write(bg)
                f.write(rmf)
                f.write(arf)
                f.write('ignore **-1. 1.5-2.0 10.-**'+'\n')
                f.write('ignore bad'+'\n')
                f.write('query yes'+'\n')
                f.write('statistic pgstat'+'\n')
                f.write('setp back on'+'\n')
                f.write('model tbabs(simpl(diskbb))'+'\n')
                f.write('3.6,1.5 1.501 4.75 5.0'+'\n')
                f.write('2,1.2 1.3 3.5 4.5'+'\n')
                f.write('0.3,0.001 0.005 0.999 1'+'\n')
                f.write('\n')
                f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
                f.write('\n')
                f.write('chatter 5'+'\n')
                f.write('freeze 1'+'\n')
                f.write('fit'+'\n')
                f.write('\n')
                f.write('thaw 1'+'\n')
                f.write('notice 0.6-10.0'+'\n')
                f.write('fit'+'\n')
                f.write('\n')
                f.write('lmod relxill .'+'\n')
                f.write('editmod tbabs(simpl(diskbb+relxill))'+'\n')
                f.write('\n')
                f.write('=p7')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('60,40,,,')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('=p2'+'\n')
                f.write('\n')
                f.write('\n')
                f.write('100'+'\n')
                f.write('-1'+'\n')
                f.write('\n')
                f.write('freeze 19'+'\n')
                f.write('parallel leven 2'+'\n')
                f.write('fit'+'\n')
                f.write('\n')
                f.write('thaw 7'+'\n')
                f.write('editmod tbfeo(simpl(diskbb+relxill))'+'\n')
                f.write('3.6,1.5 1.501 4.5 4.8'+'\n')
                f.write('0.75,0.001 0.05 2 3'+'\n')
                f.write('0.9,0.1 0.3 3 4'+'\n')
                f.write('\n')
                f.write('parallel leven 2'+'\n')
                f.write('fit'+'\n')
                f.write('chatter 10'+'\n')
                f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v1/logs/'+obsid+'.log'+'\n')
                f.write('show data'+'\n')
                f.write('show fit'+'\n')
                f.write('show param'+'\n')
                f.write('log none'+'\n')
                f.write('cpd /xs'+'\n')
                f.write('setplot energy'+'\n')
                f.write('plot ldata euf mod chi'+'\n')
                f.write('iplot'+'\n')
                f.write('hard /home/thaddaeus/FMU/Steiner/mongolia/v1/plots/'+obsid+'.png/png'+'\n')
                f.write('quit'+'\n')
                f.write('quit'+'\n')
                f.write('y'+'\n')
            def tbfeodiskbbrelxill():
                f.write('xspec'+'\n')
                f.write('xsect vern'+'\n')
                f.write('abun wilm'+'\n')
                f.write(jsgrp)
                f.write('none'+'\n')
                f.write('none' + '\n')
                f.write(bg)
                f.write(rmf)
                f.write(arf)
                f.write('lmod relxill .'+'\n')
                f.write('ignore **-1. 1.5-2.0 10.-**'+'\n')
                f.write('ignore bad'+'\n')
                f.write('query yes'+'\n')
                f.write('statistic pgstat'+'\n')
                f.write('setp back on'+'\n')
                f.write('model tbabs(relxill+diskbb)'+'\n')
                f.write('3.6,1.5 1.501 4.75 5.0'+'\n')
                f.write('\n')
                f.write('=p7')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('60,40,,,')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('2,1.2 1.3 3.5 4.5'+'\n')
                f.write('\n')
                f.write('\n')
                f.write('100'+'\n')
                f.write('-1'+'\n')
                f.write('\n')
                f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
                f.write('\n')
                f.write('chatter 5'+'\n')
                f.write('freeze 19'+'\n')
                f.write('freeze 1'+'\n')
                f.write('fit'+'\n')
                f.write('\n')
                f.write('thaw 1'+'\n')
                f.write('thaw 7'+'\n')
                f.write('notice 0.6-10.0'+'\n')
                f.write('fit'+'\n')
                f.write('\n')
                f.write('editmod tbfeo(diskbb+relxill)'+'\n')
                f.write('3.6,1.5 1.501 4.5 4.8'+'\n')
                f.write('0.75,0.001 0.05 2 3'+'\n')
                f.write('0.9,0.1 0.3 3 4'+'\n')
                f.write('\n')
                f.write('parallel leven 2'+'\n')
                f.write('fit'+'\n')
                f.write('chatter 10'+'\n')
                f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v2/logs/'+obsid+'.log'+'\n')
                f.write('show data'+'\n')
                f.write('show fit'+'\n')
                f.write('show param'+'\n')
                f.write('log none'+'\n')
                f.write('cpd /xs'+'\n')
                f.write('setplot energy'+'\n')
                f.write('plot ldata euf mod chi'+'\n')
                f.write('iplot'+'\n')
                f.write('hard /home/thaddaeus/FMU/Steiner/mongolia/v2/plots/'+obsid+'.png/png'+'\n')
                f.write('quit'+'\n')
                f.write('quit'+'\n')
                f.write('y'+'\n')
            
            def tbabsdiskbbnthcomp():
                f.write('xspec'+'\n')
                f.write('xsect vern'+'\n')
                f.write('abun wilm'+'\n')
                f.write(jsgrp)
                f.write('none'+'\n')
                f.write('none' + '\n')
                f.write(bg)
                f.write(rmf)
                f.write(arf)
                f.write('ignore **-0.5 10.0-**'+'\n')
                f.write('ignore bad'+'\n')
                f.write('query yes'+'\n')
                f.write('statistic pgstat'+'\n')
                f.write('setp back on'+'\n')
                f.write('model tbabs(diskbb+nthcomp)'+'\n')
                f.write('\n')
                f.write(',,,,2.5 2.5'+'\n')
                f.write('\n')
                f.write('\n')
                f.write('100'+'\n')
                f.write('=p2'+'\n')
                f.write('1'+'\n')
                f.write('\n')
                f.write('\n')
                f.write('freeze 5'+'\n')
                f.write('chatter 5'+'\n')
                f.write('fit'+'\n')
                f.write('chatter 10'+'\n')
                f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v3_nthcomp/logs/'+obsid+'.log'+'\n')
                f.write('show data'+'\n')
                f.write('show fit'+'\n')
                f.write('show param'+'\n')
                f.write('log none'+'\n')
                f.write('cpd /xs'+'\n')
                f.write('setplot energy'+'\n')
                f.write('plot ldata euf mod chi'+'\n')
                f.write('iplot'+'\n')
                f.write('hard /home/thaddaeus/FMU/Steiner/mongolia/v3_nthcomp/plots/'+obsid+'.png/png'+'\n')
                f.write('quit'+'\n')
                f.write('quit'+'\n')
                f.write('y'+'\n')


                

            #investigate()

def investigate_nthcomp():
    key = []
    pgs = []
    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp') == True:
                    key.append(obsid)
    for obsid in key:
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/mongolia/v3_nthcomp/logs/'+obsid+'.log') == True:
            with open('/home/thaddaeus/FMU/Steiner/mongolia/v3_nthcomp/logs/'+obsid+'.log','r') as f:
                for elem in f:
                    z = []
                    if 'PG-Statistic' in elem:
                        pgelem = re.sub(' +', ',', elem)
                        pgelemlist = pgelem.split(',')
                        pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                        pgs.append(pgstat)
    
    for elem in pgs:
        if elem < 2:
            print(elem,key[pgs.index(elem)])

def investigate_resp():
    from astropy.io import fits

    with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+
                    '/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp') == True:
                    orig = ('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid + 
                        '/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp')
                    target = ('/home/thaddaeus/FMU/Steiner/thaddaeus/' +obsid+
                        '/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.fits')
                    shutil.copyfile(orig, target)
                    hdul = fits.open(target)
                    resp = hdul[1].header['RESPFILE']
                    arf = hdul[1].header['ANCRFILE']
                    with open('/home/thaddaeus/FMU/Steiner/mongolia/sys_err/rsps_and_arfs.txt'
                        ,'a') as f2: 
                        f2.write(obsid+','+resp+','+arf+'\n')
                    os.remove(target)



    ###investigate resp files
    '''
    key = []
    pgs = []
    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp') == True:
                    key.append(obsid)
    for obsid in key:
        file = '/home/thaddaeus/FMU/Steiner/mongolia/sys_err/'+str(obsid)+'.log'
        with open(file,'r') as f:
            for line in f: 
                if '#Error: cannot read response file' in line:
                    line=line.replace('\n','')
                    if '53019466' in line: 
                        print(obsid)
                        print(line)
        '''
        
    '''
    ###I was using this to get output list of all rsp files
    data = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp'
    print('xspec')
    print('log /home/thaddaeus/FMU/Steiner/mongolia/sys_err/'+str(obsid)+'.log')
    print('data '+data)
    print('none')
    print('none')
    print('log none')
    print('quit')
    print('y')
    '''

###OCTOBER WORK###
###Function Descriptions###
'''
gen2tbf()=
    MODEL:  nthcomp(): tbabs(diskbb+nthcomp), tbabs is free, nthcomp par3 tied to 
                       diskbb par1, nthcomp par2 frozen to 100 KeV. 
            relxill(): tbfeo(simpl(diskbb)+relxill), tbfeo parameters frozen to best
                       fit parameters from relxill folder (that was emailed to Dr. 
                       Steiner) error fits, before running error on the files logxi and
                       relxill norm are frozen (to prevent core dumping during error).
                       Confidence intervals found for gamma, comptonized fraction, and
                       diskbb Tin. NOTE: at the moment, relxill parameters have one sigma
                       confidence intervals. 
    DESCR:  Second generation xspec command generator, reads .jsgrp files for what
            rsp and arf files they required/requested by each .jsgrp file (technically
            it creates a temporary .fits clone and deletes that clone after reading 
            it); this script also will be the first generation to use the error script
            Dr. Steiner sent me (after the first round of fits that is). 

freezetbfeo()=
    MODEL:  N/A.  
    DESCR:  The purpose of this function is to find the median tbfeo values from my 
            my best tbfeofits (that had confidence intervals) to use as frozen values. 

ivesgen2()=
    MODEL:  N/A
    DESCR:  The purpose of this function is to read through log files and plot findings
            from the gen2tbf() function relxill fitting routine. 

compare_rsps()= 
    MODEL:  N/A
    DESCR:  The purpose of this function is to list the obsid's with the incorrect rsp 
    files and their red pg stat values. 
'''

##Fit Command Functions##
def gen2tbf():
    #Imports
    from astropy.io import fits

    #global list definitions
    key = []
    lackingrsps = []
    lackingarfs = []

    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/v4_global/ALL_IDS.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                #temp
                with open('/home/thaddaeus/FMU/Steiner/mongolia/testcorrectrsp.txt','r') as g:
                    for line in g:
                        if obsid in line:
                            key.append(obsid)

                ###THIS IS THE LINE TO ADJUST-\/\/\/\/-THIS IS WHERE IDs ARE CHECKED###
                '''
                if os.path.exists('/home/thaddaeus/FMU/Steiner/vietnam/for_email/relxill/informative_but_no_error/fit_logs/'+obsid+'.log') == True:
                    key.append(obsid)
                '''
                '''
                with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f2:
                    for line in f2:
                        if obsid in line:
                            if 'nicer_d49_55575341.rmf' in line:
                                continue
                            else:
                                key.append(obsid)    
                '''
    #Write fit commands
    ##remove this set thing later
    key = set(key)
    key = list(key)
    
    for obsid in key:
        #Some file definitions
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp'
        bg = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.bg'
        
        #Get rsp and arfs
        target = ('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.fits')
        shutil.copyfile(jsgrp, target)
        hdul = fits.open(target)
        rsp = hdul[1].header['RESPFILE']
        arf = hdul[1].header['ANCRFILE']
        if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(rsp)) == True:
            rsp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(rsp)
        else:
            lackingrsps.append(obsid)
        if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(arf)):
            arf = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(arf)
        else: 
            lackingarfs.append(obsid)
        os.remove(target)

        #Write those fit commands
        def nthcomp():
            with open('mongolia.txt','a') as f:
                f.write('xspec'+'\n')
                f.write('xsect vern'+'\n')
                f.write('abun wilm'+'\n')
                f.write('data '+jsgrp+'\n')
                f.write('none'+'\n')
                f.write('none' + '\n')
                f.write('backgrnd '+bg+'\n')
                f.write('response '+rsp+'\n')
                f.write('arf '+arf+'\n')
                f.write('ignore **-0.5 10.0-**'+'\n')
                f.write('ignore bad'+'\n')
                f.write('query yes'+'\n')
                f.write('statistic pgstat'+'\n')
                f.write('setp back on'+'\n')
                
                f.write('model tbabs(diskbb+nthcomp)'+'\n')
                f.write('3.66,3 3 4.5 4.5'+'\n')
                f.write(',,,,2.5 2.5'+'\n')
                f.write('\n')
                f.write('2,1.1 1.1 4.5 4.5'+'\n')
                f.write('100'+'\n')
                f.write('=p2'+'\n')
                f.write('1'+'\n')
                f.write('\n')
                f.write('\n')
                
                f.write('freeze 5'+'\n')
                
                f.write('chatter 5'+'\n')
                f.write('fit'+'\n')

                f.write('chatter 10'+'\n')
                f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v4_global/logs/'+obsid+'.log'+'\n')
                f.write('show data'+'\n')
                f.write('show fit'+'\n')
                f.write('show param'+'\n')
                f.write('log none'+'\n')
                f.write('cpd /xs'+'\n')
                f.write('setplot energy'+'\n')
                f.write('plot ldata euf mod chi'+'\n')
                f.write('iplot'+'\n')
                f.write('hard /home/thaddaeus/FMU/Steiner/mongolia/v4_global/plots/'+obsid+'.png/png'+'\n')
                f.write('quit'+'\n')
                f.write('quit'+'\n')
                f.write('y'+'\n')

        def relxill():
            f.write('xspec'+'\n')
            f.write('xsect vern'+'\n')
            f.write('abun wilm'+'\n')
            f.write('data ' + jsgrp+'\n')
            f.write('none'+'\n')
            f.write('none' + '\n')
            f.write('backgrnd '+bg+'\n')
            f.write('response '+rsp+'\n')
            f.write('arf '+arf+'\n')
            f.write('ignore **-2.2 10.0-**'+'\n')
            f.write('ignore bad'+'\n')
            f.write('query yes'+'\n')
            f.write('statistic pgstat'+'\n')
            f.write('setp back on'+'\n')
            f.write('model tbabs(simpl(diskbb))'+'\n')
            f.write('/*'+'\n')
            f.write('newpar 1'+'\n')
            f.write('3.6,1.5 1.501 4.5 5.0'+'\n')
            f.write('newpar 2'+'\n')
            f.write('2,1.3 1.3 4 4'+'\n')
            f.write('newpar 3'+'\n')
            f.write('0.3,0.001 0.005 0.99 0.999'+'\n')
            f.write('newpar 5'+'\n')
            f.write('0.7,0.1 0.15 2.8 3'+'\n')
            f.write('chatter 5'+'\n')
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('notice 0.5-1.5'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('lmod relxill .'+'\n')
            f.write('editmod tbabs(simpl(diskbb+relxill))'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('66,3 5,,')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('=2'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('100'+'\n')
            f.write('-1'+'\n')
            f.write('\n')
            f.write('freeze 19'+'\n')
            f.write('editmod tbfeo(simpl(diskbb+relxill))'+'\n')
            f.write('3.68341'+'\n')
            f.write('0.7185715'+'\n')
            f.write('0.977861'+'\n')
            f.write('\n')
            f.write('freeze 1-3'+'\n')
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n') 
            f.write('chatter 10'+'\n')
            ### NOTE: log path below should be changed
            f.write('log /home/thaddaeus/FMU/Steiner/mongolia/correct_rsps_comparison/logs/'+obsid+'.log'+'\n')
            f.write('show data'+'\n')
            f.write('show param'+'\n')
            f.write('show fit'+'\n')
            f.write('log none'+'\n')
        #log functions
        def error_relxill():
            f.write('freeze 19 23'+'\n')   
            f.write('fit'+'\n')
            f.write('chatter 5 5'+'\n')
            ### NOTE: log path below should be changed
            f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v5/logs/error'+obsid+'.log'+'\n')
            f.write('error 1. 5 6 8'+'\n')
            f.write('log none'+'\n')
        def cflux_relxill():
            f.write('freeze 6 13 14 20'+'\n')
            f.write('fit'+'\n')
            f.write('editmod cflux*tbfeo(simpl(diskbb)+relxill)'+'\n')
            f.write('0.5'+'\n')
            f.write('10'+'\n')
            f.write('\n')
            f.write('fit'+'\n')
            ### NOTE: log path below should be changed
            f.write('log /home/thaddaeus/FMU/Steiner/mongolia/v5/logs/cflux'+obsid+'.log'+'\n')
            f.write('show param'+'\n')
            f.write('chatter 5'+'\n')
            f.write('error 2.706 3'+'\n')
            f.write('log none'+'\n')
        with open('mongolia.txt','a') as f:    
            relxill()
            #error_relxill()
            #cflux_relxill()
            f.write('quit'+'\n')
            f.write('y'+'\n')

    print(len(lackingarfs))
    print(len(lackingrsps))            

##Investigation Functions##
def freezetbfeo():

    import statistics as stats
    key = []
    pgs = []
    nHs = []
    Os = []
    Fes = []

    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/v4_global/ALL_IDS.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/vietnam/for_email/relxill/error_fits/fit_logs/'+obsid+'.log') == True:
                    key.append(obsid)
    #Write fit commands
    for obsid in key:
        with open('/home/thaddaeus/FMU/Steiner/vietnam/for_email/relxill/error_fits/fit_logs/'+obsid+'.log','r') as f:
            z = []
            for line in f:
                z.append(line)
            
            for elem in z:    
                if 'Fit statistic  : PG-Statistic' in elem:
                    linelist = (re.sub(' +',',',elem)).split(',')
                    pg = float(linelist[4])    
                    dofline = z[z.index(elem)+3]
                    doflist = (re.sub(' +',',',dofline)).split(',')
                    dof = float(doflist[7])
                    pgstat = pg/dof
                    pgs.append(pgstat)
                    print(obsid,pg,dof, pgstat)
                elif 'TBfeo' and 'nH' in elem:
                    linelist = (re.sub(' +',',',elem)).split(',')
                    nH = float(linelist[6])
                    nHs.append(nH)
                elif 'TBfeo' and 'O' and '#   2' in elem:
                    linelist = (re.sub(' +',',',elem)).split(',')
                    O = float(linelist[5])
                    Os.append(O)
                elif 'TBfeo' and '#   3' and 'Fe' in elem:
                    linelist = (re.sub(' +',',',elem)).split(',')
                    Fe = float(linelist[5])
                    Fes.append(Fe)
    
    for elem in pgs:
        if elem < 0.98 or elem > 1.03: 
            rindex = pgs.index(elem)
            pgs.remove(elem)
            nHs.remove(nHs[rindex])
            Os.remove(Os[rindex])
            Fes.remove(Fes[rindex])
    for elem in nHs:
        if elem < 3:
            nHs.remove(elem)
    for elem in nHs:
        if elem > 4.27:
            nHs.remove(elem)

    for elem in Os:
        if elem > 1:
            Os.remove(elem)
    for elem in Os:
        if elem < 0.4:
            Os.remove(elem)

    for elem in Fes:
        if elem > 1:
            Fes.remove(elem)
    print('***************')
    print("Median nH Value: "+str(stats.median(nHs))+'; Mean: '+str(stats.mean(nHs)))
    print("Median O Value: "+str(stats.median(Os))+'; Mean: '+str(stats.mean(Os)))
    print("Median Fe Value: "+str(stats.median(Fes))+'; Mean: '+str(stats.mean(Fes)))
    print(len(nHs),len(Os),len(Fes))
    import matplotlib.pyplot as plt
    import numpy as np
    
    print(nHs,Os,Fes)
    nHs = np.array(nHs)
    Os = np.array(Os)
    Fes = np.array(Fes)

    plt.hist(nHs,color='red')
    plt.hist(Os,color='blue')
    plt.hist(Fes,color='green')
    plt.show()
    
def ivesgen2():
    key = []
    gammas = []
    comptfracs = []
    sourcefracs = []


    #Get list of IDs
    with open('/home/thaddaeus/FMU/Steiner/mongolia/v4_global/ALL_IDS.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/mongolia/v5/logs/v5a/'+obsid+'.log') == True:
                    key.append(obsid)
    #Write fit commands
    for obsid in key:
        with open('/home/thaddaeus/FMU/Steiner/mongolia/v5/logs/v5a/'+obsid+'.log','r') as f:
            data = f.read().replace('\n','')
            if 'gsl: svd.c:148: ERROR:' in line: 
                continue
            else:
                for line in f:
                    if 'TBfeo' and 'nH' in line:
                        linelist = (re.sub(' +',',',line)).split(',')
                        nH = float(linelist[6])
                        nHs.append(nH)
                    elif 'TBfeo' and 'O' and '#   2' in line:
                        linelist = (re.sub(' +',',',line)).split(',')
                        O = float(linelist[5])
                        Os.append(O)
                    elif 'TBfeo' and '#   3' and 'Fe' in line:
                        linelist = (re.sub(' +',',',line)).split(',')
                        Fe = float(linelist[5])
                        Fes.append(Fe)

def compare_rsps():
    key = []
    pgs = []
    with open('/home/thaddaeus/FMU/Steiner/mongolia/v4_global/ALL_IDS.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                
                ###THIS IS THE LINE TO ADJUST-\/\/\/\/-THIS IS WHERE IDs ARE CHECKED###
                
                with open('/home/thaddaeus/FMU/Steiner/mongolia/sys_err/rsps_and_arfs.txt','r') as g:
                    for line in g:
                        if 'nicer_d49_55575341.rmf' not in line:
                            if os.path.exists('/home/thaddaeus/FMU/Steiner/mongolia/v2/logs/'+obsid+'.log') == True:
                                key.append(obsid)
    key = set(key)
    key = list(key)
    for obsid in key:
        with open('/home/thaddaeus/FMU/Steiner/mongolia/v2/logs/'+obsid+'.log','r') as f:
            z = []
            for line in f:
                z.append(line)
            
            for elem in z:    
                if 'Fit statistic  : PG-Statistic' in elem:
                    linelist = (re.sub(' +',',',elem)).split(',')
                    pg = float(linelist[4])    
                    dofline = z[z.index(elem)+3]
                    doflist = (re.sub(' +',',',dofline)).split(',')
                    dof = float(doflist[7])
                    pgstat = pg/dof
                    pgs.append(str(pgstat)+','+str(obsid))
    for elem in pgs:
        print(elem)

freezetbfeo()
