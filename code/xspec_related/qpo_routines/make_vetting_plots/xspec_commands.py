def make_pds(key, pds_temp, fak_temp, plot_dir):
    import numpy as np
    import os
    import pandas as pd

    df = pd.read_csv(key)
    ids = np.array(df['full_id'])
    np.random.shuffle(ids) 

    out_file = 'commands.txt'

    commands = []
    cap = commands.append

    cap('heainit')
    cap('xspec')
    cap('chatter 5 10')
    cap('setplot energy')

    for obs_id in ids: 
        split_id = obs_id.split('_')
        obs_id = split_id[0]
        gti = split_id[1]
    
        pds_file = pds_temp.replace('+++', obs_id)
        pds_file = pds_file.replace('***', gti)

        fak_file = fak_temp.replace('+++', obs_id)
        fak_file = fak_file.replace('***', gti)

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

        #cap('setplot energy'+'\n')
        cap('plot data'+'\n')
        cap('iplot'+'\n')
        cap('r x 0.1 20')
        cap('la x frequency [hz]')
        cap('la y rms-normalized power ')
        #cap('e off')
        cap('font roman')
        plot_path = plot_dir + obs_id + '.png'
        cap('hard '+plot_path+'/png'+'\n')
        cap('quit'+'\n')

        break

    for i in commands: 
        print(i)


key = './code/xspec_related/good_ids.csv'
pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***_BAND1-bin.pds'
fak_temp = pds_temp.replace('bin.pds','fak.rsp')
plot_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/make_vetting_plots/plots/'
make_pds(key, pds_temp, fak_temp, plot_dir)