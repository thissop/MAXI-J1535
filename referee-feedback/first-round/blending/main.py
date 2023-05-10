from random import Random
import numpy as np 
import pandas as pd 
from qpoml import collection 
import os 
from sklearn.linear_model import LinearRegression

from xgboost import XGBRegressor

import matplotlib.pyplot as plt 
import seaborn as sns

from qpoml.plotting import plot_model_comparison

sns.set_context("paper") #font_scale=
sns.set_palette('deep')
seaborn_colors = sns.color_palette('deep')

plt.rcParams['font.family'] = 'serif'
plt.rcParams["mathtext.fontset"] = "dejavuserif"

models = [LinearRegression(), XGBRegressor()]
model_names = ['LinearRegression','XGBoost']

plot_dir = 'referee-feedback/first-round/blending/plots'
for fold in range(10):
    fold_performances = []






    for model, model_name in zip(models, model_names): 

        collec = collection()

        qpo_path = 'Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/output-data.csv'
        context_path = 'Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/input-data.csv'

        context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
        qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
        units = {'frequency':'Hz'}

        collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                            context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

        collec.evaluate(model=model, evaluation_approach='k-fold', folds=10)








        statistics = collec.get_performance_statistics()

        fold_performance_df = pd.DataFrame.from_dict(statistics)
        fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
    
        fold_performances.append(list(fold_performance_df['mae']))

        sns.set_context(font_scale=1.15)
        fig, ax = plt.subplots(figsize=(4,4))

        collec.plot_results_regression(feature_name='frequency', which=[0], ax = ax, fold=fold)
        plot_name = f'[{model_name}][results_regression][fold={fold}].png'
        plt.savefig(os.path.join(plot_dir, plot_name), dpi=200)
        plt.close()

        fig, ax = plt.subplots(figsize=(6,6))
            
        collec.plot_feature_importances(model=model, fold=fold, kind='tree-shap', style='bar', ax=ax, hline=True)
        plot_name = f'{model_name}[feature_importances][fold={fold}].png'
        plt.savefig(os.path.join(plot_dir, plot_name), dpi=200)
        plt.close()

    fig, ax = plt.subplots()
    plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax, cut=0)

    fig.tight_layout()

    plt.savefig(os.path.join(plot_dir, 'violin_plot.png'), dpi=200) 
    plt.close()