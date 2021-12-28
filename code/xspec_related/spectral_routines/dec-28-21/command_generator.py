def write_commands(key, data_dir, log_dir, commands_file): 
    '''
    key: .csv file with column of observation ids, e.g. 101010201_13 
         values.
    data_dir: directory of data files
    log_dir: directory for log files
    commands_file: path to file into which commands should be deposited.
    '''
    
    # Import(s)
    import os
    import numpy as np
    import pandas as pd
    from astropy.io import fits
    import shutil
    
    # Action
    df = pd.read_csv(key)
    ids = np.array(df['ID'])
    np.random.shuffle(ids)
    
    commands = []
    with open(commands_file, 'w') as f: # clear contents
        commands.append('heainit')
    
    for seg_id in ids:
        obsid = seg_id.split('_')[0]
        gti = seg_id.split('_')[1]
        data_file = data_dir + '/' + obsid + '/jspipe/js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
        if os.path.exists(data_file)==True:
            # .bg file
            bg = data_file.replace('.jsgrp','.bg')

            #Get .rmf and .arf files
            jsgrp = data_file
            target = jsgrp.replace('.jsgrp','.fits')
            shutil.copyfile(jsgrp, target)
            hdul = fits.open(target)
            rmf_file = data_dir + '/' + str(hdul[1].header['RESPFILE'])
            arf_file = data_dir + '/' + str(hdul[1].header['ANCRFILE'])
        
            os.remove(target)
            
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
            
            commands.append('statistic pgstat')
            commands.append('setp back on')
            commands.append('model tbabs(diskbb+nthcomp)')
            
            commands.append('3.21 , 2 2 5 5') # tbabs nH 

            commands.append(', , 0.2 0.2 1 1') # diskbb Tin 
            commands.append(', , 0.1 0.1 '+str(10**9)+' '+str(10**9)) # diskbb norm 
            
            commands.append(', , 1.1 1.1 3.5 4.5') # nthcomp gamma
            commands.append('100') # nthcomp high energy rollover 
            commands.append('=p2') # nthcomp seed temp
            commands.append('1') # nthcomp input_type
            commands.append('0') # nthcomp redshift
            commands.append('') # nthcomp norm
            
            commands.append('freeze 1 5')
            commands.append('chatter 5 10')
            
            cores = '2'
            commands.append('parallel leven '+ cores)
            commands.append('fit 100')
            commands.append('n')
            commands.append('')
            
            # Error routine 
            errorlog_file = log_dir + '/'+seg_id+'_errorlog.txt' 
            
            commands.append('tclout stat')
            commands.append('scan $xspec_tclout "%f" pgstat')
            commands.append('tclout dof')
            commands.append('scan $xspec_tclout "%f" dof')
            commands.append('set redpgstat [expr $pgstat / $dof]')
            commands.append('set errorfile [open "'+errorlog_file+'" a+]')
            commands.append('puts $errorfile "param_num,lower_bound,upper_bound,error_string"')
            # See if red. pgstat < 2, if so do error routine
            commands.append("if {$redpgstat < 2} {")
            for param_num in [2, 3, 4, 9]: 
                commands.append('error 1. '+str(param_num))
                commands.append('tclout error ' +str(param_num))
                commands.append('set tclout_error_str [join $xspec_tclout ,]') # this isn't working
                commands.append('set param_str '+str(param_num)+',')
                commands.append('set error_string $param_str$tclout_error_str')
                commands.append('puts $errorfile $error_string')
            
            # in place of error file
            commands.append("} else {")
            commands.append('puts $errorfile ",,,"') # NaN-ing it
            commands.append('puts $errorfile ",,,"')
            commands.append('puts $errorfile ",,,"')
            commands.append('puts $errorfile ",,,"')
            commands.append("}")
            
            commands.append('close $errorfile')
                        
            log_file = log_dir+'/'+seg_id+'.txt'
            commands.append('log '+log_file)
            commands.append('show data')
            commands.append('show param')
            commands.append('show fit')
            commands.append('log none')
            
            commands.append('quit')
            commands.append('y')
            commands.append('sleep 0.5') # sleep for 0.5 seconds between iterations
    
    with open(commands_file, 'w') as f:
        for command in commands: 
            f.write(command+'\n')
    
key = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/misc/all_seg_ids.csv'
data_dir = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus'

work_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/machine_learning/second_attempt/mk2_spectral_fits/1.5_2.3_ignored'
log_dir = work_dir+'/logs'
commands_file = work_dir+'/commands.txt'
write_commands(key, data_dir, log_dir, commands_file)