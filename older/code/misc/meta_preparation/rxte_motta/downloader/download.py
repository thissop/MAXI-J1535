def download_products(obsid:str, download_dir:str, products: str='pca'):
    import pandas as pd 
    from astropy.io import fits
    from astropy.table import Table 
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import gzip
    import shutil
    import os

    if download_dir[-1]!='/':
        download_dir+='/'

    download_dir+=obsid+'/'

    pr_df = pd.read_csv('./code/misc/meta_preparation/rxte_motta/downloader/bounds.txt')
    prop_bounds = list(pr_df['proposal_bounds'])
    prop_bounds = [[int(j) for j in i.split(',')] for i in prop_bounds]

    pr = obsid.split('-')[0]
    pr_int = int(pr)
    ao_index = -1
    for i, range in enumerate(prop_bounds): 
        if range[0]<=pr_int<=range[1]: 
            ao_index = i
            break 

    if ao_index!=-1: 
        ao = pr_df['AO'][ao_index]
        if products=='pca':
            url = 'https://heasarc.gsfc.nasa.gov/FTP/xte/data/archive/'
            url += ao+'/P'+str(pr)+'//'+obsid+'/stdprod/'

            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            title = str(soup.find_all('title')[0])

            if 'Status Code 404' in title: 
                print('error url doesn\'t exist')

            elif 'Index of /FTP' in title: 
                raw_links = [str(i) for i in soup.find_all('a')]
                links = []
                for i in raw_links: 
                    if '.gz' in i: 
                        links.append(i.split('>')[1].split('<')[0])

                if not os.path.exists(download_dir): 
                    os.mkdir(download_dir)

                for i in links: 
                    if '.gz' in i: 
                        split = i.split('.')
                        if len(split)>1: 
                            second_ending = i.split('.')[-2]
                            if second_ending == 'pha' or second_ending == 'rsp':  
                                response = requests.get(url+i, stream=True)
                                if response.status_code == 200:
                                    download_path = download_dir+i
                                    with open(download_path, 'wb') as f:
                                        f.write(response.raw.read())

                                    with gzip.open(download_path, 'rb') as f_in:
                                        with open(download_path.replace('.gz',''), 'wb') as f_out:
                                            shutil.copyfileobj(f_in, f_out)
                                    
                                    os.remove(download_path)

from tqdm import tqdm
import pandas as pd

obsids = pd.read_csv('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/data/processed/2022/meta_qpo/motta_cleaned.csv')['ID']

for obsid in tqdm(obsids):
    try: 
        download_products(obsid, './code/misc/meta_preparation/rxte_motta/downloader/downloads')
    
    except Exception as e: 
        print(e)
        pass
