import os
import numpy as np
import pandas as pd

def first_test(): 
    final_ids = []
    delete_ids = []

    counter = 0
    current_ids = list(pd.read_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/all_seg_ids.csv')['ID'])

    for id in current_ids: 
        obs_id = id.split('_')[0]
        seg_id = id.split('_')[1]

        test_file = '/home/thaddaeus/FMU/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
        test_file = test_file.replace('+++', obs_id)
        test_file = test_file.replace('***', seg_id)

        if (os.path.exists(test_file)==False): 
            delete_ids.append(id)
        
        else: 
            final_ids.append(id)

    # print(len(final_ids)) --> answer is 638

    spectral_base = '/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/dec-28-21/logs'
    for file in os.listdir(spectral_base):
        delete = False
        for id in delete_ids: 
            if id in file: 
                delete = True
                break
        
        if delete == True: 
            os.remove(spectral_base+'/'+file)

    final_sample = pd.DataFrame(final_ids, columns=['ID'])
    final_sample.to_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/all_seg_ids.csv', index=False)

def second_test(): 
    ids = []
    

    base_dir = '/home/thaddaeus/FMU/Steiner/thaddaeus'
    for file in os.listdir(base_dir): 
        if '.' not in file:
            for counter in range(100): 
                test_file = '/home/thaddaeus/FMU/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
                test_file = test_file.replace('+++', file)
                test_file = test_file.replace('***', str(counter))
                if os.path.exists(test_file): 
                    ids.append(file+'_'+str(counter))

    # print(len(ids)) --> prints to 638
    final_sample = pd.DataFrame(ids, columns=['ID'])
    final_sample.to_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/all_seg_ids.csv', index=False)

    print(len(ids))

def third_test(): 
    completed_ids = list(pd.read_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/qpo_routines/jan-1-2022/completed_ids.csv')['ID'])

    all_current_ids = np.array(pd.read_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/all_seg_ids.csv')['ID'])

    for id in completed_ids: 
        if id not in all_current_ids: 
            print(id)

third_test()