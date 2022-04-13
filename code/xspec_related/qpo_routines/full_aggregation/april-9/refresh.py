import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image


ids = []
thoughts = []

plt_dir = './code/xspec_related/qpo_routines/make_vetting_plots (old)/plots/'

df = pd.read_csv('./data/processed/2022/current_qpos.csv')

mask = np.where(df['confidence_class']==-1)[0]
def first(): 
    for id in df['full_id'][mask]: 
        
        im = Image.open(plt_dir+id+".png")

        plt.imshow(im)

        plt.show()

        ids.append(id)
        thoughts.append(input(id+': '))

        plt.clf()
        plt.close()

    with open('./code/xspec_related/qpo_routines/full_aggregation/april-9/temp.csv', 'w') as f: 
        f.write('id,thoughts/n')
        for i, j in zip(ids, thoughts): 
            f.write(str(i)+','+str(j)+'/n')

def second(): 
    for id in ['1050360111_6','1050360104_1','1050360105_21','1050360108_5',
    '1050360115_7']:
        im = Image.open(plt_dir+id+".png")

        

        plt.imshow(im)

        plt.show()

        plt.clf()
        plt.close()

        classif = input(id+': ')

second()