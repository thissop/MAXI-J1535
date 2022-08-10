###Function Descriptions###
'''
find_all_data_files()=
    MODEL:  n/a
    DESCR:  I wrote this function to find all the silver data files, not just the GTI0s.  

'''



def find_all_data_files():
    #Import(s)
    import os
    import numpy as np

    #Action

    '''Get obsids'''
    
    obsids = []
    num_list = list(range(80))
    paths=[]
    print(num_list)
    with open('/home/thaddaeus/FMU/Steiner2.0/permanent/ALL_NICER_IDs.txt','r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n','')
                obsids.append(line)

    '''check if files exist'''  
    for obsid in obsids:
        for item in num_list:
            path='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/'+obsid+'/jspipe/js_ni'+obsid+'_0mpu7_silver_GTI'+str(item)+'.jsgrp'
            if os.path.exists(path)==True:
                print(obsid+':'+str(item))
                paths.append(path)

    print(len(paths))

def nthcomp_v1(file_fracs,data_path_temp,arf_path_temp,rsp_path_temp,log_dir,outfile):
    '''example file_frac: '2130360212:0' '''
    '''example path temp: '/home/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp' '''
    '''example rsp path: '/home/thaddaeus/FMU/Steiner/thaddaeus/' '''
    '''example log_dir path: '/home/thaddaeus/FMU/Steiner2.0/20November/Ragnarok/logs/' '''
    #Import(s)
    import os
    from astropy.io import fits
    import shutil
    
    #Global Declarations
    lacking_arfs = []
    lacking_rsps = []
    #Action

    #Function definitions
    def nthcomp(log_temp):
        log_temp = log_temp.replace('++++++++++',obsid)
        log_temp = log_temp.replace('+',file_frac_list[1])
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp+'\n')
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write('backgrnd '+bg+'\n')
        f.write('response '+rsp+'\n')
        f.write('arf '+arf+'\n')
        f.write('ignore **-0.5 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        #f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbabs(diskbb+nthcomp)'+'\n')
        #Define parameters
        f.write('3.6,1.5 1.501 4.5 4.501'+'\n')
        f.write('0.6,0.01 0.01 2.5 2.5'+'\n')
        f.write('\n')
        f.write('2 , 1.2 1.2 4 4'+'\n')
        f.write('1000'+'\n')
        f.write('=p2'+'\n')
        f.write('1'+'\n')
        f.write('0'+'\n')
        f.write('\n')
        #Continue
        f.write('freeze 5'+'\n')
        f.write('freeze 7'+'\n')
        f.write('freeze 8'+'\n')
        f.write('chatter 5'+'\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit 400'+'\n') #no query yes
        f.write('n'+'\n') #no query yes
        f.write('log '+log_temp+'\n')
        f.write('show data'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('log none'+'\n')
    def error(log_temp):
        log_temp = log_temp.replace('++++++++++',obsid)
        log_temp = log_temp.replace('+',file_frac_list[1])

    def cflux(log_temp):
        log_temp = log_temp.replace('++++++++++',obsid)
        log_temp = log_temp.replace('+',file_frac_list[1])

    #Execute on all file_fracs
    for file_frac in file_fracs:
        file_frac_list = file_frac.split(':')
        obsid = file_frac_list[0]
        
        #Get .jsgrp and .bg files
        data_path=data_path_temp.replace('++++++++++',obsid)
        data_path.replace('+',file_frac_list[1])
        jsgrp = data_path 
        bg = data_path.replace('.jsgrp','.bg')
        
        #Get .rsp and .arf files
        target = jsgrp.replace('.jsgrp','.fits')
        shutil.copyfile(jsgrp, target)
        hdul = fits.open(target)
        rsp = hdul[1].header['RESPFILE']
        arf = hdul[1].header['ANCRFILE']
        
        if os.path.exists(rsp_path_temp+str(rsp)) == True:
            rsp = rsp_path_temp+str(rsp)
        else:
            lacking_rsps.append(file_frac)
        
        if os.path.exists(arf_path_temp+str(arf)) == True:
            arf = arf_path_temp+str(arf)
        else: 
            lacking_arfs.append(file_frac)

        os.remove(target)

        #Finally. Generate the fit commands
        with open(outfile,'a') as f:    
            nthcomp(log_temp=(log_dir+'++++++++++_GTI+.log'))
            #error(log_temp=(log_dir+'error++++++++++_GTI+.log'))
            #cflux(log_temp=(log_dir+'cflux++++++++++_GTI+.log'))
            f.write('quit'+'\n')
            f.write('y'+'\n')
    
    print(len(lacking_arfs))
    print(len(lacking_rsps))  


find_all_data_files()