import os 
import shutil 
from tqdm import tqdm

filenames = []

download_dir = '/Users/yaroslav/Downloads/MAXIJ1535_ML_Thaddaeus/'
output_path = '/Users/yaroslav/Documents/Work/GitHub/MAXI-J1535/referee-feedback/final/final-figures'
tex_path = '/Users/yaroslav/Downloads/MAXIJ1535_ML_Thaddaeus/main-v2.tex'
with open(tex_path, 'r') as f: 
    for line in tqdm(f): 
        if 'includegraphics' and 'pdf' in line: 
            if '%' not in line: 
                filename = line.split('{')[-1].split('}')[0]
                old_path = os.path.join(download_dir, filename)
                new_path = os.path.join(output_path, filename.split('/')[-1])
                shutil.copyfile(old_path, new_path)