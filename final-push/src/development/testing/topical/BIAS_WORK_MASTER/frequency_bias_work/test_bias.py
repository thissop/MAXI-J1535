from random import Random
import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

from qpoml.utilities import unprocess1d

import matplotlib.pyplot as plt 

collec = collection()

qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv'
context_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
units = {'frequency':'Hz'}

collec.load(qpo_csv=qpo_path, context_csv=context_path, context_type='scalar',  
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=10)

qpo_preprocess1d_tuples = collec.qpo_preprocess1d_tuples

predictions, y_test = (np.transpose(collec.predictions[0]), np.transpose(collec.y_test[0]))
keys = ['frequency', 'width', 'rms']

i,j,k = [np.abs(unprocess1d(predictions[i], qpo_preprocess1d_tuples[keys[i]])-unprocess1d(y_test[i], qpo_preprocess1d_tuples[keys[i]])) for i in range(3)]
diffs = [i,j,k]

names = ['freq', 'width', 'amps']


fig, axs = plt.subplots(1,2, figsize=(6,3))

for i in range(len(names)): 
    diff = diffs[i]
    axs[0].hist(diff, label=f'{names[i]} (mean: {round(np.mean(diff), 2)}; std: {round(np.std(diff), 3)})', alpha=0.4)

    axs[1].errorbar([i], [np.mean(diff)], yerr=[np.std(diff)], label=names[i])
    axs[1].scatter([i], [np.mean(diff)], s=4)

axs[0].legend()
axs[0].set(xlabel='Absolute Normalized Difference', ylabel='Count')
axs[1].legend()
axs[1].set(ylabel='Absolute Normalized Difference')

fig.tight_layout()

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/frequency_bias_work/test_bias.png', dpi=200)