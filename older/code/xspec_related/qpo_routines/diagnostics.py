import pandas as pd
import os 
import matplotlib.pyplot as plt
import numpy as np

num_rows = []
ids = []
base_dir = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/dec-31/logs/'
for file in os.listdir(base_dir): 
    if '.csv' in file: 
        line_count = sum(1 for i in open(base_dir+file, 'r'))
        num_rows.append(line_count)
        ids.append(file.split('.csv')[0])

#plt.hist(num_rows, bins=100)
#plt.xscale('log')
#plt.show()

for id, count in zip(ids, num_rows):
    if count > 269: 
        print(id, count)