import pandas as pd
import numpy as np
from astropy.io import fits

ids = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_QPO-Input.csv')['observation_ID'])

for observation_ID in ids: 
    obsid_list = observation_ID.split('_')
    obsid = obsid_list[0]
    gti = obsid_list[1]
    hdul = fits.open(f'{}')

    