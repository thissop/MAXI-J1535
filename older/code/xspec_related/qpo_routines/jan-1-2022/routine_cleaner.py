import sys
import os
import numpy as np
import pandas as pd
import re

id = sys.argv[1]
logs_dir = sys.argv[2]
save_dir = sys.argv[3]

freqs = []
widths = []
norms = []

fit_stats = []
redchis = []

freqs_arr = 10**np.linspace(0.02, np.log10(20), 268)

all_files = os.listdir(logs_dir)

for file in all_files: 
    if '.txt' in file: 
        full_path = logs_dir + '/' +file
        freq_index = int(file.split(':')[1][:-4])
        freq = freqs_arr[freq_index]
        freqs.append(freq)
        with open(full_path, 'r') as f: 
            for line in f: 
                if 'lorentz' in line and 'frozen' not in line: 
                    if 'norm' in line: 
                        norm = float((re.sub(' +',',',line)).split(',')[5])
                        norms.append(norm)
                
                if 'Width' in line and 'frozen' not in line: 
                    width = float((re.sub(' +',',',line)).split(',')[6])
                    widths.append(width)
                elif '#Test statistic' in line: 
                    fit_stat = float((re.sub(' +',',',line)).split(',')[4])
                elif 'degrees of freedom' in line:
                    dof = float((re.sub(' +',',',line)).split(',')[7])
            
            red_chi = fit_stat/dof
            redchis.append(red_chi)
            fit_stats.append(fit_stat)
        
        os.remove(full_path)

zipped = list(zip(freqs, widths, norms, fit_stats, redchis))

col_names = ['freq', 'fwhm', 'norm', 'fit_stat', 'redchi']

df = pd.DataFrame(zipped, columns=col_names, dtype=object)
df = df.sort_values(by='freq')
df.to_csv(save_dir+'/'+id+'.csv', index=False)

with open('/home/thaddaeus/GitHub/MAXI-J1535/sanity.txt', 'a') as f:
    f.write('another one (id: '+id+')\n')