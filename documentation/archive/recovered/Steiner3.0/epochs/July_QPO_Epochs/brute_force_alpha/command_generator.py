def qpo_hunter_mk_2(ids, working_dir, pds_temp, fak_temp):
    # Import(s)
    import numpy as np
    import os
    
    # Action
    out_file = working_dir + '/commands.txt'
    logs_dir = working_dir + '/logs'
    
    if os.path.exists(logs_dir)==False: 
        os.mkdir(logs_dir)
    
    for id in ids: 
        log_dir = logs_dir + '/' + id
        
        if os.path.exists(log_dir)==False:
            os.mkdir(log_dir)
        
        obs_id = id.split('_')[0]
        seg_num = id.split('_')[1]
    
        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', seg_num)

        fak_file = fak_temp.replace('+++', obs_id)
        fak_file = fak_file.replace('***', seg_num)
        
        commands = []
        cap = commands.append
        
        cap('heainit')

        cap('xspec')
        cap('setplot energy')
        cap('data '+pds_file)
        cap('none')
        cap('response '+fak_file)
        cap('query yes')
        cap('ignore **-0.02 100.-**')

        cap('model loren')
        cap('0')
        cap('')
        cap('')
        cap('freeze 1')
        cap('fit')

        cap('editmod loren+loren')
        cap('0')
        cap('')
        cap('')
        cap('freeze 1')
        cap('fit')

        for i in ['2', '3', '5', '6']:
            cap('freeze '+i)
            
        # BRUTE FORCE PART
        counter = 0
        for freq in 10**np.linspace(0.02, np.log10(20), 268):
            width = str(0.1*freq)
            lower_width = str(0.09*freq)
            upper_width = str(0.11*freq)
            cap('editmod loren+loren+loren')
            cap(str(freq))
            width_str = width + ' , ' + lower_width + ' ' + lower_width+ ' ' 
            width_str = width_str + upper_width + ' ' + upper_width
            cap(width_str)
            cap('')
            cap('freeze 1 2')
            cap('fit')
            cap('thaw 2')
            cap('newpar 2')
            cap(', , '+ lower_width + ' ' + lower_width+ ' '+ upper_width + ' ' + upper_width)
            cap('fit')
            
            log_file = log_dir+'/'+id+'_'+str(counter)+'.txt'
            cap('log '+log_file)
            cap('show parame')
            cap('show fit')
            cap('log none')
                    
            counter = counter + 1
            
            cap('delcomp 1')
            
        cap('quit\ny')
        
        if out_file.lower() == 'print':
            for command in commands: 
                print(command)
        else: 
            with open(out_file, 'a') as f:
                for command in commands: 
                    f.write(command+'\n')
                  
import pandas as pd
  
ids = list(pd.read_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/temp_ids.txt')['ID'])
working_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/first_routine'
pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
fak_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'

qpo_hunter_mk_2(ids, working_dir, pds_temp, fak_temp)