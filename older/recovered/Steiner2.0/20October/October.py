import os
import os.path
import re
import shutil
import sys
import astropy

###Function Descriptions###
'''
tbf3()=
    MODEL:  relxill(): tbfeo(simpl(diskbb)+relxill), (tbfeo parameters frozen to best
                       fit values). 
    DESCR:  Second generation xspec command generator, reads .jsgrp files for what
            rsp and arf files they required/requested by each .jsgrp file (technically
            it creates a temporary .fits clone and deletes that clone after reading 
            it); this script can also use Dr. Sander's error 
            script. Initially I was having problems with core dumping. Initial fits 
            have gamma soft limit @ 1.4 gamma hard lower @ 1.3, gamma soft upper @ 3.3
            gamma soft upper at 3.3. Things might be better now-I installed patch up to
            12.11.0m. Most current model is using predetermined frozen bfeo


'''

def tbf3():
    #Imports
    from astropy.io import fits

    #global list definitions
    key = []
    lackingrsps = []
    lackingarfs = []

    #Get list of IDs --- current ignored section should be usual
    '''
    with open('/home/thaddaeus/FMU/Steiner/mongolia/v4_global/ALL_IDS.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsid = (line.split(','))[0]
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/for_email/relxill/informative_but_no_error/fit_logs/'+obsid+'.log') == True:
                    key.append(obsid)
    '''
    with open('/home/thaddaeus/FMU/Steiner/mongolia/>75percentsource.txt','r') as f:
        for line in f:
            if '#' not in line:
                obsid = (line.split(','))[0]
                if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI0.jsgrp') == True:
                    key.append(obsid)
    
    key = set(key)
    key = list(key)
    
    #Get files for fitting
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
            
        with open('/home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/fitcommands.txt','a') as f:
            f.write('heainit'+'\n')
            f.write('xspec'+'\n')
            f.write('xsect vern'+'\n')
            f.write('abun wilm'+'\n')
            f.write('data ' + jsgrp+'\n')
            f.write('none'+'\n')
            f.write('none' + '\n')
            f.write('backgrnd '+bg+'\n')
            f.write('response '+rsp+'\n')
            f.write('arf '+arf+'\n')
            f.write('ignore **-0.5 1.5-2.2 10.0-**'+'\n')
            f.write('ignore bad'+'\n')
            f.write('query yes'+'\n')
            f.write('statistic pgstat'+'\n')
            f.write('setp back on'+'\n')
            f.write('model tbabs(simpl(diskbb))'+'\n')
            f.write('/*'+'\n')
            f.write('newpar 1'+'\n')
            f.write('3.0 0.01 1.5 1.501 4.5 5.0'+'\n')
            f.write('newpar 2'+'\n')
            f.write('2 0.02 1.3 1.3 3.4 3.4'+'\n')
            f.write('newpar 3'+'\n')
            f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
            f.write('newpar 5'+'\n')
            f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
            f.write('chatter 5'+'\n')
            f.write('freeze 1'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('thaw 1'+'\n')
            #f.write('notice 1.0-10.0'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('lmod relxill .'+'\n')
            f.write('editmod tbabs(simpl(diskbb+relxill))'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('86,3 5,,'+'\n')
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
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('editmod tbfeo(simpl(diskbb+relxill))'+'\n')
            f.write('3.762315'+'\n')
            f.write('0.67563'+'\n')
            f.write('0.909694'+'\n')
            f.write('\n')
            f.write('freeze 1 2 3'+'\n')
            f.write('freeze 19'+'\n')
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n')
            f.write('chatter 10'+'\n')
            f.write('log /home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/logs/'+obsid+'.log'+'\n')
            f.write('show data'+'\n')
            f.write('show fit'+'\n')
            f.write('show param'+'\n')
            f.write('log none'+'\n')

            #plot
            f.write('cpd /xs'+'\n')
            f.write('setplot energy'+'\n')
            f.write('plot ldata euf mod chi'+'\n')
            f.write('iplot'+'\n')
            f.write('hard /home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/plots/'+obsid+'.png/png'+'\n')
            f.write('quit'+'\n')
            
            #errorQuit()
            f.write('log /home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/logs/error'+obsid+'.log'+'\n')
            #f.write('source /home/thaddaeus/Random/common.tcl'+'\n')
            f.write("chatter 5 5"+'\n')
            f.write('parallel error 2'+'\n')
            f.write('error 1. 5 6 8'+'\n')
            #f.write('_pct_get_error_list {5 6 8} 1.'+'\n')
            f.write('log none'+'\n')
            f.write('quit'+'\n')
            f.write('y'+'\n')
            
    print(len(lackingarfs))
    print(len(lackingrsps))


        

tbf3()