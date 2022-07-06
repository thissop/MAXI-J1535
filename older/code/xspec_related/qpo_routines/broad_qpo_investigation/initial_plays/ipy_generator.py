def print_setup(full_id:str='1050360113_1'):
    id_list = full_id.split('_')
    obs_id = id_list[0]
    gti = id_list[1]

    pds_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-bin.pds'
    fak_temp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI***-fak.rsp'
    
    pds_file = pds_temp.replace('+++', obs_id).replace('***', gti)
    fak_file = fak_temp.replace('+++', obs_id).replace('***', gti)

    print('data '+pds_file)
    print('none')
    print('response '+fak_file)
    print('query yes')
    print('ignore **-0.02 100.-**')
    print('model loren')
    print('0')
    print('')
    print('')
    print('freeze 1')
    print('fit')

    print('editmod loren+loren')
    print('0')
    print('')
    print('')
    print('freeze 1')
    print('fit')

    for i in ['2', '3', '5', '6']:
        print('freeze '+i)

print_setup()