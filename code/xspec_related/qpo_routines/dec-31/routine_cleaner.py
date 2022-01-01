import sys
import os
import numpy as np
import pandas as pd
import re

id = sys.argv[1]

freqs = []
widths = []
norms = []

fit_stats = []
redchis = []

freqs_arr = 10**np.linspace(0.02, np.log10(20), 268)

for file in os.listdir(): 
    if '.txt' in file: 
        freq_index = file.split('_')[:-4]
        freq = freqs_arr[freq_index]
        
        freqs.append(freq)

        with open(file, 'r') as f: 
            for line in f: 
                if 'lorentz' in line and 'frozen' not in line: 
                    if 'norm' in line: 
                        norm = float((re.sub(' +',',',line)).split(',')[5])
                        norms.append(norm)
                
                if 'Width' in line and 'frozen' not in line: 
                    width = float((re.sub(' +',',',line)).split(',')[6])
                    widths.append(width)
                
                elif 'Test statistic' in line: 
                    fit_stat = float((re.sub(' +',',',line)).split(',')[4])
                
                elif 'degrees of freedom' in line:
                    dof = float((re.sub(' +',',',line)).split(',')[7])
            
            red_chi = fit_stat/dof
            redchis.append(red_chi)
            fit_stats.append(fit_stats)


        os.remove(file)

# need to sort df on freqs column

zipped = list(zip(freqs, widths, norms, fit_stats, redchis))

col_names = ['freq', 'fwhm', 'norm', 'fit_stat', 'redchi']

df = pd.DataFrame(zipped, columns=col_names)
df = df.sort_values(by='freq', axis=1)
df.to_csv(id+'.csv', index=False)