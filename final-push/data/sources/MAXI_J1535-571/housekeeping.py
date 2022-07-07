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
                new_pds_path = new_pds_path+pds

                fak = pds.replace('-bin.pds', '-fak.rsp')
                old_fak_path = old_pds_path.replace('-bin.pds', '-fak.rsp')
                new_fak_path = new_qpo_root+obsid+'/'+fak

                # needed for jspipe spectral --> arf and rmf are in fits keys 
                spectrum = 'js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
                old_spectrum_path = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus\+++\jspipe\js_ni+++_0mpu7_silver_GTI***.jsgrp".replace('+++',obsid).replace('***',gti)
                new_spectrum_path = new_spectral_root+obsid+'/'
                if not os.path.exists(new_spectrum_path):
                    os.mkdir(new_spectrum_path)
                new_spectrum_path+=spectrum
                background = spectrum.replace('.jsgrp','.bg') 
                old_background_path = old_spectrum_path.replace('.jsgrp','.bg')
                new_background_path = new_spectral_root+obsid+'/'+background
                
                # COPY THEM ALL # 
                shutil.copyfile(old_pds_path, new_pds_path)
                shutil.copyfile(old_fak_path, new_fak_path)

                shutil.copyfile(old_spectrum_path, new_spectrum_path)
                shutil.copyfile(old_background_path, new_background_path)

    print('total obs:', unique_count) # 638

#make_maxi_light()

def delete_accidental_extras(old_master = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus",
                             new_qpo_root='./final-push/data/sources/MAXI_J1535-571/qpo/jspipe_qpo/'):
    r'''
    this isn't relevant anyomore because it was for one time use to fix one of my mistakes :)
    '''
    
    import os 
    import shutil 
    from tqdm import tqdm 

    obsids = [i for i in os.listdir(old_master) if '.' not in i]

    for obsid in tqdm(obsids):
        for gti in [str(i) for i in range(40)]:
            # needed for jspipe pds 

            old_pds_path = r"C:\Users\Research\Documents\GitHub_LFS\Steiner\thaddaeus\+++\jspipe\js_ni+++_0mpu7_silver_GTI***-bin.pds".replace('+++',obsid).replace('***',gti)
            
            spectrum = 'js_ni' + obsid + '_0mpu7_silver_GTI' + gti + '.jsgrp'
            new_pds_path = new_qpo_root+obsid+'/'
            if os.path.exists(new_pds_path+spectrum):
                os.remove(new_pds_path+spectrum)

def check_internal_paths(): 
    from astropy.io import fits

    fp_list =['/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/10258-01-02-00/src_pcu2.pha',
              '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/92702-01-31-00/bkg_pcu2.pha', 
              '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/92702-01-31-00/p2_xe_2008-05-03.rsp']
    for fp in fp_list: 
        print('\n###'+fp.split('/')[-1]+'###\n')

        hdul = fits.open(fp)
        for key in hdul[0].header: 
            print(key, hdul[0].header[key])
        print('###')
        for key in hdul[1].header: 
            print(key, hdul[1].header[key])
        print('###')

check_internal_paths()

def fix_internal_paths(): 
    r'''
    fixed internal paths for MAXI and GRS_1915+105

    MAXI notes
    ----------

    jsgrp spectrum: hdul[1].header
    * fix: ['BACKFILE','RESPFILE','ANCRFILE']

    bg spectrum: 
    * fix: None


    bin.pds: hdul[1].header
    * fix: ['RESPFILE'] 
    
    fak.rsp: 
    * fix: None

    GRS 1915 notes
    --------------



    

    '''
    pass 