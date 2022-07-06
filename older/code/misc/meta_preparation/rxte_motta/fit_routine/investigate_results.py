def get_ktes(results_file:str=r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\misc\meta_preparation\rxte_motta\fit_routine\results\test.csv'):
    import os
    import weighted     
    import pandas as pd
    import numpy as np

    df = pd.read_csv(results_file) 
    mask = df['kT_e']<=300 
    df = df.iloc[mask.to_list()] 
    median = weighted.median(df['kT_e'], 1/(df['red_pgstat'])) 
    print('weighted', median) 
    print('normal:', np.median(df['kT_e'])) 
    print('mean:', np.mean(df['kT_e']))

get_ktes()