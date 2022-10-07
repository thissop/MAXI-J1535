def make_grs_hids(data_file='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv', cols:list=['A', 'F']):
    r'''
    
    Notes
    -----
    - Hardness is calculated as [3-10]/[10-50]
    
    '''

    import matplotlib.pyplot as plt 
    import pandas as pd
    import seaborn as sns
    from matplotlib.colors import LinearSegmentedColormap
    plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

    sns.set_context('paper', font_scale=0.7)

    df = pd.read_csv(data_file)

    df = df.merge(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'), on='observation_ID')

    #sns.set_style('darkgrid')
    #sns.set_style('ticks')
    
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
    #plt.style.use('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/pipeline/qpoml_style.mplstyle')
    #plt.style.use('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/pipeline/exo.mplstyle')
    #sns.set_context("paper", font_scale=0.6) #font_scale=

    #plt.rcParams['font.family'] = 'serif'
    #plt.rcParams["mathtext.fontset"] = "dejavuserif"

    #fig, ax = plt.subplots(figsize=())

    plt.scatter(df['B'], df['A'], c=df['frequency'], lw=0.3, edgecolors='black', cmap='viridis', s=3)

    plt.gca().set(xlabel='Hardness Ratio', ylabel='Net Count Rate') # 

    plt.colorbar(orientation='vertical', shrink=0.8, label='QPO Centroid Frequency')

    plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_3/GRS_count_rate_vs_hardness.png', dpi=250)
    plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_3/GRS_count_rate_vs_hardness.pdf')
    plt.clf()
    plt.close()

    #sns.set_style('darkgrid')
    #sns.set_style('ticks')
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
    #plt.style.use('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/pipeline/qpoml_style.mplstyle')
    #plt.style.use('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/pipeline/exo.mplstyle')
    #sns.set_context("paper", font_scale=0.6) #font_scale=

    #plt.rcParams['font.family'] = 'serif'
    #plt.rcParams["mathtext.fontset"] = "dejavuserif"

    plt.scatter(df['B'], df['frequency'], c=df['A'], lw=0.3, edgecolors='black', cmap='viridis', s=3)

    plt.gca().set(xlabel='Hardness Ratio', ylabel='QPO Centroid Frequency') # 

    plt.colorbar(orientation='vertical', shrink=0.8, label='Net Count Rate')

    plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_3/GRS_freq_vs_hardness.png', dpi=250)
    plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_3/GRS_freq_vs_hardness.pdf')

    plt.clf()
    plt.close()

    '''
    # test for maxi 

    df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv').merge(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_dates.csv'), on='observation_ID')

    fig, ax = plt.subplots()

    ax.scatter(df['B'], df['F'])
    ax.set(xscale='log')

    plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/individual/figure_3/maxi_temp.png', dpi=200)
    '''

make_grs_hids()