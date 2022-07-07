def reformat_spectral_directory(root:str='./final-push/data/sources/GRS_1915+105/spectral/external_spectra/'): 
    r'''
    
    this function is irrelevant now because it's been executed
    
    '''
    import os 
    import shutil
    from tqdm import tqdm 

    if root[-1]!='/':
        root+='/'
    
    obsids = [i for i in os.listdir(root) if i != 'Users'] 
    for obsid in tqdm(obsids): 
        sub_dir = root+'Users/users/mariano/liang/GRS1915_C/'+obsid+'/' 
        for f in os.listdir(sub_dir): 
            shutil.copyfile(sub_dir+f, root+obsid+'/'+f)

def first_look_at_qpos(): 
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    df = pd.read_csv('final-push/data/sources/GRS_1915+105/qpo/qpo_summary.txt')
    
    obsids = ['-'.join(i.split('-')[:-1]) for i in df['OBSID']]

    print(len(list(set(obsids)))) # 348 from 620 
    
    f = [3.479,2.777]
    w = [0.363,0.371]
    a = [10.202,11.799]

    def loren(E, EL, σ, K):
        return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

    x = np.linspace(0,8,500)
    y = np.zeros(len(x))
    fig, ax = plt.subplots(figsize=(4,2))
    for i in range(2): 
        y = loren(x, f[i], w[i], a[i])
        ax.scatter(x, y, label='amp='+str(a[i])+'\nfreq='+str(round(f[i],2)), 
                   s=2, color='cornflowerblue')
    
    ax.legend(fontsize='small')
    ax.set(xlabel='x', ylabel='y')
    plt.tight_layout()
    plt.savefig('final-push/data/sources/GRS_1915+105/miscellaneous/first_qpo.png', dpi=150)

#first_look_at_qpos()

def prepare_spectral_for_qpoml(old_context:str='final-push/data/sources/GRS_1915+105/spectral/spectral_summary.txt',
                               new_context:str='final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt',
                               old_qpo:str='final-push/data/sources/GRS_1915+105/qpo/qpo_summary.txt',
                               new_qpo:str='final-push/data/sources/GRS_1915+105/qpo/qpo_summary_for_qpoml.txt'):
    import pandas as pd
    import numpy as np

    qpo = pd.read_csv(old_qpo)
    qpo = qpo.drop(columns=['date','frequency_err','width_err','rms_err'])
    
    for i in list(qpo):
        x = np.array(qpo[i])
        print(min(x),max(x))

        r'''
        0.466 6.229
        0.034 1.12
        3.637 16.218
        '''

    ids = pd.DataFrame(pd.read_csv(old_context)['observation_ID'])

    merged = ids.merge(qpo, on='observation_ID')
    merged.to_csv(new_qpo, index=False)

    new_context_df = pd.read_csv(old_context).drop(columns=['red_stat'])
    new_context_df.to_csv(new_context, index=False)

prepare_spectral_for_qpoml()