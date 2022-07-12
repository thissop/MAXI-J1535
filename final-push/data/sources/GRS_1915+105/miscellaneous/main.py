def first_plot():
    import pandas as pd 
    import numpy as np
    import matplotlib.pyplot as plt 

    df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/miscellaneous/recovering_harmonics/example.txt')
    arr = np.array(df['val'])

    size = arr.shape[0]
    arr = np.reshape(arr, (int(size/3),3))
    print(arr)

    # need to grab data from PDS for plotting 
    # email liang 

first_plot()