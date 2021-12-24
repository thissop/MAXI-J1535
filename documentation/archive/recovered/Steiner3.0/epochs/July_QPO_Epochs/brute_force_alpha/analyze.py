def make_summary_plots(ids, log_dir, plot_dir):
    import os 
    import re
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoMinorLocator


    for id in ids: 
        freqs = np.array([])
        norms = np.array([])
        redchis = np.array([])
        widths = np.array([])
        log_dir_ = log_dir + '/' +  id
                    
        
        print(id)
        
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
                
                #if width > 0.11*freq or width < 0.09*freq:
                    #print(list(test_freqs).index(freq), width, freq)
                
                red_chi = chi/dof
                redchis = np.append(redchis, red_chi)
                        
        plt.rcParams['font.family']='serif'
        fig, axs = plt.subplots(2,2)



        axs[0,0].scatter(freqs, redchis, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
        axs[0,0].set_xlabel('Frequency [Hz]')
        axs[0,0].set_ylabel('red. '+r'$\chi^2$')
        
        axs[0,1].scatter(freqs, norms, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
        axs[0,1].set_xlabel('Frequency [Hz]')
        axs[0,1].set_ylabel('Norm.')


        image = plt.imread('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/alpha_qpo_fitting/first_run/plots/+++.png'.replace('+++', id))

        axs[1,0].imshow(image)

        for ax in [axs[0,0], axs[0, 1], axs[1, 1]]:
            #ax.xaxis.set_minor_locator(AutoMinorLocator())    
            ax.tick_params(axis='both',which='both',direction='in')
            ax.tick_params(which='both',bottom=True,top=True,left=True,right=True)
            ax.tick_params(labelbottom=True,labeltop=False,labelleft=True,labelright=False)
            ax.set_xscale('log')
            ax.set_yscale('log')

        axs[1, 0].axis('off')

        axs[1,1].scatter(freqs, widths, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
        axs[1, 1].set_xlabel('Frequency [Hz]')
        axs[1, 1].set_ylabel('Width')

        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        plot_path = plot_dir+'/'+id+'.png'
        plt.savefig(plot_path, dpi=250) 
        plt.clf()
        plt.close()  
        
        ###
        
        #zipped = list(zip(freqs, norms, redchis, widths))
        
        #ex_df = pd.DataFrame(zipped, columns=['Frequency', 'Norm', 'redchi', 'width'])
        #ex_df.to_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/ExtraForSteiner/table.csv', index=False)
          
import pandas as pd   
ids = list(pd.read_csv('/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/temp_ids.txt')['ID'])



log_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/beta_run/logs'
plot_dir = '/home/thaddaeus/FMU/Steiner3.0/epochs/July_QPO_Epochs/brute_force_beta/plots'



make_summary_plots(ids, log_dir, plot_dir)