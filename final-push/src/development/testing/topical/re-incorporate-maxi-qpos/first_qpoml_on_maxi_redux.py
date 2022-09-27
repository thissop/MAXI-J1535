import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from qpoml import collection 
import seaborn as sns
from sklearn.ensemble import ExtraTreesRegressor

qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/re-incorporate-maxi-qpos/test.csv'
context_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv'
context_preprocess = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
# fix to re-order QPOs!
qpo_labels = ['frequency','width','normalization']
qpo_preprocess = dict(zip(qpo_labels, len(qpo_labels)*['normalize']))

collec= collection()
collec.load(qpo_csv=qpo_path, context_csv=context_csv, context_type='scalar',  
            context_preprocess=context_preprocess, qpo_preprocess=qpo_preprocess, units={'frequency':'Hz'}, approach='regression') 

# 2.1.2: k-fold on Best Configuration # 

collec.evaluate(model=ExtraTreesRegressor(), evaluation_approach='k-fold', folds=10) # evaluate-approach???

predictions = np.transpose(collec.predictions[3])
y_test = np.transpose(collec.y_test[3])

labels = ['1st_freq', '1st_width', '1st_norm', '2nd_freq','2nd_width','2nd_norm']
fig, axs = plt.subplots(2,3, figsize=(6.1,3.05))
for i in range(2):
    for j in range(3):
        label = labels[i+j]
        ax = axs[i,j]
        ax.scatter(y_test[i+j], predictions[i+j])
        ax.set(xlim=(0,1.1), ylim=(0,1.1))
        ax.set_xlabel(f'True {label}', fontsize='xx-small')
        ax.set_ylabel(f'Predicted {label}', fontsize='xx-small')

fig.tight_layout()
plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/re-incorporate-maxi-qpos/comps.png', dpi=200)

for k in range(10):
    # 2.1.4: Plot Results Regression from 10th Fold # 
    fig, axs = plt.subplots(2,3, figsize=(6.1, 3.05))
    for i in range(2):
        for j in range(3):
            ax = axs[i, j]
            collec.plot_results_regression(feature_name='frequency', which=[i+j], ax = ax, fold=k)
    
    temp_path = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/re-incorporate-maxi-qpos/reg_results/'
    plt.savefig(f'{temp_path}results_regression-fold={k}.png', dpi=200)
    plt.close()