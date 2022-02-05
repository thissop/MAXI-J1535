def write_commands(key, data_dir, params_dict, log_dir, commands_file):    
    import pandas as pd
    import numpy as np
    import os
    from astropy.io import fits
    import shutil

    good_ids = pd.read_csv(key)['full_id']


    commands = []
    with open(commands_file, 'w') as f: # clear contents
        commands.append('heainit')
    
    for seg_id in good_ids:
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        data_file = data_dir + '/' + obsid + '/jspipe/js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
        windows_data_file = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus" 
        windows_data_file = os.path.join(windows_data_file, obsid + r'\jspipe\js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp') 
        
        if os.path.exists(windows_data_file)==True:
            # .bg file
            windows_bg = windows_data_file.replace('.jsgrp','.bg')
            
            jsgrp = data_file
            bg = jsgrp.replace('.jsgrp', '.bg')
            
            #Get .rmf and .arf files
            windows_jsgrp = windows_data_file
            #target = jsgrp.replace('.jsgrp','.fits')
            #shutil.copyfile(jsgrp, target)
            hdul = fits.open(windows_jsgrp)
            rmf_file = data_dir + '/' + str(hdul[1].header['RESPFILE'])
            arf_file = data_dir + '/' + str(hdul[1].header['ANCRFILE'])
        
            #os.remove(target)
            
            # Append commands
            commands.append('xspec')
            #commands.append('query yes')
            commands.append('data ' + jsgrp)
            commands.append('none')
            commands.append('none')
            commands.append('backgrnd '+bg)
            commands.append('response '+rmf_file)
            commands.append('arf '+arf_file)
            
            commands.append('ignore **-0.5 1.5-2.3 10.0-**') #Often modified, e.g. sometimes 1.5-2.3 as well
            
            commands.append('ignore bad')
            tcl_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/common.tcl'
            commands.append('source '+tcl_path)
            commands.append('statistic pgstat')
            commands.append('setp back on')
            commands.append('energies 0.01 200. 1000 log') # only for simpl 
            commands.append('model tbabs(simpl(diskbb))') # or nthcomp 
            
            commands.append('3.2107 , 2 2 5 5') # tbabs nH 
    

            gamma_init = [str(i) for i in params_dict['simpl_gamma']]
            commands.append(' '.join(gamma_init)) # simple gamma

            scat_frac_init = [str(i) for i in params_dict['simpl_scat_frac']]
            commands.append(' '.join(scat_frac_init))
            
            commands.append('1') 

            tin_init = [str(i) for i in params_dict['diskbb_tin']]
            commands.append(' '.join(tin_init)) # diskbb Tin 
            commands.append(', , 0.1 0.1 '+str(10**9)+' '+str(10**9)) # diskbb norm 

            # simpl values
            # 1. gamma -->  
            # 2. scattered fraction --> 
            # 3. flag to switch from up scattering only (>0) or both up and down (<0) --> set to 1

            commands.append('freeze 1') # FIX? 
            commands.append('chatter 5 10') # FIX? 
            
            cores = '2'
            commands.append('parallel leven '+ cores)
            commands.append('fit 250')
            commands.append('n')
            commands.append('')
            
            # Error routine
            log_file = log_dir+'/'+seg_id+'_before_error.txt' 
            errorlog_file = log_dir + '/'+seg_id+'_errorlog.txt' 
            
            # do initial log because of the issue discussed in jupyter notebook

            commands.append('log '+log_file)
            commands.append('show data')
            commands.append('show param')
            commands.append('show fit')
            commands.append('log none')

            # See if red. pgstat < 3, if so do error routine
            
            commands.append('tclout stat')
            commands.append('scan $xspec_tclout "%f" pgstat')
            commands.append('tclout dof')
            commands.append('scan $xspec_tclout "%f" dof')
            commands.append('set redpgstat [expr $pgstat / $dof]')
            commands.append('if {$redpgstat < 3} {')
            commands.append('set error_array [_pct_get_error_list {2 3 4 5} 2.706]')
            commands.append('set error_log_file [open ' + errorlog_file + ' w]')
            commands.append('set header_string "value,lower_err,upper_err,err_str" ')
            commands.append('puts $error_log_file $header_string')
            commands.append('foreach item $error_array {')
            commands.append('set item [join $item ,]')
            commands.append('puts $error_log_file $item')
            commands.append('}')
            commands.append('close $error_log_file')
            commands.append('}')
            
            commands.append('quit')
            commands.append('y')
            commands.append('sleep 0.5') # sleep for 0.5 seconds between iterations
            
            commands.append('model clear')
            commands.append('data none')

    with open(commands_file, 'w') as f:
        for command in commands: 
            f.write(command+'\n')


key = r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\xspec_related\good_ids.csv'
data_dir = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus'

work_dir = './code/xspec_related/spectral_routines/jan-29-simpl'
log_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/logs'
commands_file =r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\xspec_related\spectral_routines\jan-29-simpl\commands.txt'

# value, step, hard lower, soft lower, soft upper, hard upper 
params_dict = {'diskbb_tin':[',', ',', 0.2, 0.2, 2, 3],
               'nthcomp_gamma':[',',',',1.1, 1.2, 3.5, 4], 
               'simpl_gamma':[2.0,0.05,1.1,1.4,3.5,4.], 
               'simpl_scat_frac':[0.1,0.1,0.001,0.01,0.9,1.]
              }

write_commands(key, data_dir, params_dict, log_dir, commands_file)