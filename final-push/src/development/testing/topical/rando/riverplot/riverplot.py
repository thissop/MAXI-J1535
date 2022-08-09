def pds_riverplot(obsids:list, csv_data_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/older/code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw/'):
    import matplotlib.pyplot as plt
    import numpy as np
    import os 
    import pandas as pd 
    import seaborn as sns
    
    #sns.set_style('white')

    matrix = []

    ordinate = None 
    
    for counter, file in enumerate(os.listdir(csv_data_dir)):
        for obsid in obsids: 
            if obsid in file:
                df = pd.read_csv(csv_data_dir+file)
                if len(df.index)==225:
                    x, y = (np.array(df[i]) for i in ['x', 'y'])
                    matrix.append(x*y)
                    if ordinate is None: 
                        ordinate = [str(i) for i in x] 

                break 
    
    matrix = np.array(matrix)

    fig, ax = plt.subplots(figsize=(4,2))
    sns.heatmap(data=matrix, ax=ax, lw=0, cmap='viridis', cbar_kws={'shrink':0.75, 'label':'Frequency x Power'}) # f x PDS Power (rms)
    #ax.set_xticks(ticks=ax.get_xticks(), labels=ordinate)
    ax.set(xticks=[], yticks=[], xlabel='Frequency [Hz]', ylabel='GTI')
    plt.tight_layout() # xlim was given in 0.1, 1, 10, 100 and seemed uniformly spaced...so log transformed? 
    plt.savefig(f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/rando/riverplot/temp.png')

pds_riverplot(['1050360103', '1050360104', '1050360105', '1050360106', '1050360107', '1050360108', '1050360109', '1050360110'])