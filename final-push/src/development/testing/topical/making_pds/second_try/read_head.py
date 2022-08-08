import pandas as pd 
from astropy.io import fits 

file_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/data/temp/FS4f_186d5c45-186d62d2.fits'
hdul = fits.open(file_path)

for i in range(4):
    keys = list(hdul[i].header)
    values = [hdul[i].header[j] for j in keys]
    df = pd.DataFrame(list(zip(keys, values)), columns=['key', 'value'])
    df.to_csv(f'/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/development/testing/topical/making_pds/second_try/example_headers/example_{i}.csv', index=False)

