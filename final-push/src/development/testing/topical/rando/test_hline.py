import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt 
import seaborn as sns

collec = collection()

qpo_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'
context_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
units = {'frequency':'Hz'}

collec.load(qpo_csv=qpo_path, context_csv=context_path, context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=10)

plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
fig, ax = plt.subplots(figsize=(4,4))

sns.set_context('paper')
collec.plot_feature_importances(RandomForestRegressor(), fold=9, style='bar', ax=ax, kind='tree-shap', median_hline=True)
fig.tight_layout()

plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/development/testing/topical/rando/test_hline.png', dpi=200) 
plt.close()