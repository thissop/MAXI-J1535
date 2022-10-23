
import numpy as np
def get_count(rootdir, types=['py','sh', 'tcl', 'ipynb', 'md', 'MD']): 
    import glob 
    from json import load

    def loc(nb):
        with open(nb, encoding='utf-8') as data_file:
            cells = load(data_file)['cells']
            return sum(len(c['source']) for c in cells if c['cell_type'] == 'code')

    def run(ipynb_files):
        return sum(loc(nb) for nb in ipynb_files)

    lines = 0
    files = 0
    errors = 0

    for t in types:
        for filepath in glob.iglob(rootdir+f'**/*.{t}', recursive=True): 
            try: 
                files += 1
                if t!='ipynb':
                    with open(filepath, 'r') as f: 
                        for line in f: 
                            lines+= 1

                else: 
                    lines += run([filepath])

            except: 
                errors += 1
                continue 

    return files, lines, errors

maxi_root = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/'
qpo_ml_root = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/'
lines, files, errors = np.array(get_count(maxi_root))+np.array(get_count(qpo_ml_root))

print(lines, files, errors)