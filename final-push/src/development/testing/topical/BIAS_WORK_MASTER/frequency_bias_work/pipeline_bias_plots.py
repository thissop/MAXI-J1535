import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import seaborn as sns
from qpoml.utilities import unprocess1d

import matplotlib.pyplot as plt 

fold = 9
folds = 10

collec = collection()

qpo_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'
context_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
units = {'frequency':'Hz', 'width':'', 'rms':''}

collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=folds)

sns.set_context(font_scale=0.25)
fig, axs = plt.subplots(1,3, figsize=(6,2))
features = ['frequency', 'width', 'rms']
for i in range(3):
    ax = axs[i]
    collec.plot_results_regression(feature_name=features[i], which=[i], ax = ax, fold=fold, font_scale=0.75)

plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/development/testing/topical/BIAS_WORK_MASTER/frequency_bias_work/triple_results_regression.png', dpi=200)

quit()

qpo_preprocess1d_tuples = collec.qpo_preprocess1d_tuples

predictions, y_test = (np.transpose(collec.predictions[fold]), np.transpose(collec.y_test[fold]))
keys = ['frequency', 'width', 'rms']

i,j,k = [np.abs(unprocess1d(predictions[i], qpo_preprocess1d_tuples[keys[i]])-unprocess1d(y_test[i], qpo_preprocess1d_tuples[keys[i]])) for i in range(3)]
diffs = [i,j,k]

names = ['freq', 'width', 'amps']