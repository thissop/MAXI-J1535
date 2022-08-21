import xspec 
from xspec import *
import numpy as np
import pandas as pd

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

#prepare_spectral_for_qpoml()

def add_dates(summary_file:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt',
              data_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra'): 

    import pandas as pd
    from astropy.io import fits 
    from tqdm import tqdm 
    import os 
    from astropy.time import Time

    if data_dir[-1]!='/':
        data_dir+='/'

    df = pd.read_csv(summary_file)
    obsids = list(df['observation_ID'])
    
    mjds = [] 
    for obsid in tqdm(obsids): 
        temp_dir = f'{data_dir}{obsid}' 
        if os.path.exists(temp_dir):
            os.chdir(temp_dir)
            hdul = fits.open('src_pcu2.pha')
            date_obs = hdul[1].header['DATE-OBS'].split('/')
            time_obs = hdul[1].header['TIME-OBS']
            
            print(date_obs)
            
            if len(date_obs)==1:
                date = date_obs[0]
            else: 
                year = int(date_obs[2])
                if year>22: 
                    year = '19'+str(year)
                else: 
                    year = '20'+str(year)

                date = year+'-'+date_obs[1]+'-'+date_obs[0]+'T'+time_obs
            mjd = Time(date, format='isot').mjd
            mjds.append(mjd) # TSTOP

    df['MJD'] = mjds
    df.to_csv(summary_file, index=False)

#add_dates()

def first_stacked_plot(summary_file:str, x:str='TSTART', y:str='net_count_rate', save_path:str=None):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt 
    import seaborn as sns

    #sns.set_context('paper')

    plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')

    df = pd.read_csv(summary_file)

    fig, ax = plt.subplots(figsize=(4, 1.5))
    ax.scatter(df[x], df[y]/np.median(df[y]), s=2)
    ax.set(xlabel=x, ylabel=y)
    plt.tight_layout()
    if save_path is not None: 
        plt.savefig(save_path, dpi=200)

summary_file='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt'
save_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/miscellaneous/temp.png'
#first_stacked_plot(x='MJD', y='net_count_rate', summary_file=summary_file, save_path=save_path)

def prep_context(context_file:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS_1915+105_context.txt', 
                 spectral_file:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS_1915+105_qpo_for_qpoml.txt'):
    
    import pandas as pd 
    df = pd.read_csv(spectral_file)
    obsid, times = (list(df[i]) for i in ['observation_ID', 'MJD'])
    df = df.drop(columns=['MJD'])
    df.to_csv(spectral_file, index=False)
    context_df = pd.DataFrame(list(zip(obsid, times)), columns=['observation_ID', 'MJD'])
    context_df.to_csv(context_file, index=False)

#prep_context()

def fix_response_paths():

    r'''
    
    notes
    -----

    this function is not relevant any more since it's been run and the header response file terms have been fixed.
    
    '''


    import os
    from astropy.io import fits 
    from tqdm import tqdm 

    root = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/'

    for sub_dir in tqdm(os.listdir(root)):
        if sub_dir!='.gitkeep':
            sub_dir = root+sub_dir
            os.chdir(sub_dir)

            hdul = fits.open('power_0_249.pha')            
            fits.setval('power_0_249.pha', 'RESPFILE', value='power_0_249.rmf', ext=1)
            
#fix_response_paths()

def pds_data_to_csv(root:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS', 
                    plot_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/pds_plots', 
                    pds_csv_dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/pds_csv'):
    import matplotlib.pyplot as plt 
    import os 
    from tqdm import tqdm 

    if root[-1]!='/':
        root+='/'

    if plot_dir[-1]!='/':
        plot_dir+='/'

    if pds_csv_dir[-1]!='/':
        pds_csv_dir+='/'

    for obsid in tqdm(os.listdir(root)):
        if obsid!='.gitkeep':
            os.chdir(f'{root}{obsid}')

            Xset.chatter = 0

            s = Spectrum("power_0_249.pha")

            #Plot.device = "/xs"
            Plot.xAxis = "kev"

            Plot("data")

            x = np.array(Plot.x())
            y = np.array(Plot.y())
            #y /= np.median(y)

            mask = np.logical_and(x>0.25, x<10)
            x, y = (i[mask] for i in [x,y])

            xerr = np.array(Plot.xErr())
            yerr = np.array(Plot.yErr())

            fig, ax = plt.subplots()

            ax.scatter(x, y)
            ax.set(xlabel='Frequency [Hz]', ylabel='Power')
            plt.savefig(f'{plot_dir}{obsid}.png', dpi=200)

            s = None 
            xspec.Plot.commands = ()
            xspec.AllData.clear()
            plt.clf()
            plt.close()
            
            df = pd.DataFrame(list(zip(x,y,xerr,yerr)), columns=['x','y','xerr','yerr'])
            df.to_csv(f'{pds_csv_dir}{obsid}.csv', index=False)

#pds_data_to_csv()

def prep_csv_pds_for_ml(pds_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/pds_csv'):
    import os 
    from tqdm import tqdm 

    if pds_directory[-1]!='/':
        pds_directory+='/'

    powers = []
    obsids = []

    for pds in tqdm(os.listdir(pds_directory)):
        df = pd.read_csv(f'{pds_directory}{pds}')
        powers.append(list(df['y']))
        obsids.append(pds.split('.')[0])

    df = pd.DataFrame(np.transpose(powers), columns=obsids)
    df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/qpo_pds_for_ml.csv', index=False)

prep_csv_pds_for_ml()