def first_plays(id, log_dir, plot_dir):
    # Import(s)
    import re
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks, peak_prominences, peak_widths
    
    # Action
    freqs = np.array([])
    norms = np.array([])
    redchis = np.array([])
    widths = np.array([])
    log_dir_ = log_dir + '/' +  id
    
    def save_to_csv(freqs, norms, redchis, widths):
    
        test_freqs = 10**np.linspace(0.02, np.log10(20), 268)
        for file_number, freq in zip(range(0, 268), test_freqs): 
            file_path = log_dir_+'/'+id + '_' + str(file_number) +'.txt'
            freqs = np.append(freqs, freq)
            with open(file_path, 'r') as f:
                for line in f: 
                    if 'lorentz' in line and 'frozen' not in line: 
                        if 'norm' in line: 
                            norm = float((re.sub(' +',',',line)).split(',')[5])
                            norms = np.append(norms, norm)
                    
                    if 'Width' in line and 'frozen' not in line: 
                        width = float((re.sub(' +',',',line)).split(',')[6])
                        widths = np.append(widths, width)
                    
                    elif 'Test statistic' in line: 
                        chi = float((re.sub(' +',',',line)).split(',')[4])
                    
                    elif 'degrees of freedom' in line:
                        dof = float((re.sub(' +',',',line)).split(',')[7])
                
                red_chi = chi/dof
                redchis = np.append(redchis, red_chi)
                
        zipped = list(zip(freqs, redchis, norms, widths))
        df = pd.DataFrame(zipped, columns=['freq', 'redchi', 'norm', 'width'])            
        df.to_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/csv_qpo_files'+'/'+id+'.csv', index=False)
    
    #save_to_csv(freqs, norms, redchis, widths)
    
    data_path = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/csv_qpo_files'+'/'+id+'.csv'
    df = pd.read_csv(data_path)
    freqs = np.array(df['freq'])
    norms = np.array(df['norm'])
    redchis = np.array(df['redchi'])
    
    # Simple plot
    fig, axs = plt.subplots(2, 2)
    plt.tight_layout()
    
    max_redchi, sigma_redchi = np.max(redchis), np.std(redchis)
    
    axs[0, 0].scatter(freqs, redchis, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    axs[0, 0].set_xlabel('Frequency [Hz]')
    axs[0, 0].set_ylabel('red. '+r'$\chi^2$')
    axs[0, 0].hlines(y=max_redchi-sigma_redchi, xmin=min(freqs), xmax=max(freqs), label='Max '+r'$-1\sigma$')
    axs[0, 0].hlines(y=max_redchi-2*sigma_redchi, xmin=min(freqs), xmax=max(freqs), label='Max '+r'$-2\sigma$')
    
    peaks, _ = find_peaks(-1*redchis, distance=20)

    prominences = peak_prominences(-1*redchis, peaks)[0]
    
    contour_heights = redchis[peaks] + prominences
    
    axs[0, 0].plot(freqs[peaks], redchis[peaks], "x", color='C1')
    
    axs[0, 0].vlines(x=freqs[peaks], ymin=contour_heights, ymax=redchis[peaks], color='C1', label='Prominences')
   
    axs[0,1].scatter(freqs, norms, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    axs[0,1].set_xlabel('Frequency [Hz]')
    axs[0,1].set_ylabel('Norm.')
    
    min_norm, sigma_norm = np.min(norms), np.std(norms)
    
    axs[0,1].hlines(y=min_norm+sigma_norm, xmin=min(freqs), xmax=max(freqs), label='Min '+r'$+1\sigma$')
    axs[0,1].hlines(y=min_norm+2*sigma_norm, xmin=min(freqs), xmax=max(freqs), label='Min '+r'$+2\sigma$')
    
    peaks, _ = find_peaks(norms, distance=20)

    prominences = peak_prominences(norms, peaks)[0]
    
    contour_heights = norms[peaks] - prominences
    
    axs[0,1].plot(freqs[peaks], norms[peaks], "x", color='C1')
    
    axs[0,1].vlines(x=freqs[peaks], ymin=contour_heights, ymax=norms[peaks], color='C1', label='Prominences')
    
    for ax in [axs[0,0], axs[0,1]]:
        ax.legend(fontsize='small')
    
    image = plt.imread('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/alpha_qpo_fitting/first_run/plots/+++.png'.replace('+++', id))

    axs[1,0].imshow(image)
    axs[1, 0].axis('off')
    
    axs[1,1].axis('off')
    
    plt.subplots_adjust(wspace=0.45)
    
    plt.savefig(plot_dir+'/'+id+'.png', bbox_inches='tight', dpi=200)
    plt.clf()
    plt.close()
    
log_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/beta_run/logs'
plot_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/plots'


import pandas as pd   
ids = list(pd.read_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/temp_ids.txt')['ID'])

for id in ids: 
    first_plays(id, log_dir, plot_dir)