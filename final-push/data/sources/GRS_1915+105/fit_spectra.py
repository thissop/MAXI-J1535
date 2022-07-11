import xspec 
from xspec import * 

def first_routine(data_dir:str='final-push/data/sources/GRS_1915+105/spectral/external_spectra', 
                   output_file:str='final-push/data/sources/GRS_1915+105/spectral/spectral_summary.txt'): 
    import os 
    from tqdm import tqdm 
    import pandas as pd
    import re 

    if data_dir[-1]!='/':
        data_dir+='/'

    full_path_for_change = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'
    
    with open(output_file, 'w') as f: 
        f.write('obs_id,net_count_rate,gamma,kTe,nthcomp_norm,diskbb_tin,diskbb_norm,red_stat'+'\n')
    
    with open(output_file, 'a') as f1: 
        for dir in tqdm([i for i in os.listdir(data_dir) if i != '.gitkeep']): 
            output_list = []
            output_list.append(dir)        
            current_dir = data_dir+dir 
            os.chdir(full_path_for_change+current_dir)
            
            log_file = 'xspec_fit_log.txt'

            if not os.path.exists(log_file):

                Xset.chatter = 5
                Xset.logChatter = 10

                s1 = Spectrum('src_pcu2.pha')
                s1.ignore("**-2.5")
                s1.ignore("25.0-**")
                #AllData.ignore("bad")

                m1 = Model("tbabs*(diskbb+nthcomp)")

                m1.TBabs.nH = 6.0
                m1.TBabs.nH.frozen = True 

                m1.diskbb.Tin.values = ', , 0.2 0.2 3 3'

                m1.nthComp.Gamma.values = ', , 1.1 1.1 3. 3.'
                m1.nthComp.kT_bb.link = "2" #m1.diskbb.Tin 
                m1.nthComp.inp_type = 1
                m1.nthComp.inp_type.frozen = True
                m1.nthComp.Redshift = 0
                m1.nthComp.Redshift.frozen = True

                Fit.nIterations = 300

                Fit.perform()

                _ = Xset.openLog(log_file)
                s1.show()
                m1.show()
                Fit.show()
                Xset.closeLog()

                AllModels.clear()
                #AllData -= "*"
                m1 = None
                s1 = None

            # DATA ANALYSIS 
            with open(log_file, 'r') as f2: 
                found_fit_stat = False
                for line in f2: 
                    line_list = re.sub(' +', ',', line.strip()).split(',')
                    if 'Net count rate (cts/s)' in line: 
                        net_count_rate = line_list[6]
                        output_list.append(net_count_rate)
                    elif 'nthComp    Gamma' in line: 
                        gamma = line_list[4]
                        output_list.append(gamma)
                    elif 'nthComp    kT_e' in line: 
                        kT_e = line_list[5]
                        output_list.append(kT_e)
                    elif 'nthComp    norm' in line: 
                        nthcomp_norm = line_list[4]
                        output_list.append(nthcomp_norm)
                    elif 'diskbb     Tin' in line: 
                        diskbb_tin = line_list[5]
                        output_list.append(diskbb_tin)
                    elif 'diskbb     norm' in line: 
                        diskbb_norm = line_list[4]
                        output_list.append(diskbb_norm)
                    elif 'Fit statistic' in line and not found_fit_stat: 
                        stat = line_list[4]
                        found_fit_stat = True 
                    elif 'Null hypothesis' in line: 
                        dof = line_list[6]
                        red_stat = float(stat)/float(dof)            
                        output_list.append(red_stat)

            f1.write(','.join([str(i) for i in output_list])+'\n')  

first_routine()