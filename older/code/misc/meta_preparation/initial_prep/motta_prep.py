from tabnanny import check


def add_segment(name, type, inclination, 
                temp_file:str='./data/processed/2022/meta_qpo/motta_holding.txt',
                clean_file:str='./data/processed/2022/meta_qpo/motta_cleaned.csv'): 

    import os 
    import pandas as pd
    import numpy as np

    nums = []
    ids = []

    freqs = []
    freq_bounds = []

    qpo_rms_values = []
    qpo_rms_bounds = []

    noise_rms_values = []
    noise_rms_bounds = []

    total_rms_values = []
    total_rms_bounds = []

    def extract(string): 

        if string == '0.0': 
            return 0, '"(0,0)"'

        value = float(string[0:string.index('$')])
        string = string[string.index('{'):]
        string = string.replace('$','')
        string_list = string.split('^')

        for char in ['+','-','{','}']: 
            for index, item in enumerate(string_list): 
                string_list[index] = item.replace(char, '')

        bounds = tuple(float(i) for i in string_list)

        return value, '"'+str(bounds)+'"'

    with open(temp_file, 'r') as f: 
        for line in f: 
            line_list = line.split('&')

            nums.append(line_list[0])
            ids.append(line_list[1])

            freq, bounds = extract(line_list[2])
            freqs.append(freq)
            freq_bounds.append(bounds)

            qpo_rms, qpo_rms_bound = extract(line_list[3])
            qpo_rms_values.append(qpo_rms)
            qpo_rms_bounds.append(qpo_rms_bound)

            noise_rms, noise_rms_bound = extract(line_list[4])
            noise_rms_values.append(noise_rms)
            noise_rms_bounds.append(noise_rms_bound)

            total_rms, total_rms_bound = extract(line_list[5])
            total_rms_values.append(total_rms)
            total_rms_bounds.append(total_rms_bound)

    length = len(nums)
    types = length*[type]
    inclinations = length*[inclination]
    sources = length*[name]

    cols = [ids, sources, types, inclinations, freqs, qpo_rms_values, noise_rms_values, total_rms_values]
    cols += [freq_bounds, noise_rms_bounds, total_rms_bounds, nums]

    header = 'ID,source,type,inclination,freq,qpo_rms,noise_rms,total_rms,freq_err,noise_err,total_err,number'

    df = pd.DataFrame(np.transpose(cols), columns=header.split(','))

    if not os.path.exists(clean_file): 
        with open(clean_file, 'w') as f: 
            f.write(header+'\n')

    for index in range(length): 
        with open(clean_file, 'a') as f: 
            out_str =','.join([str(i) for i in df.loc[index].tolist()])+'\n'
            f.write(out_str)
            
#add_segment('MAXI J1659-15', 'B', 'high')

def check_motta(clean_file:str='./data/processed/2022/meta_qpo/motta_cleaned.csv'): 
    import pandas as pd

    df = pd.read_csv(clean_file)

    correct_order = True

    nums = list(range(1, 565))
    for index, val in enumerate(df['number']): 
        if val!=nums[index]:
            correct_order=False
            break 

    assert correct_order # true

#check_motta()

def add_classes(clean_file:str='./data/processed/2022/meta_qpo/motta_cleaned.csv'):
    import pandas as pd

    df = pd.read_csv(clean_file)
    
    sources = list(df['source'])
    types = list(df['type'])
    inclinations = list(df['inclination'])

    combined = [sources[i]+':'+types[i]+':'+inclinations[i] for i in range(len(sources))]

    class_options = list(set(combined))

    class_nums = [str(i) for i in list(range(len(class_options)))]

    class_dict = dict(zip(class_options, class_nums))

    classes = []

    for i in range(len(sources)): 
        test_str = sources[i]+':'+types[i]+':'+inclinations[i]
        classes.append(class_dict[test_str])
    
    df['class'] = classes 

    df.to_csv(clean_file, index=False)

#add_classes()

def classes_plot(clean_file:str='./data/processed/2022/meta_qpo/motta_cleaned.csv'):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    df = pd.read_csv(clean_file)
    
    classes = np.array(df['class'])

    set_classes = list(set(classes))

    print(set_classes)
    counts = [len(np.where(classes==qpo_class)[0]) for qpo_class in set_classes]

    plt.style.use('https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/misc/stolen_science.mplstyle?token=GHSAT0AAAAAABP54PQO2X2VXMNS256IWOBOYRNCFBA')

    plt.bar(set_classes, counts)

    plt.gca().set(xlabel='Motta et al. Class', ylabel='Frequency')

    #plt.show()
    plt.savefig('code/misc/meta_preparation/motta_classes_hist.png', bbox_inches='tight', dpi=150)

classes_plot()