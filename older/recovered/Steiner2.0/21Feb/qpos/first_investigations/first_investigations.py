def plot_psd_data(ID,path_temp):
    #Import(s)
    import matplotlib.pyplot as plt
    from astropy.io import fits
    import numpy as np

    #Action

    obs_id = ID.split('_')[0]
    gti = ID.split('_')[1]

    pds_file = path_temp.replace('+++',obs_id)
    pds_file = pds_file.replace('+',gti)

    channels = []
    count_rates = []
    errors = []
    
    with fits.open(pds_file) as hdul: 
        data = hdul[1].data
        data_length = len(data)
        for i in range(data_length):
            channels.append(float(data[i][0]))
            count_rates.append(float(data[i][1]))
            errors.append(float(data[i][2]))
    

    #Plot
    plt.rcParams['font.family'] = 'serif'
    plt.errorbar(list(np.array(channels)/10),count_rates,yerr=errors,lw=0,elinewidth=0.5,color='cornflowerblue')
    plt.scatter(list(np.array(channels)/10),count_rates,marker='o',color='cornflowerblue',s=2)
    plt.xlabel('Frequency [Hz] (?)')
    plt.ylabel('rms-Normalized Power')
    plt.xscale('log')
    plt.yscale('log')
    save_path = '/home/thaddaeus/FMU/Steiner2.0/21Feb/qpos/first_investigations/first_plots/+++_+.png'.replace('+++',obs_id)
    save_path = save_path.replace('+',gti)
    plt.savefig(save_path)
    plt.clf()

 
def testing_stingray():
    #Import(s)
    from stingray import Powerspectrum
    import numpy as np
    from astropy.modeling import models
    import matplotlib.pyplot as plt

    #Action

    #first 
    m = 1
    nfreq = 100000
    freq = np.linspace(1, 1000, nfreq)

    np.random.seed(100)  # set the seed for the random number generator
    noise = np.random.exponential(size=nfreq)

    model = models.PowerLaw1D() + models.Const1D()
    model.x_0_0.fixed = True

    alpha_0 = 2.0
    amplitude_0 = 100.0
    amplitude_1 = 2.0

    model.alpha_0 = alpha_0
    model.amplitude_0 = amplitude_0
    model.amplitude_1 = amplitude_1

    p = model(freq)
    power = noise * p

    ps = Powerspectrum()
    ps.freq = freq
    ps.power = power
    ps.m = m
    ps.df = freq[1] - freq[0]
    ps.norm = "leahy"

    #Lorenziation 
    l = models.Lorentz1D
    def fit_lorentzians(ps, nlor, starting_pars, fit_whitenoise=True, max_post=False, priors=None,fitmethod="L-BFGS-B"):

        model = models.Lorentz1D()

        if nlor > 1:
            for i in range(nlor-1):
                model += models.Lorentz1D()

        if fit_whitenoise:
            model += models.Const1D()

        parest = PSDParEst(ps, fitmethod=fitmethod, max_post=max_post)
        lpost = PSDPosterior(ps.freq, ps.power, model, priors=priors, m=ps.m)
        res = parest.fit(lpost, starting_pars, neg=True)

        return parest, res
    
    np.random.seed(400)
    nlor = 3

    x_0_0 = 0.5
    x_0_1 = 2.0
    x_0_2 = 7.5

    amplitude_0 = 150.0
    amplitude_1 = 50.0
    amplitude_2 = 15.0

    fwhm_0 = 0.1
    fwhm_1 = 1.0
    fwhm_2 = 0.5

    whitenoise = 2.0

    model = models.Lorentz1D(amplitude_0, x_0_0, fwhm_0) + \
            models.Lorentz1D(amplitude_1, x_0_1, fwhm_1) + \
            models.Lorentz1D(amplitude_2, x_0_2, fwhm_2) + \
            models.Const1D(whitenoise)

    p = model(ps.freq)
    noise = np.random.exponential(size=len(ps.freq))

    power = p*noise

    #Plot
    plt.figure()
    plt.loglog(ps.freq, power, lw=1, ds="steps-mid", c="black")
    plt.loglog(ps.freq, p, lw=3, color="red")
    plt.show()

def second_sting_test():
    #Import(s)
    from stingray import Powerspectrum
    import numpy as np
    from astropy.modeling import models

    #Action

    m = 1
    nfreq = 100000
    freq = np.linspace(1, 1000, nfreq)

    np.random.seed(100)  # set the seed for the random number generator
    noise = np.random.exponential(size=nfreq)

    model = models.PowerLaw1D() + models.Const1D()
    model.x_0_0.fixed = True

    alpha_0 = 2.0
    amplitude_0 = 100.0
    amplitude_1 = 2.0

    model.alpha_0 = alpha_0
    model.amplitude_0 = amplitude_0
    model.amplitude_1 = amplitude_1

    p = model(freq)
    power = noise * p

    ps = Powerspectrum()
    ps.freq = freq
    ps.power = power
    ps.m = m
    ps.df = freq[1] - freq[0]
    ps.norm = "frac"   

    print(list(ps))




