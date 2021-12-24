def first_attempt(ids, out_file, log_dir, plot_dir):
    import os
    import numpy as np
    import pandas as pd
    
    
    class_one_dir = '/home/thaddaeus/FMU/Steiner2.0/21Apr/classified_plots/class_one'
    class_two_dir = class_one_dir.replace('class_one', 'class_two')
    ids = [i.replace('.png', '') for i in os.listdir(class_one_dir)]
    ids2 = [i.replace('.png', '') for i in os.listdir(class_one_dir)]
    
    ids = np.concatenate((ids, ids2))
    
    
    ### ONLY FOR SOMETHING ELSE 
    ids = np.array(pd.read_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/aug1-aug7_work/sample_cuts/final_ids.csv')['ids'])
    
    commands = []
    cap = commands.append
    cap('heainit')
    
    for id in ids: 
        
        obs_id = id.split('_')[0]
        seg_num = id.split('_')[1]
        
        pds_file = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'.replace('+++', obs_id)
        pds_file = pds_file.replace('***', seg_num)
        
        fak_file = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'.replace('+++', obs_id)
        fak_file = fak_file.replace('***', seg_num)
        
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
        
        #cap('editmod loren+loren+loren')
        #cap('')
        #cap('')
        #cap('')
        #cap('fit')
        
        #cap('editmod loren+loren+loren+loren')
        #cap('')
        #cap('')
        #cap('')
        #cap('fit')
        
        cap('cpd /xs')
        cap('plot data')
        
        cap('iplot')
        #cap('color 1 on 1')
        #cap('color 2 on 2')
        #cap('color 2 on 3')
        #cap('color 2 on 4')
        cap('la x frequency [Hz]')
        cap('la y rms normalized power')
        
        plot_path = os.path.join(plot_dir, (id+'.png'))
        cap('hard '+plot_path+'/png')
        
        cap('quit')
        #log_file = log_dir+'/'+id+'.txt'
        ##cap('log '+log_file)
        #cap('show parame')
        #cap('show fit')
        #cap('log none')
        cap('quit\ny')
        
    if out_file.lower() == 'print':
        for command in commands: 
            print(command)
    else: 
        with open(out_file, 'w') as f:
            for command in commands: 
                f.write(command+'\n')
        
log_dir = '/home/thaddaeus/FMU/Steiner3.0/alpha_qpo_fitting/first_run/logs'

plot_dir = '/home/thaddaeus/FMU/Steiner3.0/alpha_qpo_fitting/first_run/plots'
out_file = '/home/thaddaeus/FMU/Steiner3.0/alpha_qpo_fitting/commands.txt'

first_attempt('', out_file, log_dir, plot_dir)