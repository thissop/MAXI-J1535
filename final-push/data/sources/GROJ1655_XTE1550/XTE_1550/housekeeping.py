def make_better_info_files():
    r'''
    
    not relevant anymore ... I was just tweaking the info 26 files ...
    
    '''

    
    import numpy as np
    import pandas as pd

    columns = np.array(pd.read_csv('final-push/data/sources/XTE_1550/info_cols.txt')['column'])

    GRO_DF = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/thaddaeus_xtefiles/GRO_J1655/groj1655_seg_2013.info26', columns=columns)
    print(GRO_DF)

make_better_info_files()
