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

add_dud_data()