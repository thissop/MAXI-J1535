import os 
import re 
import pandas as pd 
import matplotlib.pyplot as plt 
from tqdm import tqdm 

dirs = ['/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/groj1655_pds',
        '/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/gx339_pds',
        '/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/xtej1550_pds']

for dir in dirs: 
    plot_dir = os.path.join(dir, 'plots')
    if not os.path.exists(plot_dir): 
        os.mkdir(plot_dir)
    for file in tqdm(os.listdir(dir)):
        if file.split('.')[-1] == 'asc': 
            frequencies = []
            powers = []
            errors = []

            original_path = os.path.join(dir, file)
            with open(original_path, 'r') as f: 
                for line in f: 
                    line_list = re.sub(' +', ',', line.replace('\n', '')).split(',')
                    frequencies.append(line_list[0])
                    powers.append(line_list[1])
                    errors.append(line_list[2])

            df = pd.DataFrame()
            df['frequency'] = frequencies
            df['power'] = powers
            df['error'] = errors

            fig, ax = plt.subplots()
            ax.scatter(frequencies, powers)

            try: 
                ax.set(xscale='log', yscale='log')
            except: 
                pass 

            ax.set(xlabel='Frequency', ylabel='Power', xlim=(1.5, 30))
            plt.tight_layout()
            plt.savefig(os.path.join(plot_dir, file.split('.')[0]+'.png'), dpi=200)
            plt.close()

            df.to_csv(original_path.replace(file, file.replace('asc','csv')), index=False)
            #os.remove(original_path)


