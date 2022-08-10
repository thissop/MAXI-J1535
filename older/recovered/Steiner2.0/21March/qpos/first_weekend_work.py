def retrieve_qpo_data(ID,pds_path,rsp_path,x_min,x_max,plot):
    #Import(s)
    import numpy as np
    from astropy.io import fits
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os

    #Action

    obs_id = ID.split('_')[0]
    gti = ID.split('_')[1]

    pds_file = pds_path.replace('+++',obs_id)
    pds_file = pds_file.replace('+',gti)

    rsp_file = rsp_path.replace('+++',obs_id)
    rsp_file = rsp_file.replace('+',gti)

    if os.path.exists(rsp_file)==True and os.path.exists(pds_file)==True:

        powers = []
        errors = []

        with fits.open(pds_file) as hdul: 
            data = hdul[1].data
            data_length = len(data)
            for i in range(data_length):
                powers.append(float(data[i][1]))
                errors.append(float(data[i][2]))
        
        frequencies = []

        with fits.open(rsp_file) as hdul: 
            data = hdul[1].data
            data_length = len(data)
            for i in range(data_length):
                lower_bound = float(data[i][1])
                upper_bound = float(data[i][2])
                freqency = (lower_bound+upper_bound)/2 
                frequencies.append(freqency)

        powers, frequencies, errors = np.array(powers), np.array(frequencies), np.array(errors)

        if x_min != '' and x_max != '': 
            mask = np.logical_and(frequencies>x_min, frequencies<x_max)
            powers, frequencies, errors = powers[mask], frequencies[mask], errors[mask]

        #Plot
        if plot != 'None': 
            sns.set_style('darkgrid')
            plt.rcParams['font.family'] = 'serif'
            plt.errorbar(frequencies,powers,yerr=errors,lw=0,elinewidth=0.5,color='cornflowerblue')
            plt.scatter(frequencies,powers,marker='o',color='cornflowerblue',s=2)
            plt.xlim(x_min,x_max)
            plt.xlabel('Frequency [Hz]')
            plt.ylabel('f '+r'$\cdot$'+' rms-Normalized Power')
            plt.xscale('log')
            plt.yscale('log')
            #plt.vlines(x=[1.25,7.276],ymin=min(powers),ymax=max(powers),colors=['indianred'],label='Centers: 1.25 & 7.28 Hz',ls='--')
            #plt.legend(loc='lower left',fontsize='x-small')
            if plot =='Show': 
                plt.show()
                plt.clf()
            else:
                plot_path = plot.replace('+++',obs_id)
                plot_path = plot_path.replace('+',gti)
                plt.savefig(plot_path)
                plt.clf()
        
        #Return data
        return frequencies, powers, errors

def simulate_loren(x_range,num_obs,amp,wid,offset,noise_scale):
    '''
    x_range: range of simulated x values 
    num_obs: number of simulated values to create
    amp: simulated lorentzian amplitude
    wid: simulated lorentzian width 
    offset: horiztonal offset from 0 of returned distribution, +/-
    noise_scale: standard deviation of the gaussian noise added to the simulated y values
    '''

    # Import(s)
    import numpy as np

    # Action
    delta = x_range/2

    x_vals = np.linspace((0-delta),(0+delta),num_obs)

    # Fit
    def loren(x,amp,cen,wid):
        return (amp+wid**2/((x-cen)**2+wid**2))

    y_vals = loren(x_vals,amp=amp,cen=0,wid=wid)

    y_vals = y_vals + np.random.normal(0,noise_scale,len(y_vals))

    x_vals = x_vals+offset

    return x_vals, y_vals
    
def fit_lorentzian(x,y): 
    # Import(s)
    from scipy.optimize import curve_fit 

    # Action

    def loren(x,amp,cen,wid,height):
        return (amp+wid**2/((x-cen)**2+wid**2))+height
    
    pars, cov = curve_fit(f=loren,xdata=x,ydata=y)

    a = pars[0]
    b = pars[1]
    c = pars[2]
    h = pars[3]

    y_prime = loren(x,a,b,c,h)

    residuals = y-y_prime

    return x, y, y_prime, residuals, a, b, c

