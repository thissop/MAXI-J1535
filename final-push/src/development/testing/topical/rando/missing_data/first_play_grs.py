import os 

def first_test():
    energy_dir = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra'
    timing_dir = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS'

    energy_files = [i for i in os.listdir(energy_dir) if i!='.gitkeep']
    timing_files = [i for i in os.listdir(timing_dir) if i!='.gitkeep']

    print('length energy: ', len(energy_files))
    print('length timing: ', len(timing_files))

    '''
    
    length energy:  554
    length timing:  625
    
    '''

first_test()