lines = []
with open('quick-fixes/main.tex', 'r') as f: 
    for line in f: 
        if 'includegraphics' in line: 
            line = line.replace('[', '').replace(']', '').replace('-', '').replace(' ', '')
        lines.append(line)


with open('quick-fixes/main.tex', 'w') as f: 
    for line in lines: 
        f.write(line)

import os
rootdir = '/Users/yaroslav/Downloads/MAXIJ1535_ML'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        fp = os.path.join(subdir, file)
        new_fp = fp.replace('[', '').replace(']', '').replace('-', '').replace(' ', '')
        os.rename(fp, new_fp)