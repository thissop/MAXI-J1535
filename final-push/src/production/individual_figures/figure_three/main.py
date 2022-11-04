def make_grs_hids(data_file='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv', cols:list=['A', 'F']):
    r'''
    
    Notes
    -----
    - Hardness is calculated as [3-10]/[10-50]
    
    '''
    import numpy as np
    import matplotlib.pyplot as plt 
    import pandas as pd
    import seaborn as sns
    from matplotlib.colors import LinearSegmentedColormap
    wh1 = True

    plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')

    sns.set_context('paper', font_scale=0.7)

    df = pd.read_csv(data_file)

    df = df.merge(pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'), on='observation_ID')

    #sns.set_style('darkgrid')
    #sns.set_style('ticks')
    
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
    #plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/production/pipeline/qpoml_style.mplstyle')
    #plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/production/pipeline/exo.mplstyle')
    #sns.set_context("paper", font_scale=0.6) #font_scale=

    #plt.rcParams['font.family'] = 'serif'
    #plt.rcParams["mathtext.fontset"] = "dejavuserif"

    #fig, ax = plt.subplots(figsize=())

    plt.scatter(df['B'], df['A'], c=df['frequency'], lw=0.3, edgecolors='black', cmap='viridis', s=3)

    plt.gca().set(xlabel='Hardness Ratio', ylabel='Net Count Rate (c/s)', yscale='log') # 

    plt.colorbar(orientation='vertical', shrink=0.8, label='QPO Centroid Frequency (Hz)')

    plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_3/[GRS][hardness vs net count rate].png', dpi=250)
    plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_3/[GRS][hardness vs net count rate].pdf')
    plt.clf()
    plt.close()

    #sns.set_style('darkgrid')
    #sns.set_style('ticks')
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
    #plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/production/pipeline/qpoml_style.mplstyle')
    #plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/production/pipeline/exo.mplstyle')
    #sns.set_context("paper", font_scale=0.6) #font_scale=

    #plt.rcParams['font.family'] = 'serif'
    #plt.rcParams["mathtext.fontset"] = "dejavuserif"

    plt.scatter(df['B'], df['frequency'], c=np.log10(df['A']), lw=0.3, edgecolors='black', cmap='viridis', s=3)

    plt.gca().set(xlabel='Hardness Ratio', ylabel='QPO Centroid Frequency (Hz)') # 

    plt.colorbar(orientation='vertical', shrink=0.8, label='log(Net Count Rate)')

    plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_3/[GRS][hardness vs frequency].png', dpi=250)
    plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_3/[GRS][hardness vs frequency].pdf')

    plt.clf()
    plt.close()

    '''
    # test for maxi 

    df = pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv').merge(pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_dates.csv'), on='observation_ID')

    fig, ax = plt.subplots()

    ax.scatter(df['B'], df['F'])
    ax.set(xscale='log')

    plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/manuscript/figures/individual/figure_3/maxi_temp.png', dpi=200)
    '''

make_grs_hids()