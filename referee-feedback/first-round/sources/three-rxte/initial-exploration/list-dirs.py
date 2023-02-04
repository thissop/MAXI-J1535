import os 

dirs = ['/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/groj1655_pds',
        '/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/gx339_pds',
        '/Users/yaroslav/Documents/Research/Steiner/Data/thaddaeus_bundle/xtej1550_pds']

for dir in dirs: 
    files = list(os.listdir(dir))
    print(dir.split('/')[0], len(files))