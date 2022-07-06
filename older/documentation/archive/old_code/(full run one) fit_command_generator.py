def nthcomp_v2(IDs,data_path_temp,arf_dir,rmf_dir,log_dir,plot_dir,cores,iterations,dfs,out_file,save_plots):
    '''Example seg_id in IDs: 
        '2130360212_0' '''
    '''Example data_path_temp: 
        '/home/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp' '''
    '''Example arf_dir (directory of the ancillary resp. file):  
        '/home/.../thaddaeus/' '''
    '''Example rmf_dir (directory of the redistribution matrix, aka response, file): 
        '/home/.../thaddaeus/' '''
    '''log_dir (directory for log files to be written to): 
        '/home/thaddaeus/logs/' '''
    '''plot_dir (directory for plot files to be saved to):
        '/home/thaddaeus/plots/' '''
    '''Cores: 
        Integer; number of cores in computer CPU'''
    '''iterations: 
        Integer; number of fit iterations'''
    '''dfs: 
        String; delta fit statisitic (for error)'''
    '''out_file: 
        File to write commands to'''
    '''save_plots:
        Boolean; whether plots should be saved or not'''

    #Import(s)
    import os
    from astropy.io import fits
    import shutil

    #Action
    lacking_arfs = []
    lacking_rmfs = []

    #Function definitions

    def fit_commands(fit_log_temp,error_log_temp):
        fit_log_file = fit_log_temp.replace('++++++++++',seg_id)
        error_log_file = error_log_temp.replace('++++++++++',seg_id)

        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp+'\n')
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write('backgrnd '+bg+'\n')
        f.write('response '+rmf+'\n')
        f.write('arf '+arf+'\n')
        
        f.write('ignore **-0.5 1.5-2.3 10.0-**'+'\n') #Often modified
        
        f.write('ignore bad'+'\n')

        #f.write('query yes'+'\n') ''' Often modified '''

        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbabs(diskbb+nthcomp)'+'\n')
        
        f.write(nH+'\n')

        f.write('0.6 0.02 '+tin_lower+' '+tin_lower+' '+tin_upper+' '+tin_upper+'\n')
        f.write('\n')
        
        f.write('2 0.02 '+gamma_lower+' '+gamma_lower+' '+gamma_upper+' '+gamma_upper+'\n')  

        f.write(kTe+'\n')
        f.write('=p2'+'\n')
    
        f.write(inp_type+'\n')
        
        f.write(redshift+'\n')
        
        f.write('\n')
        f.write('freeze 1'+'\n')
        f.write('freeze 5'+'\n')
        f.write('freeze 7'+'\n')
        f.write('freeze 8'+'\n')
        f.write('chatter 5 10'+'\n')
        f.write('parallel leven '+str(cores)+'\n')
        f.write('fit '+str(iterations)+'\n') #query yes = False
        f.write('n'+'\n') #query yes = False
        
        f.write('chatter 5 5'+'\n')
        f.write('log '+error_log_file+'\n')
        f.write('error '+dfs+' 2 3 4 9'+'\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('log none'+'\n')
        
        f.write('chatter 5 10'+'\n')
        f.write('log '+fit_log_file+'\n')
        f.write('show data'+'\n')
        f.write('show model'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('log none'+'\n')
        
        #Save plot
        if save_plots==True:
            f.write('cpd /xs'+'\n')
            f.write('setplot energy'+'\n')
            f.write('plot ldata euf mod chi'+'\n')
            f.write('iplot'+'\n')
            plot_path = plot_dir + seg_id + '.png'
            f.write('hard '+plot_path+'/png'+'\n')
            f.write('quit'+'\n')

    def error_commands(log_temp):
        log_file = log_temp.replace('++++++++++',seg_id)
        f.write('chatter 5 5'+'\n')
        f.write('log '+log_file+'\n')
        f.write('error '+dfs+' 2 3 4 9'+'\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('log none'+'\n')
    
    def cflux_commands(log_temp):
        log_file = log_temp.replace('++++++++++',seg_id)
        
        def bounds():
            f.write('0.5'+'\n')
            f.write('10.0'+'\n')
            f.write('\n')

        f.write('chatter 5 10'+'\n')
        #f.write('freeze 2 3 4 9'+'\n')
        
        f.write('editmod tbabs*cflux(diskbb+nthcomp)'+'\n')
        bounds()

        '''
        f.write('editmod tbabs*cflux(cflux(diskbb)+nthcomp)'+'\n')
        bounds()

        f.write('editmod tbabs*cflux(cflux(diskbb)+cflux(nthcomp))'+'\n')
        bounds()
        '''

        f.write('fit'+'\n')
        f.write('n'+'\n')

        f.write('log '+log_file+'\n')
        f.write('show data'+'\n')
        f.write('show model'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
    
    def cflux_error(log_temp):
        log_file = log_temp.replace('++++++++++',seg_id)
        f.write('chatter 5 5'+'\n')
        f.write('log '+log_file+'\n')
        
        f.write('error '+dfs+' 4'+'\n') #Often Changed
        
        f.write('n'+'\n')
        f.write('\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('log none'+'\n')

    #Execution
    nH = '3.2'
    tin_lower = '0.01'
    tin_upper = '1.0'
    gamma_lower = '1.2'
    gamma_upper = '3.0'
    kTe = '100'
    inp_type = '1'
    redshift = '0'

    for seg_id in IDs:
        print(seg_id)
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        data_path = data_path_temp.replace('++++++++++',obsid)
        data_path = data_path.replace('+',gti)
        if os.path.exists(data_path)==True:
            bg = data_path.replace('.jsgrp','.bg')
       
            #Get .rmf and .arf files
            jsgrp = data_path
            target = jsgrp.replace('.jsgrp','.fits')
            shutil.copyfile(jsgrp, target)
            hdul = fits.open(target)
            rmf = hdul[1].header['RESPFILE']
            arf = hdul[1].header['ANCRFILE']
        
            if os.path.exists(rmf_dir+str(rmf)) == True:
                rmf = rmf_dir+str(rmf)
            else:
                lacking_rmfs.append(seg_id)
        
            if os.path.exists(arf_dir+str(arf)) == True:
                arf = arf_dir+str(arf)
            else:
                lacking_arfs.append(seg_id)

            os.remove(target)

            #Finally, write commands to outfile
            with open(out_file,'a') as f:    
                fit_commands(fit_log_temp=(log_dir+'++++++++++.log'),error_log_temp=(log_dir+'error++++++++++.log'))
                #error_commands(log_temp=(log_dir+'error++++++++++.log'))
                cflux_commands(log_temp=(log_dir+'cflux++++++++++.log'))
                cflux_error(log_temp=(log_dir+'cflux_error++++++++++.log'))
                f.write('quit'+'\n')
                f.write('y'+'\n')

    print(len(lacking_arfs))
    print(len(lacking_rmfs))
    print('\n')
    print('Model Summary')
    print('*************')
    print('Model: tbabs(diskbb+nthcomp)')
    print('Delta fit statistic: '+dfs)
    print('Noticed Channels: 0.5-1.5 2.3-10.0 keV')
    print('nH: 3.2 (frozen)')
    print('Tin lower limit: '+tin_lower)
    print('Tin upper limit: '+tin_upper)
    print('Gamma lower limit: '+gamma_lower)
    print('Gamma upper limit: '+gamma_upper)
    print('High energy rollover: '+kTe+' keV')
    print('inp_type: '+inp_type)
    print('Redshift: '+redshift)

def simpl(IDs,data_path_temp,arf_dir,rmf_dir,log_dir,cores,iterations,dfs,out_file):
    #Import(s)
    import os
    from astropy.io import fits
    import shutil

    #Action
    lacking_arfs = []
    lacking_rmfs = []

    #Function definitions
    def simpl_commands(fit_log_temp,error_log_temp):
        fit_log_file = fit_log_temp.replace('++++++++++',seg_id)
        error_log_file = error_log_temp.replace('++++++++++',seg_id)

        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp+'\n')
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write('backgrnd '+bg+'\n')
        f.write('response '+rmf+'\n')
        f.write('arf '+arf+'\n')
        
        f.write('ignore **-0.5 1.5-2.3 10.0-**'+'\n') #Often modified
        
        f.write('ignore bad'+'\n')

        #f.write('query yes'+'\n') ''' Often modified '''

        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')

        f.write('model clear'+'\n')
        f.write('model tbabs(simpl(diskbb))'+'\n')
        f.write(nH+'\n')
        f.write('2 0.02 '+simpl_gamma_lower+' '+simpl_gamma_lower+' '+simpl_gamma_upper+' '+simpl_gamma_upper+'\n')
        f.write('0.5 0.02 0.00001 0.0001 1 1'+'\n')
        f.write(simpl_flag+'\n')
        f.write('0.6 0.02 '+tin_lower+' '+tin_lower+' '+tin_upper+' '+tin_upper+'\n')
        f.write('\n')
        f.write('freeze 1 4'+'\n')
        f.write('chatter 5 5'+'\n')
        f.write('parallel leven '+str(cores)+'\n')
        f.write('fit '+str(iterations)+'\n') #query yes = False
        f.write('n'+'\n') #query yes = False
        
        #Just for the first round to find which obsids have \chi^{2}_{\nu} < 2
        
        f.write('chatter 5 10'+'\n')
        f.write('log '+fit_log_file+'\n')
        f.write('show data'+'\n')
        f.write('show model'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('log none'+'\n')

        f.write('chatter 5 5'+'\n')
        f.write('log '+error_log_file+'\n')
        f.write('parallel error '+str(cores)+'\n')
        f.write('error '+dfs+' 3'+'\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('n'+'\n')
        f.write('\n')
        f.write('log none'+'\n')
        
    #Execution
    nH = '3.2'
    tin_lower = '0.01'
    tin_upper = '1.0'
    simpl_gamma_lower = '1.4'
    simpl_gamma_upper = '3.4'
    simpl_flag = '1'

    for seg_id in IDs:
        print(seg_id)
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        data_path = data_path_temp.replace('++++++++++',obsid)
        data_path = data_path.replace('+',gti)
        if os.path.exists(data_path)==True:
            bg = data_path.replace('.jsgrp','.bg')
       
            #Get .rmf and .arf files
            jsgrp = data_path
            target = jsgrp.replace('.jsgrp','.fits')
            shutil.copyfile(jsgrp, target)
            hdul = fits.open(target)
            rmf = hdul[1].header['RESPFILE']
            arf = hdul[1].header['ANCRFILE']
        
            if os.path.exists(rmf_dir+str(rmf)) == True:
                rmf = rmf_dir+str(rmf)
            else:
                lacking_rmfs.append(seg_id)
        
            if os.path.exists(arf_dir+str(arf)) == True:
                arf = arf_dir+str(arf)
            else:
                lacking_arfs.append(seg_id)

            os.remove(target)

            #Finally, write commands to outfile
            with open(out_file,'a') as f:    
                simpl_commands(fit_log_temp=(log_dir+'simpl++++++++++.log'),error_log_temp=(log_dir+'simpl_error++++++++++.log'))
                
                f.write('quit'+'\n')
                f.write('y'+'\n')

    print(len(lacking_arfs))
    print(len(lacking_rmfs))
    print('\n')
    print('Model: tbabs(simpl(diskbb))')
    print('Delta fit statistic: '+dfs)
    print('Noticed Channels: 0.5-1.5 2.3-10.0 keV')
    print('nH: 3.2 (frozen)')
    print('Tin lower limit: '+tin_lower)
    print('Tin upper limit: '+tin_upper)
    print('Gamma lower limit: '+simpl_gamma_lower)
    print('Gamma upper limit: '+simpl_gamma_upper)
    print('UpScOnly value: '+simpl_flag)
    
#get list of obsids_gti
import os

#get ids

sids = []
with open('/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_one/rpg 1.975.txt','r') as f:
    for line in f:
        if '#' not in line: 
            line = line.replace('\n','')
            path = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
            
            obsid = line.split('_')[0]
            gti = line.split('_')[1]

            path_b = path.replace('++++++++++',obsid)
            path_b = path_b.replace('+',gti)
            if os.path.exists(path_b)==True:
                sids.append(line)

all_ids = []
with open('/home/thaddaeus/FMU/Steiner/ChristmasBreak/all_seg_ids.txt','r') as f:
    for line in f:
        if '#' not in line: 
            line = line.replace('\n','')
            line = line.replace(':','_')
            path = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
            
            obsid = line.split('_')[0]
            gti = line.split('_')[1]

            path_b = path.replace('++++++++++',obsid)
            path_b = path_b.replace('+',gti)
            if os.path.exists(path_b)==True:
                all_ids.append(line)


simpl_ids = []
with open('/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/simpl/rpg 1.975(simpl).txt','r') as f:
    for line in f:
        line = line.replace('\n','')
        path = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
        obsid = line.split('_')[0]
        gti = line.split('_')[1]
        path_b = path.replace('++++++++++',obsid)
        path_b = path_b.replace('+',gti)
        if os.path.exists(path_b)==True:
            simpl_ids.append(line)



dpt = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
simpl(IDs=simpl_ids,data_path_temp=dpt,arf_dir='/home/thaddaeus/FMU/Steiner/thaddaeus/',rmf_dir='/home/thaddaeus/FMU/Steiner/thaddaeus/',log_dir='/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/simpl/logs/',cores=4,iterations=900,dfs='1.',out_file='/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/simpl/fit_commands.txt')


#dpt = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
#nthcomp_v2(IDs=sids,data_path_temp=dpt,arf_dir='/home/thaddaeus/FMU/Steiner/thaddaeus/',rmf_dir='/home/thaddaeus/FMU/Steiner/thaddaeus/',log_dir='/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/nthcomp/logs/',plot_dir='/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/nthcomp/plots/',cores=4,iterations=900,dfs='1.',out_file='/home/thaddaeus/FMU/Steiner/ChristmasBreak/full_run_two/nthcomp/fit_commands.txt',save_plots=True)
