import sys
import os
import numpy as np
import pandas as pd

id = sys.argv[1]

freqs = []
norms = []
chis = []

freqs_arr = 10**np.linspace(0.02, np.log10(20), 268)

for file in os.listdir(): 
    if '.txt' in file: 
        freq_index = file.split('_')[:-4]
        freq = freqs_arr[freq_index]
        
        freqs.append(freq)




        os.remove(file)

# need to sort df on freqs column

zipped = list(zip(freqs, norms, chis))
df = pd.DataFrame(zipped, columns=['freq','norm','chi-stat'])
df = df.sort_values(by='freq', axis=1)
df.to_csv(id+'.csv', index=False)