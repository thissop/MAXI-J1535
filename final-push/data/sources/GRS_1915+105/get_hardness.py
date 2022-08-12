import sys
import os 
import re
from threading import local

local_directory = sys.argv[1]

temp_path = local_directory 
if temp_path[-1]=='/':
    temp_path = temp_path[:-1]
obsid = temp_path.split('/')[-1]

master_log = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/hardness.txt'

if not os.path.exists(master_log): 
    with open(master_log, 'w') as f: 
        f.write('observation_ID,hardness_ratio'+'\n') 

soft_file = local_directory+'/soft.txt'
hard_file = local_directory+'/hard.txt'

soft, hard = (None, None)

hardness = None

with open(soft_file, 'r') as f: 
    for line in f: 
        if '#Net count rate (cts/s) for Spectrum:1' in line: 
            line_list = re.sub(' +', ',', line).split(',')
            soft = float(line_list[6])

with open(hard_file, 'r') as f: 
    for line in f: 
            if '#Net count rate (cts/s) for Spectrum:1' in line: 
                line_list = re.sub(' +', ',', line).split(',')
                hard = float(line_list[6])

hardness = soft/hard 

#os.remove(soft_file)
#os.remove(hard_file)

with open(master_log, 'a') as f: 
    f.write(f'{obsid},{hardness}\n')