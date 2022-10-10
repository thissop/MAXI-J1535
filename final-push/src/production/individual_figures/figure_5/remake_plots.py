import matplotlib.pyplot as plt 
import os 


def grs_plot_commands(): 
    # 80701-01-54-02,2.759,0.345,13.386,2.7519999999999993,0.33083999999999947,13.422989999999997
    # 50703-01-28-01,3.523,0.729,11.06,3.0962699999999983,0.44462000000000046,11.748149999999995
    # 50703-01-24-01,4.09,0.5880000000000001,8.520000000000001,3.1312599999999993,0.48858999999999997,11.153579999999998

    # best, median, worst
    # amplitudes are as fitted 

    observation_IDs = ['80701-01-54-02', '50703-01-28-01', '50703-01-24-01']
    pythagorean_diffs = [0.040221458203300475, 0.8582079583644016, 2.8044265638629198]
    freq_diffs = [0.007, 0.42673, 0.95874]
    true_values = [[2.759,0.345,13.386], [3.523,0.729,11.06], [4.09,0.588,8.52]]
    predicted_values = [[2.752,0.33084,13.423], [3.09627,0.44462,11.74815], [3.13126,0.48859,11.15358]]

    commands = ['heainit', 'xspec']

    for i in range(3):
        commands.append(f'cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/{observation_IDs[i]}')
        commands.append('data power_0_249.pha')

        commands.append('model loren')
        commands.append('0')
        commands.append('')
        commands.append('')
        commands.append('freeze 1')
        commands.append('query yes')
        commands.append('')
        commands.append('fit')
        commands.append('')
        commands.append('editmod loren+loren ')
        commands.append(f'{predicted_values[i][0]}')
        commands.append(f'{predicted_values[i][1]}')
        commands.append(f'{predicted_values[i][2]}')
        commands.append('show param')
        commands.append('freeze 1-3')
        commands.append('fit')
        commands.append('ignore **-0.1')
        commands.append('ignore 10.0-**')
        commands.append('cpd /s')
        commands.append('setplot energy')
        commands.append('plot ldata')
        commands.append('cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_5')
        commands.append('iplot')
        commands.append('label bottom Frequency (Hz)')
        commands.append('label left Power (Leahy Normalized)')
        commands.append('label top')
        commands.append('font roman')
        commands.append('t off')
        commands.append('View 0.12 0.12')
        commands.append('csize 2.0')
        commands.append('rescale x 0.1 10')
        commands.append('rescale y 1 200')
        commands.append(f'hard  /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_5/{observation_IDs[i]}[fig-5-pds-data].ps/ps')
        #commands.append(f'{observation_IDs[i]}[pds-data]/ps')
        #commands.append(f'{observation_IDs[i]}[pds-data].ps/ps')
        commands.append('quit')
        commands.append('plot model')
        commands.append('iplot')
        commands.append('label top')
        commands.append('font roman')
        commands.append('t off')
        commands.append('label X Frequency (Hz)')
        commands.append('label Y Power (Leahy Normalized)')
        commands.append('View 0.12 0.12')
        commands.append('csize 2.0')
        commands.append('rescale x 0.1 10')
        commands.append('rescale y 1 200')
        commands.append(f'hard  /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_5/{observation_IDs[i]}[fig-5-pds-model].ps/ps')
        #commands.append(f'{observation_IDs[i]}[fig-5-pds-model]/ps')
        #commands.append(f'{observation_IDs[i]}[fig-5-pds-model].ps/ps')
        commands.append('quit')
        commands.append('model none')
        commands.append('data none')

    commands.append('quit')
    commands.append('y')

    with open('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/individual_figures/figure_5/commands.sh', 'w') as f: 
        for line in commands: 
            f.write(f'{line}\n')

#grs_plot_commands()

def ps_to_pdf_cleanup():
    import os
    dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_5/'
    for f in os.listdir(dir):
        if f.split('.')[-1] == 'ps':
            print('changing')
            os.system(f"ps2pdf {dir+f} {dir+f.replace('.ps','.pdf')}")
            os.remove(f"{dir+f}")
        else: 
            print(f.split('.'))

ps_to_pdf_cleanup()