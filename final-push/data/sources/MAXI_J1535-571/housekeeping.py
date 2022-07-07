def make_maxi_light(old_master = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus",
                    new_spectral_root='./final-push/data/sources/MAXI_J1535-571/spectral/jspipe_spectra/', 
                    new_qpo_root='./final-push/data/sources/MAXI_J1535-571/qpo/jspipe_qpo/'):
    r'''
    this isn't relevantt anyomore because it's already been run :)
    '''
    
    import os 
    import shutil 
    from tqdm import tqdm 

    obsids = [i for i in os.listdir(old_master) if '.' not in i]
    unique_count = 0
    for obsid in tqdm(obsids):
        for gti in [str(i) for i in range(40)]:
            # needed for jspipe pds 

            pds = 'js_ni'+obsid+'_0mpu7_silver_GTI'+gti+'-bin.pds'
            old_pds_path = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus\+++\jspipe\js_ni+++_0mpu7_silver_GTI***-bin.pds".replace('+++',obsid).replace('***',gti)
            
            if os.path.exists(old_pds_path): 
                unique_count+=1

                new_pds_path = new_qpo_root+obsid+'/'
                if not os.path.exists(new_pds_path):
                    os.mkdir(new_pds_path)
                new_pds_path = new_qpo_root+pds

                fak = pds.replace('-bin.pds', '-fak.rsp')
                old_fak_path = old_pds_path.replace('-bin.pds', '-fak.rsp')
                new_fak_path = new_qpo_root+fak

                # needed for jspipe spectral --> arf and rmf are in fits keys 
                spectrum = 'js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
                old_spectrum_path = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus\+++\jspipe\js_ni+++_0mpu7_silver_GTI***.jsgrp".replace('+++',obsid).replace('***',gti)
                new_spectrum_path = new_spectral_root+obsid+'/'
                if not os.path.exists(new_spectrum_path):
                    os.mkdir(new_spectrum_path)
                new_spectrum_path+=spectrum

                background = spectrum.replace('.jsgrp','.bg') 
                old_background_path = old_spectrum_path.replace('.jsgrp','.bg')
                new_background_path = new_spectral_root+background
                
                # COPY THEM ALL # 
                shutil.copyfile(old_pds_path, new_pds_path)
                shutil.copyfile(old_fak_path, new_fak_path)

                shutil.copyfile(old_spectrum_path, new_spectrum_path)
                shutil.copyfile(old_background_path, new_background_path)

    print('total obs:', unique_count) # 638

def check_internal_paths(): 
    from astropy.io import fits

    hdul = fits.open('')