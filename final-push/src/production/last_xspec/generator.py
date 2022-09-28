def generate_grs_commands():
    r'''
    
    these are kinda cracked...only for one time final use

    ''' 

    import pandas as pd 
    import numpy as np

    observation_IDs = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv')['observation_ID'])
    commands = ['heainit', 'xspec', 'chatter 5 10']

    for observation_ID in observation_IDs: 
        commands.append(f'cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/{observation_ID}')
        commands.append('data src_pcu2.pha')
        commands.append('ignore **-2.5')
        commands.append('ignore 25.0-**')
        commands.append('ignore bad')
        commands.append('model tbabs*(diskbb+nthcomp)')

        commands.append('6.0') # nH
        # need to freeze! 
        commands.append( ', , 0.2 0.2 3 3') #diskbb Tin
        commands.append('') # diskbb norm
        commands.append(', , 1.1 1.1 3.5 4.0') # nthcomp gamma 
        commands.append(', , 4 4 40 40') # high energy rollover  
        commands.append('=p2') # low temp 
        commands.append('1') # input type = disk blackbody --> freeze!
        commands.append('0') # redshift --> freeze! 
        commands.append('') # nthcomp norm 

        commands.append('freeze 1 7 8')
        commands.append('query no')
        commands.append('fit 400')

        log_file = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/temp_dir/GRS|{observation_ID}|.txt'

        commands.append(f'log {log_file}')
        commands.append('show data')
        commands.append('show param')
        commands.append('show fit')
        commands.append('log none')
        commands.append('data none')
        commands.append('model none')

        commands.append('python /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/aggregator.py')

    commands.append('quit\ny\n')

    out_str = '\n'.join(commands)
    with open('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/grs_commands.txt', 'w') as fx: 
        fx.write(out_str)

def generate_maxi_commands():
    r'''
    
    these are kinda cracked...only for one time final use

    ''' 

    import pandas as pd 
    import numpy as np

    observation_IDs = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv')['observation_ID'])
    commands = ['heainit', 'xspec', 'chatter 5 10']

    commands.append('cd /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/')

    for observation_ID in observation_IDs: 
        obsid_list = observation_ID.split('_')
        obsid = obsid_list[0]
        gti = obsid_list[1]
        commands.append(f'data /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/{obsid}/jspipe/js_ni{obsid}_0mpu7_silver_GTI{gti}.jsgrp')
        commands.append('ignore **-0.5 10.0-**')
        commands.append('ignore 1.5-2.3')
        commands.append('ignore bad')
        commands.append('model tbabs*(diskbb+nthcomp)')

        commands.append('3.2107') # nH
        # need to freeze! 
        commands.append( ', , 0.2 0.2 3 3') #diskbb Tin
        commands.append('') # diskbb norm
        commands.append(', , 1.1 1.1 3.5 4.0') # nthcomp gamma 
        commands.append(', , 4 4 250 250') # high energy rollover --> freeze!  --> frozen after cuneo value
        commands.append('=p2') # low temp 
        commands.append('1') # input type = disk blackbody --> freeze!
        commands.append('0') # redshift --> freeze! 
        commands.append('') # nthcomp norm 

        commands.append('freeze 1 7 8')
        commands.append('query no')
        commands.append('fit 400')

        log_file = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/temp_dir/MAXI|{observation_ID}|.txt'

        commands.append(f'log {log_file}')
        commands.append('show data')
        commands.append('show param')
        commands.append('show fit')
        commands.append('log none')
        commands.append('data none')
        commands.append('model none')

        commands.append('python /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/aggregator.py')

    commands.append('quit\ny\n')

    out_str = '\n'.join(commands)
    with open('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/maxi_commands.txt', 'w') as fx: 
        fx.write(out_str)
 

generate_grs_commands()
generate_maxi_commands()