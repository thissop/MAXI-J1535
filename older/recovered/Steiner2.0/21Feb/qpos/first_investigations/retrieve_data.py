def retrieve_qpo_data(ID,pds_path,rsp_path,plot):
    #Import(s)
    import numpy as np
    from astropy.io import fits
    import matplotlib.pyplot as plt

    #Action

    obs_id = ID.split('_')[0]
    gti = ID.split('_')[1]

    pds_file = pds_path.replace('+++',obs_id)
    pds_file = pds_file.replace('+',gti)

    rsp_file = rsp_path.replace('+++',obs_id)
    rsp_file = rsp_file.replace('+',gti)

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

    #Plot
    if plot != 'None': 
        plt.rcParams['font.family'] = 'serif'
        plt.errorbar(frequencies,powers,yerr=errors,lw=0,elinewidth=0.5,color='cornflowerblue')
        plt.scatter(frequencies,powers,marker='o',color='cornflowerblue',s=2)
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
    
    #Return data
    return frequencies, powers, errors

def first_fooof_test():
    #Import(s)
    import numpy as np
    from fooof import FOOOF
    import matplotlib.pyplot as plt

    # Import a utility to download and load example data
    from fooof.utils.download import load_fooof_data

    #Action

    
    #Get data

    pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds'
    rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
    qpo_data = retrieve_qpo_data(ID='1130360110_0',pds_path=pds_temp,rsp_path=rsp_temp,plot='None')

    freqs = np.array(qpo_data[0])
    powers = 10**np.array(qpo_data[1])
    
    # Initialize a FOOOF object
    fm = FOOOF(max_n_peaks=3)

    # Set the frequency range to fit the model
    freq_range = [min(freqs), max(freqs)]

    # Report: fit the model, print the resulting parameters, and plot the reconstruction
    fm.report(freqs, powers, freq_range)

    #Plot
    plt.scatter(fm.freqs,fm.power_spectrum)
    plt.show()

def following_christopher():
    #Import(s)
    import math
    import numpy as np
    from scipy import optimize, signal
    from lmfit import models
    import matplotlib.pyplot as plt

    #Action
    
    #Get data
    pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds'
    rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
    qpo_data = retrieve_qpo_data(ID='1130360110_0',pds_path=pds_temp,rsp_path=rsp_temp,plot='None')

    freqs = np.array(qpo_data[0])
    powers = np.array(qpo_data[1])

    #Work

    def g(x, A, μ, σ):
        return A / (σ * math.sqrt(2 * math.pi)) * np.exp(-(x-μ)**2 / (2*σ**2))

    

pds_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-bin.pds'
rsp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/+++/jspipe/js_ni+++_0mpu7_silver_GTI+-fak.rsp'
qpo_data = retrieve_qpo_data(ID='1130360110_0',pds_path=pds_temp,rsp_path=rsp_temp,plot='Show')