def plot_single_peak_fit(x,y,yerr,y_prime,residuals,amp,cen,wid,title):
    # Import(s)
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Plot

    sns.set_style('darkgrid')
    plt.rcParams['font.family'] = 'serif'
    fig, axs = plt.subplots(2,1,gridspec_kw={'height_ratios':[4,1]})

    axs[0].errorbar(x,y,yerr=yerr,lw=0,elinewidth=0.5)
    axs[0].scatter(x,y,marker='o',s=2)
    #axs[0].axvline(x=cent,color='red',linestyle='--')
    loren_desc = 'Amp: ' + str(round(amp,3)) + '\nCenter: ' + str(round(cen,3))+ '\nWidth: ' +str(round(wid,3))
    axs[0].plot(x,y_prime,label=loren_desc,color='orange')
    axs[0].set_title(title)
    axs[0].set_ylabel('"f '+r'$\cdot$'+' rms-Normalized Power"')
    axs[0].legend(loc='upper right',fontsize=6)


    axs[1].scatter(x,residuals)
    axs[1].hlines(0,xmin=min(x),xmax=max(x),linestyles='dashed')
    axs[1].set_xlabel('Frequency')
    axs[1].set_ylabel('Residuals')
    axs[1].set_ylim(bottom=(1.3*min(residuals)),top=1.3*max(residuals))

    plt.show()

def fit_two_lorentzians(x,y):
    # Import(s)
    from scipy.optimize import curve_fit 
    import numpy as np
    from scipy.signal import find_peaks

    # Action

    peaks,_ = find_peaks(y)
    
    top_90_indices = np.where(y>np.percentile(y,95))
    cent = np.median(x[top_90_indices])

def locate_centers(x,y,yerr,x_min,x_max,plot,obs_id,gti):
    # Import(s)
    import numpy as np 
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks

    # Action

    req_height_1 = np.mean(y)+2*np.std(y)
    peak_indices, _ = find_peaks(y,height=req_height_1,distance=20)
    
    initial_peak_centers = x[peak_indices]

    better_peak_cents = [] # for better peak center values

    for peak_index in peak_indices: # Func that get's better peak center values
        min_index = peak_index - 10
        max_index = peak_index + 10
        
        indice_range = np.array(range(min_index,max_index+1))
        
        within_range = y[indice_range]

        near_peak_vals = within_range[np.where(within_range>req_height_1)]
        
        near_peak_x_vals = []

        for npv in near_peak_vals:
            near_peak_x_vals.append(x[np.where(y==npv)])
    
        median_val = np.median(near_peak_x_vals)
        better_peak_cents.append(median_val)

    # Plot
    if plot != 'None': 
        plt.rcParams['font.family'] = 'serif'
        plt.errorbar(x,y,yerr=yerr,lw=0,elinewidth=0.5,color='cornflowerblue')
        plt.axhline(y=req_height_1)
        for i in initial_peak_centers:
            plt.axvline(x=i)
        for i in better_peak_cents:
            plt.axvline(x=i,color='red')
        plt.scatter(x,y,marker='o',color='cornflowerblue',s=2)
        plt.xlim(x_min,x_max)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('f '+r'$\cdot$'+' rms-Normalized Power')
        plt.xscale('log')
        plt.yscale('log')
        if plot =='Show': 
            plt.show()
            plt.clf()
        else:
            plot_path = plot.replace('+++',obs_id)
            plot_path = plot_path.replace('+',gti)
            plt.savefig(plot_path)
            plt.clf()


#### TESTS ####

def test_one():
    # Import(s)

    # Action

    pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds'
    rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
    qpo_data = retrieve_qpo_data(ID='1130360110_0',pds_path=pds_temp,rsp_path=rsp_temp,x_min=6*10**-2,x_max=40,plot='None')

    freqs = qpo_data[0]
    powers = qpo_data[1]
    y_errs = qpo_data[2]


    locate_centers(freqs,powers,y_errs,6*10**-2,40,'Show','','') 

    #fitted = fit_lorentzian(freqs,powers)

    #plot_single_peak_fit(fitted[0],fitted[1],y_errs,fitted[2],fitted[3],fitted[4],fitted[5],fitted[6],title='Portion of left peak')

def create_qpo_plots():
    # Import(s)
    import pandas as pd
    from progress.bar import Bar

    # Action 
    df = pd.read_csv('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/all_seg_ids.csv')
    ids = list(df['ID'])
    pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds'
    rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
    plot_temp = '/home/thaddaeus/FMU/Steiner2.0/21Apr/all_pds_plots/+++.png'
    bar = Bar('Processing...',max=len(ids))
    for id in ids: 
        plot_path = plot_temp.replace('+++',id)
        retrieve_qpo_data(ID=id,pds_path=pds_temp,rsp_path=rsp_temp,x_min=0.06,x_max=40,plot=plot_path)
        bar.next()
    bar.finish()

create_qpo_plots()