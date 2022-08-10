def tbfeo_v3(IDs,pathtemp,outfile):
    #Imports
    import os
    from astropy.io import fits
    import shutil

    #Definitions 
    lackingarfs = []
    lackingrsps = []
    #Action
    
    #Function definitions
    def relxill(fitpathtemp):
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
        f.write('chatter 10 10'+'\n')
        fit_path_temp = fitpathtemp.replace('++++++++++',obsid)
        f.write('log '+fit_path_temp+'\n')
        f.write('show data'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('log none'+'\n')
    def error(errorpathtemp):
        f.write('freeze 19 23'+'\n')   
        f.write('fit'+'\n')
        f.write('chatter 5 5'+'\n')
        error_file_path = errorpathtemp.replace('++++++++++',obsid)
        f.write('log '+error_file_path+'\n')
        f.write('parallel error 2'+'\n')
        f.write('error 5 6 8'+'\n')
        f.write('log none'+'\n')
    def cflux(cfluxpathtemp):
        f.write('freeze 6 13 14 20'+'\n')
        f.write('fit'+'\n')
        f.write('editmod tbfeo*cflux(simpl(diskbb)+relxill)'+'\n')
        f.write('0.5'+'\n')
        f.write('10'+'\n')
        f.write('\n')
        f.write('fit'+'\n')
        cflux_path_temp = cfluxpathtemp.replace('++++++++++',obsid)
        f.write('log '+cflux_path_temp+'\n')
        f.write('chatter 10 10'+'\n')
        f.write('show param'+'\n')
        f.write('chatter 5 5'+'\n')
        f.write('error 2.706 7'+'\n')
        f.write('log none'+'\n')
    
    #Execute the functions for all IDs
    for item in IDs:
        obsid = item
        path = pathtemp.replace('++++++++++',obsid)
        if os.path.exists(path) == True:
            
            #Some file definitions
            jsgrp = path 
            bg = path.replace('.jsgrp','.bg')
            target = path
            
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
            
            if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(arf)) == True:
                arf = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+str(arf)
            else: 
                lackingarfs.append(obsid)

            os.remove(target)
            
            
            #Finally. Generate the fit commands
            with open(outfile,'a') as f:    
                relxill(fitpathtemp='/home/thaddaeus/FMU/Steiner2.0/20November/Ragnarok/logs/++++++++++.log')
                error(errorpathtemp='/home/thaddaeus/FMU/Steiner2.0/20November/Ragnarok/logs/error++++++++++.log')
                cflux(cfluxpathtemp='/home/thaddaeus/FMU/Steiner2.0/20November/Ragnarok/logs/cflux++++++++++.log')
                f.write('quit'+'\n')
                f.write('y'+'\n')
    
    print(len(lackingarfs))
    print(len(lackingrsps))  