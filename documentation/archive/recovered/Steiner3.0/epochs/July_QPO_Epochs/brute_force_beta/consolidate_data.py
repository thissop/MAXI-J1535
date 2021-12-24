# Import(s)
import os
import numpy as np
import pandas as pd
import re 

# Definitions
def split_line(line):
    return re.sub(' +', ',', line).split(',')

# Action

logs_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/beta_run/logs'
out_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/beta_run/fitted_param_files'

ids = np.array(os.listdir(logs_dir))

for id in ids: 
    sub_dir = os.path.join(logs_dir, id)
    indices = np.array([])
    
    freqs = np.array([])
    widths = np.array([])
    norms = np.array([])
    
    for index, data_file in enumerate(np.sort(os.listdir(sub_dir))):
        indices = np.append(indices, index)
        with open(os.path.join(sub_dir, data_file), 'r') as f:
            for line in f: 
                if '#   1    1   lorentz    LineE' in line: 
                    freq = split_line(line)[6]
                    freqs = np.append(freqs, freq)
                    
                elif '#   2    1   lorentz    Width' in line: 
                    width = split_line(line)[6]
                    widths = np.append(widths, width)
                    
                elif '#   3    1   lorentz    norm' in line: 
                    norm = split_line(line)[5]
                    norms = np.append(norms, norm)
                    
    zipped = list(zip(indices.astype(int), freqs, widths, norms))
    df = pd.DataFrame(zipped, columns=['Index', 'Frequency', 'Width', 'Norm'])
    df.to_csv(os.path.join(out_dir, id+'.csv'), index=False)
            
    