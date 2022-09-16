from random import Random
import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

from sklearn.linear_model import LinearRegression

from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor

from qpoml.utilities import unprocess1d

import matplotlib.pyplot as plt 
import seaborn as sns

from qpoml.plotting import plot_model_comparison


models = [LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor(), ExtraTreesRegressor(), XGBRegressor()]
model_names = ['Linear', 'DT', 'RF', 'ET', 'XGBoost']

fold_performances = []

for model in models: 

    collec = collection()

    qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv'
    context_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'

    context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
    qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
    units = {'frequency':'Hz'}

    collec.load(qpo_csv=qpo_path, context_csv=context_path, context_type='scalar',  
                        context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

    collec.evaluate(model=model, evaluation_approach='k-fold', folds=10)

    statistics = collec.get_performance_statistics()

    fold_performance_df = pd.DataFrame.from_dict(statistics)
    fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
   
    fold_performances.append(list(fold_performance_df['mae']))

fig, ax = plt.subplots()
plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax, cut=0)

fig.tight_layout()

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_violin_figure/plot.png', dpi=200) 
plt.close()