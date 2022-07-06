def qpo_hunter_mk3(key, working_dir, pds_temp, fak_temp, clean_file):
    # Import(s)
    import numpy as np
    import os
    import pandas as pd
    
    # Action
    df = pd.read_csv(key)
    ids = np.array(df['ID'])
    np.random.shuffle(ids)
    #ids = [ids[0]]
    #ids = ['1130360199_1']

    out_file = working_dir + '/commands.txt'
    logs_dir = working_dir + '/temp_logs'
    
    #logs_dir = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/dec-31/diagnostic_logs'

    if os.path.exists(logs_dir)==False: 
        os.mkdir(logs_dir)
    
    freqs_arr = 10**np.linspace(0.02, np.log10(20), 268)[0:267]
    #freqs_arr = 10**np.linspace(0.02, np.log10(20), 2)[0:1]
    last_freq = 20

    commands = []
    cap = commands.append

    cap('heainit')
    cap('xspec')
    cap('chatter 5 10')
    cap('setplot energy')

    sanity_counter = 0
    for id in ids: 
        sanity_counter += 1
        split_id = id.split('_')
        obs_id = split_id[0]
        seg_num = split_id[1]
    
        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', seg_num)

        fak_file = fak_temp.replace('+++', obs_id)
        fak_file = fak_file.replace('***', seg_num)
        
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
        for freq in freqs_arr:
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
            
            log_file = logs_dir+'/'+id+':'+str(counter)+'.txt'
            cap('log '+log_file)
            cap('show parame')
            cap('show fit')
            cap('log none')
                    
            counter = counter + 1
            
            cap('delcomp 1')

        # add last freq commands
        width = str(0.1*last_freq)
        lower_width = str(0.09*last_freq)
        upper_width = str(0.11*last_freq)
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
        
        log_file = logs_dir+'/'+id+':'+str(counter)+'.txt'
        cap('chatter 10')
        cap('log '+log_file)
        cap('show parame')
        cap('show fit')
        cap('log none')
        cap('chatter 5')
        
        cap('delcomp 1')

        # tcl activation of python cleaning
        #completed_dir = logs_dir
        completed_dir = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/jan-1-2022/final_logs'
        cap('exec python3 '+clean_file+' '+id + ' '+logs_dir + ' ' + completed_dir)
            
        # clear model
        # clear data
        cap('model clear')
        cap('data none')

        # quicker than restarting xspec every time

    cap('quit\ny\n')  
    if out_file.lower() == 'print':
        for command in commands: 
            print(command)
    else: 
        with open(out_file, 'a') as f:
            for command in commands: 
                f.write(command+'\n')

key = '/home/thaddaeus/GitHub/MAXI-J1535/code/all_seg_ids.csv'
working_dir = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/jan-1-2022'

pds_temp = '/home/thaddaeus/FMU/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
fak_temp = '/home/thaddaeus/FMU/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'
clean_file = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/jan-1-2022/routine_cleaner.py'

qpo_hunter_mk3(key, working_dir, pds_temp, fak_temp, clean_file)