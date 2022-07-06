# /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/routine_executor.py
import xspec 
from xspec import *

def run_routine(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                nH_data:str = './code/misc/meta_preparation/rxte_motta/fit_routine/preparation/nH_dict.csv', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results'): 

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np
    import os
    import re 

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+data_dir[2:]

    if nH_data[0:6]=='./code': 
        nH_data = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+nH_data[2:]

    if log_path[0:6] == './code': 
        log_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+log_path[2:]

    warnings.warn('bouma idea: jupyter notebook vs python file paths')

    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    objects = key_df['object']
    responses = key_df['resp_file']

    nH_df = pd.read_csv(nH_data)
    nH_sources = nH_df['source']
    nH_values = nH_df['nH']

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    output = log_path+'/output.csv'

    with open(output, 'w') as f: 
        f.write('obsid,gamma,kT_e,nthcomp_norm,diskbb_Tin,diskbb_norm,red_pgstat'+'\n')

    for index in tqdm(range(len(key_df.index))): 
        full_id = ids[index]
        id_list = full_id.split('_')
        prop_num = id_list[0]

        source_name = objects[index]

        data_dir = data_dir+prop_num+'/'

        spectrum_path = data_dir+source_spectrums[index]
        s1 = Spectrum(spectrum_path)

        s1.ignore("**-3.0") 
        s1.ignore('45.-**')
        #AllData.ignore("bad")

        m1 = Model("tbabs*(nthcomp+diskbb)")

        # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
        # print(m1.TBabs.parameterNames) # ['nH']
        # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
        # print(m1.diskbb.parameterNames) # ['Tin', 'norm']
        
        m1.TBabs.nH = nH_values[np.where(nH_sources==source_name)[0][0]]
        m1.TBabs.nH.frozen = True 

        warnings.warn('is it okay to have nH from different literature models?')

        m1.nthComp.Gamma.values = '2 , 1.1 1.2 3.5 4'
        m1.nthComp.kT_e.values = '50 , 10 10 300 300' # fix this!
        m1.nthComp.kT_bb.link = "8" #m1.diskbb.Tin 
        m1.nthComp.inp_type = 1
        m1.nthComp.inp_type.frozen = True
        m1.nthComp.Redshift = 0
        m1.nthComp.Redshift.frozen = True

        warnings.warn('red shift?')

        m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

        Fit.nIterations = 300
        Fit.statMethod = "pgstat"

        Fit.perform()

        log_file_path = log_path+'/'+full_id+'.txt'
        log_file = Xset.openLog(log_file_path)
        s1.show()
        m1.show()
        Fit.show()
        Xset.closeLog()

        AllModels.clear()
        #AllData -= "*"

        # DATA ANALYSIS 

        with open(log_file_path, 'r') as f: 
            for line in f: 
                line_list = re.sub(' +', ',', line.strip()).split(',')
                if 'nthComp    Gamma' in line: 
                    gamma = line_list[4]
                elif 'nthComp    kT_e' in line: 
                    kT_e = line_list[5]
                elif 'nthComp    norm' in line: 
                    nthcomp_norm = line_list[4]

                elif 'diskbb     Tin' in line: 
                    diskbb_tin = line_list[5]
                    
                elif 'diskbb     norm' in line: 
                    diskbb_norm = line_list[4]

                elif 'Fit statistic  : PG-Statistic' in line: 
                    pgstat = line_list[4]
                elif 'Null hypothesis' in line: 
                    dof = line_list[6]
                    red_pgstat = float(pgstat)/float(dof)

        with open(output, 'a') as f: 
            result_list = [full_id,gamma,kT_e,nthcomp_norm,diskbb_tin,diskbb_norm,red_pgstat]
            f.write(','.join([str(i) for i in result_list])+'\n')
            
        os.remove(log_file_path)

        # go scrape that data before running another iteration, delete log. 
#run_routine()

def run_nh_routine(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results'):

    print('starting...')

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np
    import os
    import re 

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+data_dir[2:]

    if log_path[0:6] == './code': 
        log_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+log_path[2:]


    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    objects = key_df['object']
    responses = key_df['resp_file']

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    output = log_path+'/output.csv'

    with open(output, 'w') as f: 
        f.write('obsid,gamma,kT_e,nthcomp_norm,diskbb_Tin,diskbb_norm,red_pgstat'+'\n')

    for index in tqdm(range(len(key_df.index))): 
        full_id = ids[index]
        id_list = full_id.split('_')
        prop_num = id_list[0]

        source_name = objects[index]

        data_dir = data_dir+prop_num+'/'

        spectrum_path = data_dir+source_spectrums[index]
        s1 = Spectrum(spectrum_path)

        s1.ignore("**-3.0") 
        s1.ignore('45.-**')
        AllData.ignore("bad")

        m1 = Model("tbabs*(pow+diskbb)")

        # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
        # print(m1.TBabs.parameterNames) # ['nH']
        # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
        # print(m1.diskbb.parameterNames) # ['Tin', 'norm']
        
        m1.powerlaw.PhoIndex.values = ', , 1.1 1.2 3.5 4'

        warnings.warn('red shift?')

        m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

        Fit.nIterations = 100

        Fit.statMethod = "pgstat"

        Fit.perform()

        log_file_path = log_path+'/'+full_id+'.txt'
        log_file = Xset.openLog(log_file_path)
        s1.show()
        m1.show()
        Fit.show()
        Xset.closeLog()

        AllModels.clear()
        #AllData -= "*"

        # DATA ANALYSIS 

        with open(log_file_path, 'r') as f: 
            for line in f: 
                line_list = re.sub(' +', ',', line.strip()).split(',')
                if 'TBabs      nH' in line: 
                    nH = line_list[5]
                elif 'Fit statistic  : PG-Statistic' in line: 
                    pgstat = line_list[4]
                elif 'Null hypothesis' in line: 
                    dof = line_list[6]
                    red_pgstat = float(pgstat)/float(dof)

        with open(output, 'a') as f: 
            result_list = [full_id,nH,red_pgstat]
            f.write(','.join([str(i) for i in result_list])+'\n')
            
        os.remove(log_file_path)

        break                 

#run_nh_routine()

def run_nH_nthcomp_routine(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results'): 

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np
    import os
    import re 

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+data_dir[2:]

    if log_path[0:6] == './code': 
        log_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'+log_path[2:]


    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    objects = key_df['object']
    responses = key_df['resp_file']

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    output = log_path+'/output.csv'

    with open(output, 'w') as f: 
        f.write('obsid,source,nH,gamma,kT_e,nthcomp_norm,diskbb_Tin,diskbb_norm,red_pgstat'+'\n')

    for index in tqdm(range(len(key_df.index))): 
        try: 
            temp_data_dir = data_dir
            
            full_id = ids[index]
            id_list = full_id.split('_')
            prop_num = id_list[0]

            source_name = objects[index]
            
            temp_data_dir = temp_data_dir+prop_num+'/'
            spectrum_path = temp_data_dir+source_spectrums[index]
            
            s1 = Spectrum(spectrum_path)

            s1.ignore("**-3.0") 
            s1.ignore('45.-**')
            #AllData.ignore("bad")

            m1 = Model("tbabs*(nthcomp+diskbb)")

            # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
            # print(m1.TBabs.parameterNames) # ['nH']
            # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
            # print(m1.diskbb.parameterNames) # ['Tin', 'norm']

            m1.TBabs.nH.values = '2 , 1 1 15 15'
            m1.nthComp.Gamma.values = '2 , 1.1 1.2 3.5 4'
            m1.nthComp.kT_e.values = '50 , 10 10 300 300' 
            m1.nthComp.kT_bb.link = "8" #m1.diskbb.Tin 
            m1.nthComp.inp_type = 1
            m1.nthComp.inp_type.frozen = True
            m1.nthComp.Redshift = 0
            m1.nthComp.Redshift.frozen = True

            m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

            Fit.nIterations = 300
            Fit.statMethod = "pgstat"

            Fit.perform()

            log_file_path = log_path+'/'+full_id+'.txt'
            log_file = Xset.openLog(log_file_path)
            s1.show()
            m1.show()
            Fit.show()
            Xset.closeLog()

            AllModels.clear()
            #AllData -= "*"

            # DATA ANALYSIS 

            with open(log_file_path, 'r') as f: 
                for line in f: 
                    line_list = re.sub(' +', ',', line.strip()).split(',')
                    if 'TBabs      nH' in line: 
                        nH = line_list[5]
                    if 'nthComp    Gamma' in line: 
                        gamma = line_list[4]
                    elif 'nthComp    kT_e' in line: 
                        kT_e = line_list[5]
                    elif 'nthComp    norm' in line: 
                        nthcomp_norm = line_list[4]

                    elif 'diskbb     Tin' in line: 
                        diskbb_tin = line_list[5]
                        
                    elif 'diskbb     norm' in line: 
                        diskbb_norm = line_list[4]

                    elif 'Fit statistic  : PG-Statistic' in line: 
                        pgstat = line_list[4]
                    elif 'Null hypothesis' in line: 
                        dof = line_list[6]
                        red_pgstat = float(pgstat)/float(dof)

            with open(output, 'a') as f: 
                result_list = [full_id,source_name,nH,gamma,kT_e,nthcomp_norm,diskbb_tin,diskbb_norm,red_pgstat]
                f.write(','.join([str(i) for i in result_list])+'\n')
                
            os.remove(log_file_path)

        except: 
            continue 
            
#run_nH_nthcomp_routine()

def run_pycorrected_with_nH_initial(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results', 
                nH_csv:str='./code/misc/meta_preparation/rxte_motta/fit_routine/preparation/nH_dict.csv'): 

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np
    import os
    import re 

    linux = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = linux+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = linux+data_dir[2:]

    if log_path[0:6] == './code': 
        log_path = linux+log_path[2:]

    if nH_csv[0:6]=='./code': 
        nH_csv = linux+nH_csv[2:]

    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    objects = key_df['object']
    responses = key_df['resp_file']
    nH_df = pd.read_csv(nH_csv)

    nH_df = nH_df.iloc[list(~nH_df['neutron star'])]
    nH_df = nH_df.iloc[list(nH_df['double checked'])]

    nH_objects = np.array(nH_df['source'])
    nHs = np.array(nH_df['first nH'])
    temp = []

    for i in nHs: 
        nh_list = i.split('*')
        if nh_list[1]=='10^21': 
            temp.append(str(float(nh_list[0])/10))
        else: 
            temp.append(nh_list[0])

    nHs = temp

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    output = log_path+'/output-pycorr and nH testing.csv'

    with open(output, 'w') as f: 
        f.write('obsid,source,nH,gamma,kT_e,nthcomp_norm,diskbb_Tin,diskbb_norm,red_pgstat'+'\n')
    counter = 0 
    for index in tqdm(range(len(key_df.index))): 
        #try: 
        temp_data_dir = data_dir
        
        full_id = ids[index]
        id_list = full_id.split('_')
        prop_num = id_list[0]

        source_name = objects[index]
        
        temp_data_dir = temp_data_dir+prop_num+'/'
        spectrum_path = temp_data_dir+source_spectrums[index]
        corrected_spectrum = spectrum_path.replace('.pha', '-corr.pha')

        if os.path.exists(corrected_spectrum):  
            
            if source_name in nH_objects:
                s1 = None
                s1 = Spectrum(corrected_spectrum)

                s1.ignore("**-3.0") 
                s1.ignore('45.-**')
                #AllData.ignore("bad")

                m1 = None
                m1 = Model("tbabs*(nthcomp+diskbb)")

                # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
                # print(m1.TBabs.parameterNames) # ['nH']
                # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
                # print(m1.diskbb.parameterNames) # ['Tin', 'norm']

                index = np.where(nH_objects==source_name)[0][0]
                source_nH = nHs[index]
                m1.TBabs.nH = source_nH

                counter = counter+1

                '''
                if counter>25: 
                    break 
                '''

                m1.TBabs.nH.frozen = True
                m1.nthComp.Gamma.values = '2 , 1.1 1.2 3.5 4'
                m1.nthComp.kT_e.values = '50 , 10 10 300 300' 
                m1.nthComp.kT_bb.link = "8" #m1.diskbb.Tin 
                m1.nthComp.inp_type = 1
                m1.nthComp.inp_type.frozen = True
                m1.nthComp.Redshift = 0
                m1.nthComp.Redshift.frozen = True

                m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

                Fit.nIterations = 500
                Fit.statMethod = "pgstat"

                Fit.perform()

                log_file_path = log_path+'/'+full_id+'.txt'
                log_file = Xset.openLog(log_file_path)
                s1.show()
                m1.show()
                Fit.show()
                Xset.closeLog()

                AllModels.clear()
                
                # DATA ANALYSIS 

                with open(log_file_path, 'r') as f: 
                    for line in f: 
                        line_list = re.sub(' +', ',', line.strip()).split(',')
                        if 'TBabs      nH' in line: 
                            nH = line_list[5]
                        if 'nthComp    Gamma' in line: 
                            gamma = line_list[4]
                        elif 'nthComp    kT_e' in line: 
                            kT_e = line_list[5]
                        elif 'nthComp    norm' in line: 
                            nthcomp_norm = line_list[4]

                        elif 'diskbb     Tin' in line: 
                            diskbb_tin = line_list[5]
                            
                        elif 'diskbb     norm' in line: 
                            diskbb_norm = line_list[4]

                        elif 'Fit statistic  : PG-Statistic' in line: 
                            pgstat = line_list[4]
                        elif 'Null hypothesis' in line: 
                            dof = line_list[6]
                            red_pgstat = float(pgstat)/float(dof)

                with open(output, 'a') as f: 
                    result_list = [full_id,source_name,nH,gamma,kT_e,nthcomp_norm,diskbb_tin,diskbb_norm,red_pgstat]
                    f.write(','.join([str(i) for i in result_list])+'\n')
                    
                os.remove(log_file_path)
        
        '''
        except: 
            print('error!!!')
            break 
            continue 
        '''

#run_pycorrected_with_nH_initial()

def one_obj_only_rerun(fits_key: str='./code/misc/meta_preparation/rxte_motta/fits_key.csv', 
                data_dir:str='./data/processed/2022/meta_qpo/motta_spectral_files', 
                log_path:str='./code/misc/meta_preparation/rxte_motta/fit_routine/results', 
                nH_csv:str='./code/misc/meta_preparation/rxte_motta/fit_routine/preparation/nH_dict.csv'): 

    import pandas as pd
    from tqdm import tqdm
    import warnings
    import numpy as np
    import os
    import re 

    linux = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/'

    if data_dir[-1]!='/': 
        data_dir+='/'

    if fits_key[0:6] == './code': 
        fits_key = linux+fits_key[2:]

    if data_dir[0:6]=='./data': 
        data_dir = linux+data_dir[2:]

    if log_path[0:6] == './code': 
        log_path = linux+log_path[2:]

    if nH_csv[0:6]=='./code': 
        nH_csv = linux+nH_csv[2:]

    key_df = pd.read_csv(fits_key)
    ids = np.array(key_df['obsid'])
    source_spectrums = key_df['spectral_file']
    objects = key_df['object']
    responses = key_df['resp_file']
    nH_df = pd.read_csv(nH_csv)

    nH_df = nH_df.iloc[list(~nH_df['neutron star'])]
    nH_df = nH_df.iloc[list(nH_df['double checked'])]

    nH_objects = np.array(nH_df['source'])
    nHs = np.array(nH_df['first nH'])
    temp = []

    for i in nHs: 
        nh_list = i.split('*')
        if nh_list[1]=='10^21': 
            temp.append(str(float(nh_list[0])/10))
        else: 
            temp.append(nh_list[0])

    nHs = temp

    Xset.chatter = 0
    Xset.logChatter = 10
    Fit.query = "no"

    output = log_path+'/XTE_J1550-564 testing.csv'

    with open(output, 'w') as f: 
        f.write('obsid,source,nH,gamma,kT_e,nthcomp_norm,diskbb_Tin,diskbb_norm,red_pgstat'+'\n')
    counter = 0 
    for index in tqdm(range(len(key_df.index))): 
        #try: 
        temp_data_dir = data_dir
        
        full_id = ids[index]
        id_list = full_id.split('_')
        prop_num = id_list[0]

        source_name = objects[index]
        
        temp_data_dir = temp_data_dir+prop_num+'/'
        spectrum_path = temp_data_dir+source_spectrums[index]
        corrected_spectrum = spectrum_path.replace('.pha', '-corr.pha')

        if os.path.exists(corrected_spectrum) and source_name=='XTE_J1550-564':  
            
            if source_name in nH_objects:
                s1 = None
                s1 = Spectrum(corrected_spectrum)

                s1.ignore("**-3.0") 
                s1.ignore('45.-**')
                #AllData.ignore("bad")

                m1 = None
                m1 = Model("tbabs*(nthcomp+diskbb)")

                # print(m1.componentNames) # ['TBabs', 'nthcomp', 'diskbb']
                # print(m1.TBabs.parameterNames) # ['nH']
                # print(m1.nthComp.parameterNames) # ['Gamma', 'kT_e', 'kT_bb', 'inp_type', 'Redshift', 'norm']
                # print(m1.diskbb.parameterNames) # ['Tin', 'norm']

                index = np.where(nH_objects==source_name)[0][0]
                source_nH = nHs[index]
                m1.TBabs.nH = source_nH

                counter = counter+1

                '''
                if counter>25: 
                    break 
                '''

                m1.TBabs.nH.frozen = True
                m1.nthComp.Gamma.values = '2 , 1.1 1.2 3.5 4'
                m1.nthComp.kT_e.values = '31' 
                m1.nthComp.kT_e.frozen = True
                m1.nthComp.kT_bb.link = "8" #m1.diskbb.Tin 
                m1.nthComp.inp_type = 1
                m1.nthComp.inp_type.frozen = True
                m1.nthComp.Redshift = 0
                m1.nthComp.Redshift.frozen = True

                m1.diskbb.Tin.values = ',, 0.2 0.2 2 3'

                Fit.nIterations = 500
                Fit.statMethod = "pgstat"

                Fit.perform()

                log_file_path = log_path+'/'+full_id+'.txt'
                log_file = Xset.openLog(log_file_path)
                s1.show()
                m1.show()
                Fit.show()
                Xset.closeLog()

                AllModels.clear()
                
                # DATA ANALYSIS 

                with open(log_file_path, 'r') as f: 
                    for line in f: 
                        line_list = re.sub(' +', ',', line.strip()).split(',')
                        if 'TBabs      nH' in line: 
                            nH = line_list[5]
                        if 'nthComp    Gamma' in line: 
                            gamma = line_list[4]
                        elif 'nthComp    kT_e' in line: 
                            kT_e = line_list[5]
                        elif 'nthComp    norm' in line: 
                            nthcomp_norm = line_list[4]

                        elif 'diskbb     Tin' in line: 
                            diskbb_tin = line_list[5]
                            
                        elif 'diskbb     norm' in line: 
                            diskbb_norm = line_list[4]

                        elif 'Fit statistic  : PG-Statistic' in line: 
                            pgstat = line_list[4]
                        elif 'Null hypothesis' in line: 
                            dof = line_list[6]
                            red_pgstat = float(pgstat)/float(dof)

                with open(output, 'a') as f: 
                    result_list = [full_id,source_name,nH,gamma,kT_e,nthcomp_norm,diskbb_tin,diskbb_norm,red_pgstat]
                    f.write(','.join([str(i) for i in result_list])+'\n')
                    
                os.remove(log_file_path)

one_obj_only_rerun()