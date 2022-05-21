def check_objects(top_dir:str=''): 
    import os 
    from astropy.io import fits
    from tqdm import tqdm 

    if top_dir[-1]!='/': 
        top_dir+='/'

    objects = []
    for dir in tqdm(os.listdir(top_dir)): 
        if dir!='.gitkeep': 
            data_dir = top_dir+dir+'/'
            for file in os.listdir(data_dir):
                if 's0' in file: 
                    hdul = fits.open(data_dir+file)
                    hdul_keys = list(hdul[0].header)
                    if 'OBJECT' in hdul_keys: 
                        objects.append(str(hdul[0].header['OBJECT'])) 
                    else: 
                        print("NO OBJECT!", file)

    print(list(set(objects))) 
    '''
    'MAXI_J1543-564', 'ASM_J1748-2848', 'XTE_J1650-500', 'MAXI_J1659-152', 
    'XTE_J1817-330', '4U_1630-47', 'GRO_J1655-40', 'H1743-322', 
    'XTE_J1829-098', 'XTE_J1746-319', 'XTE_J1859+226', 'GX_339-4', 
    'H_1743-322', 'XTE_J1748-2848', '4U1543-47', 'XTE_J1550-564', 
    'GX339-4', 'SWIFT_J1753.5-0127', 'XTE_J1752-223'
    '''

check_objects('./code/misc/meta_preparation/rxte_motta/downloader/downloads')