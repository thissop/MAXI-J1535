import os
import numpy as np
import pandas as pd 

x = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/MAXI/[dates].csv')['MJD'])
print('MAXI: ', np.min(x), np.max(x), np.max(x)-np.min(x))

x = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[dates].csv')['MJD'])
print('GRS: ', np.min(x), np.max(x), np.max(x)-np.min(x))