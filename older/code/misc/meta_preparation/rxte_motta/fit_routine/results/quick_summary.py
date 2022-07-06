def kte_plot(output:str=r'C:\Users\Research\Documents\GitHub\MAXI-J1535\code\misc\meta_preparation\rxte_motta\fit_routine\results\output.csv'): 
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    data = pd.read_csv(output)
    kT_e = np.array(data['kT_e'])
    kT_e = kT_e[np.logical_and(kT_e<900, kT_e>10.0)]

    print(np.sort(list(set(kT_e))))

    plt.hist(kT_e)
    
    plt.gca().set(xlabel='kT_e', ylabel='count')

    #plt.show()
    plt.savefig('kte_dist.png', dpi=150)

kte_plot()