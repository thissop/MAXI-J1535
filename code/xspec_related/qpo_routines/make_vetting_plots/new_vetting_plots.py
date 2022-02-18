from matplotlib import markers
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tqdm import tqdm 

plt.style.use(r"C:\Users\Research\Documents\GitHub\sunnyhills\other\aesthetics\science.mplstyle")
data_dir = './code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw'
pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
plot_dir = './code/xspec_related/qpo_routines/make_vetting_plots/plots'

all_ids = list(pd.read_csv('./code/xspec_related/good_ids.csv')['full_id'])

for full_id in tqdm(all_ids): 
    full_id = '1050360104_5'
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    image_data = data_dir+'/'+full_id+'_plot-data.csv'
    image_data = pd.read_csv(image_data)

    x = np.array(image_data['x'])
    y = np.array(image_data['y'])
    xerr = np.array(image_data['xerr'])
    yerr = np.array(image_data['yerr'])

    ### MAKE PLOT ###
    fig = plt.figure(constrained_layout=True, figsize=(7,4))
    mosaic = """
        AB
        CD
        EF
        """
    ax_dict = fig.subplot_mosaic(mosaic)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    ax = ax_dict['A']

    for ax_str in ['C','D']: 
        ax = ax_dict[ax_str]
        ax.plot(image_data.e, image_data.total,label='Total Continuum  Model')
        ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
        ax.set_ylim(bottom=10**-5)

        '''
        for j in range(2):
            ax.plot(image_data.e, image_data[f'model{j}'],label=f'{comp_labels[j]}')
        ax.legend()
        '''

    for ax_str in ['A','B','C','D']: 
        ax = ax_dict[ax_str]
        ax.set(xlim=(0.1,20), xscale='log', yscale='log')


    # Annotations Info

    ax = ax_dict['E']
    ax.axis('off')
    ax.set(title='Detected QPO Frequencies')

    ax = ax_dict['F']
    ax.axis('off')
    ax.set(title='Initial Annotations')

    message = 'hmmm. just like the one above? not sure though.'
    ax.text(0.1, 0.5, message)

    plt.savefig('example-(work in progress).png', bbox_inches='tight', dpi=150)
    break





'''

### from the model plotting part ###

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df.e, df.total, color='red',label='Total model',linewidth=3)
for j in range(ncomp):
    ax.plot(df.e, df[f'model{j}'],label=f'{m1.componentNames[j]}')

ax.set_xlabel('Energy (keV)')
ax.set_ylabel(r'counts/s/keV')
ax.set_xscale("linear")
ax.set_yscale("linear")
ax.legend()
ax.set(xlim=(0.1,20))
'''