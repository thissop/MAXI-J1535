def maxi_pds_plot(observation_ID:str, 
                  out_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_two'):
    
    
    if out_dir[-1]!= '/':
        out_dir+='/'

    commands_file = out_dir+"out.sh"
    plot_path = out_dir+f'{observation_ID}'

    split_id = observation_ID.split('_')
    obsid = split_id[0]
    gti = split_id[1]

    commands = []

    pds_file = f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}-bin.pds'
    fak_file = f'/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}-fak.rsp'
    
    commands.append('data '+pds_file)
    commands.append('none')
    commands.append('response '+fak_file)
    commands.append('ignore **-1.0 20.0-**')

    commands.append('query yes')

    commands.append(r'cpd \xs')
    commands.append('setplot energy')
    commands.append('setplot xlog')
    commands.append('plot data')
    commands.append('iplot')
    commands.append('label top')
    commands.append('label bottom Frequency [Hz]')
    commands.append('label left rms-Normalized Power')
    commands.append('time off')
    commands.append('font roman')
    commands.append(f'hard {plot_path}_data.png/png')
    commands.append('quit\n')

    commands.append('model loren')
    commands.append('0')
    commands.append('')
    commands.append('')
    commands.append('freeze 1')
    commands.append('fit')

    commands.append('editmod loren+loren')
    commands.append('0')
    commands.append('')
    commands.append('')
    commands.append('freeze 1')
    commands.append('fit')

    for i in ['2', '3', '5', '6']:
        commands.append('freeze '+i)

    commands.append(r'cpd \xs')
    commands.append('setplot energy')
    commands.append('setplot xlog')
    commands.append('plot ldata')
    commands.append('iplot')
    commands.append('label top')
    commands.append('label bottom Frequency [Hz]')
    commands.append('label left rms-Normalized Power')
    commands.append('time off')
    commands.append('font roman')
    commands.append(f'hard {plot_path}_background_ldata.png/png')
    commands.append('quit\n')

    commands.append('editmod loren+loren+loren')
    commands.append('2.5,2 2 3 3')
    for i in range(2): 
        commands.append('')

    commands.append('editmod loren+loren+loren+loren')
    commands.append('5,4 4 6 6')
    for i in range(3): 
        commands.append('')

    commands.append('fit')

    commands.append(r'cpd \xs')
    commands.append('setplot energy')
    commands.append('setplot xlog')
    commands.append('plot model')
    commands.append('iplot')
    commands.append('label top')
    commands.append('label bottom Frequency [Hz]')
    commands.append('label left rms-Normalized Power')
    commands.append('time off')
    commands.append('font roman')
    commands.append(f'hard {plot_path}_model.png/png')
    commands.append('quit\n')

    with open(commands_file, 'w') as f: 
        for line in commands: 
            f.write(f'{line}\n')

#maxi_pds_plot('1050360105_21')

def maxi_simpl_routine(observation_ID:str, 
                       out_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_two'):

    pass 

def get_GRS_hardness(working_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra', 
                     commands_file:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/hardness_commands.sh'):
    
    import os
    import pandas as pd
    import numpy as np

    if working_directory[-1]!='/':
        working_directory+='/'

    commands = []

    #commands.append('xspec')

    finished_ids = list(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/hardness.txt')['observation_ID'])

    for sub_dir in np.setdiff1d(os.listdir(working_directory), finished_ids)[0:38]:
        if sub_dir != '.gitkeep' and sub_dir not in finished_ids:
            new_dir = working_directory+sub_dir+'/'
            commands.append(f'cd {new_dir}')

            commands.append('data src_pcu2.pha')

            commands.append('ignore **-3.0 10.0-**')
            commands.append('log soft.txt')
            commands.append('show data')
            commands.append('log none')
            commands.append('notice **-**')
            commands.append('ignore **-10.0 50.0-**')
            commands.append('log hard.txt')
            commands.append('show data')
            commands.append('log none')
            #commands.append('quit\n\n')

            commands.append('data none')

            python = 'python '+'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/get_hardness.py '
            python += new_dir 

            commands.append(python)

        else:
            print(sub_dir)

    commands.append('')
    commands.append('quit\n')
    commands.append('xspec\n')

    with open(commands_file, 'w') as f: 
        for line in commands: 
            f.write(line+'\n')


get_GRS_hardness()