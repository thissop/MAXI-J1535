import pandas as pd 
import os 

from tqdm import tqdm 

def initial_finalization_lol(): 

    df =  pd.read_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv')

    new_df = pd.DataFrame()

    '''
    GRS
    net_count_rate: A
    gamma: B
    kTe: C
    nthcomp_norm: D
    diskbb_tin: E 
    diskbb_norm: F
    hardness: G

    MAXI

    A:simpl_FracScat
    B:net_source_count_rate
    C:tin_before_error
    D:diskbb_norm_before_error
    E:gamma_before_error
    F:nthcomp_norm_before_error
    G:hardness_ratio 

    SHARED 

    A: net_count_rate
    B: hardness 
    C: gamma
    D: nthcomp_norm 
    E: diskbb_tin
    F: diskbb_norm

    '''

    out_cols = ['observation_ID', 'A', 'B', 'C', 'D', 'E', 'F']

    # SORT TO SAME OUTPUT LETTER COLUMNS FOR EASE OF EXPLANATION

    keep = ['observation_ID', 'A', 'G', 'B', 'D', 'E', 'F']

    for i, j in zip(keep, out_cols):
        new_df[j] = df[i]
    ## GRS ## 
    new_df.to_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv', index=False)
    ## maxi 
    df =  pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv')

    new_df = pd.DataFrame()

    keep = ['observation_ID', 'B', 'G', 'E', 'F', 'C', 'D']

    for i, j in zip(keep, out_cols):
        new_df[j] = df[i]

    new_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv', index=False)

def make_hardness_files(): 
    grs_df =  pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv')
    maxi_df = pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv')
    commands_file = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/development/testing/topical/fixing_hardness/xspec_commands.sh'

    commands = ['heainit', 'xspec']
    
    # Handle GRS FIRST 

    for observation_ID in tqdm(list(grs_df['observation_ID'])):
        
        commands.append(f'cd /ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra{observation_ID}')
        commands.append('data src_pcu2.pha')
        commands.append('ignore **-2.0 7.0-**')
        commands.append('log soft.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('notice **-**')
        commands.append('ignore **-13.0 60.0-**')
        commands.append('log hard.txt')
        commands.append('show data')
        commands.append('log none')
        commands.append('data none')

    with open(commands_file, 'w') as f1: 
        for line in commands: 
            f1.write(line+'\n')

    commands.append('cd ')

    for observation_ID in list(maxi_df['observation_ID']):

    
    with open(commands_file, 'a') as f1: 
        for line in commands: 
            f1.write(line+'\n')

        #os.chdir(f'/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra{observation_ID}')


