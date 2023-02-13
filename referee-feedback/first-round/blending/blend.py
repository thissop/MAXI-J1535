import pandas as pd
import numpy as np

def add_dud_data(): 
    r'''
    
    Notes
    -----
    - This is a one-time execution type of function that only matters because I'm testing combining data. it's purpose is to add dud 2nd qpos to grs data 
    
    '''
    fp = '/Users/yaroslav/Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/output-data.csv'
    lines = []
    with open(fp, 'r') as f: 
        for line in f: 
            lines.append(line)
            obsid = line.split(',')[0]
            lines.append(f'{obsid},0,0,0'+'\n')
    
    with open(fp, 'w') as f: 
        for line in lines:
            f.write(line)

#add_dud_data()

def quick_plot():
    import matplotlib.pyplot as plt 

    df1  = pd.read_csv('referee-feedback/first-round/blending/input-data.csv')

    df2 = pd.read_csv('referee-feedback/first-round/blending/output-data.csv')

    fig, axs = plt.subplots(2,3, figsize=(6,3))

    cols = ['A','B','C','D','E','F']
    for i in range(2):
        for j in range(3):
            ax = axs[i,j]
            ax.hist(df1[cols[i+j]])
            ax.set(xlabel=cols[i+j])

    plt.tight_layout()
    plt.savefig('referee-feedback/first-round/blending/input-data-dist.pdf')

    plt.clf()

    fig, axs = plt.subplots(3, figsize=(3,4))

    cols = ['frequency','width','rms']

    for i in range(3):
        ax = axs[i]
        ax.hist(df2[cols[i]])
        ax.set(xlabel=cols[i])

    plt.tight_layout()
    plt.savefig('referee-feedback/first-round/blending/output-data-dist.pdf')

    plt.clf()

quick_plot()