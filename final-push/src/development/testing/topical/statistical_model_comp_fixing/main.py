from random import Random
import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from qpoml.utilities import compare_models, pairwise_compare_models
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from qpoml.utilities import unprocess1d

import matplotlib.pyplot as plt 

models = [LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor(), ExtraTreesRegressor(), XGBRegressor()]
model_names = ['Linear', 'DT', 'RF', 'ET', 'XGBoost']
fold_performances = []

model_n = len(models)

alphabet = [str(chr(letter)).upper() for letter in range(97,123)] 

qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv'
context_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'

n_total_qpos = len(pd.read_csv(qpo_path).index)
n_test = int(n_total_qpos/5)
n_train = n_total_qpos-n_test

for model, model_name in zip(models, model_names):

    collec = collection()

    qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv'
    context_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'

    context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
    qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
    units = {'frequency':'Hz'}

    collec.load(qpo_csv=qpo_path, context_csv=context_path, context_type='scalar',  
                        context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

    collec.evaluate(model=model, evaluation_approach='k-fold', folds=5)

    statistics = collec.get_performance_statistics()

    fold_performance_df = pd.DataFrame.from_dict(statistics)
    fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]

    fold_performances.append(list(fold_performance_df['mae']))

print(fold_performances)

save_dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/statistical_model_comp_fixing/'

pairwise_compare_models(model_names, model_score_arrays=fold_performances, n_train=n_train, n_test=n_test, save_dir=save_dir)




