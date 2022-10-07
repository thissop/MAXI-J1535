import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor

import warnings
warnings.filterwarnings("ignore")

wh1 = True

if wh1: 
    plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
else: 
    plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

sns.set_context("paper") #font_scale=
sns.set_palette('deep')
seaborn_colors = sns.color_palette('deep')

plt.rcParams['font.family'] = 'serif'
plt.rcParams["mathtext.fontset"] = "dejavuserif"

#bi_cm = LinearSegmentedColormap.from_list("Custom", [seaborn_colors[0], (1,1,1), seaborn_colors[3]], N=20)

def regression_pipeline(source:str, models:list, model_names:list,
                        qpo_path:str, context_path:str, repository_path:str,
                        qpo_preprocess_dict:dict, context_preprocess_dict:dict,
                        model_hyperparameter_dictionaries:list,spectrum:bool=False,
                        model_comparison_statistic:str='mae', k:int=10, repetitions:int=2, fold:int=0, wh1=wh1,
                        units:dict={'frequency':'Hz'}):

    r''' 
    model_comparison_statistic : str
        either 'mae' or 'mse' 

    '''

    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml.new_main import collection
    from qpoml.plotting import plot_model_comparison
    from qpoml.utilities import pairwise_compare_models

    #plt.rcParams["mathtext.fontset"] = "dejavuserif"
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')

    # 1: Preparation for Pipeline # 

    model_n = len(models)

    all_gridsearch_scores = []
    source_observation_counts = []

    alphabet = [str(chr(letter)).upper() for letter in range(97,123)] 

    if repository_path[-1]!='/':
        repository_path!='/'

    qpo_path = f'{repository_path}{qpo_path}' 
    context_path = f'{repository_path}{context_path}'

    # 2: Source-wise Machine Learning #

    n_total_qpos = len(pd.read_csv(qpo_path).index)
    n_test = int(n_total_qpos/k)
    n_train = n_total_qpos-n_test

    fold_performances = []
    gridsearch_scores = []

    # 2.1: Machine Learning for Each Model # 

    for model_index, model in enumerate(models):

        model_name = model_names[model_index]

        notation_string = f'[{model_name}][{source}][{spectrum}]'

        collec = collection()

        collec.load(qpo_csv=qpo_path, context_csv=context_path,
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

        # 2.1.1: GridSearch # 

        scores, _, _, best_params = collec.gridsearch(model=model, parameters=model_hyperparameter_dictionaries[model_index])

        column_names = list(best_params.keys())
        columns = [[i] for i in list(best_params.values())]

        best_configuration_df = pd.DataFrame()

        for temp_index in range(len(column_names)):
            best_configuration_df[column_names[temp_index]] = columns[temp_index]

        if source.replace('_',' ') == 'GRS 1915+905': 
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/GRS_1915+105/{notation_string}_BestParams.csv', index=False)
        else: 
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}_BestParams.csv', index=False)
        
        # 2.1.2: k-fold on Best Configuration # 

        collec.evaluate(model=model, evaluation_approach='k-fold', folds=k, repetitions=repetitions, hyperparameter_dictionary=best_params) # evaluate-approach???

        # 2.1.3: Save and Plot Performance Across Folds # 

        statistics = collec.get_performance_statistics()

        fold_performance_df = pd.DataFrame.from_dict(statistics)
        fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
        if source.replace('_',' ') == 'GRS 1915+905': 
            temp_path = f'{repository_path}final-push/output/pipeline/GRS_1915+105/{notation_string}_k-fold.csv'
        else: 
            temp_path = f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}_k-fold.csv'
        
        fold_performance_df.to_csv(temp_path, index=False)

        fold_performances.append(list(fold_performance_df[model_comparison_statistic]))

        # 2.1.4: Plot Results Regression from 10th Fold # 
        sns.set_context(font_scale=1.15)
        fig, ax = plt.subplots(figsize=(4,4))

        collec.plot_results_regression(feature_name='frequency', which=[0], ax = ax, fold=fold)
        temp_path = f'{repository_path}manuscript/figures/individual/figure_6/{notation_string}[results_regression][fold={fold}]'
        plt.savefig(f'{temp_path}.pdf')
        plt.savefig(f'{temp_path}.png', dpi=200)
        plt.close()

        # 2.1.5: Plot Feature Importances from fold-th Fold # 
        fig, ax = plt.subplots(figsize=(6,6))
        
        collec.plot_feature_importances(model=model, fold=fold, kind='tree-shap', style='box', ax=ax)
        
        temp_path = None 

        if source.replace('_',' ') == 'GRS 1915+105':
            temp_path = f'{repository_path}manuscript/figures/individual/figure_8/{notation_string}[feature_importances][fold={fold}]'
        else: 
            temp_path = f'{repository_path}manuscript/figures/individual/figure_9/{notation_string}[feature_importances][fold={fold}]'    
        
        plt.savefig(f'{temp_path}.pdf')
        plt.savefig(f'{temp_path}.png', dpi=200)
        plt.close()

    # 2.2: All-Models One Source Results # 

    # 2.2.1: Plot Performances for all Models #
    fig, ax = plt.subplots()
    print(model_names, len(fold_performances))
    plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax, cut=0)
    temp_path = f'{repository_path}manuscript/figures/individual/figure_4/[{source}][{spectrum}][model-comparison]'
    plt.savefig(f'{temp_path}.pdf') 
    plt.savefig(f'{temp_path}.png', dpi=200) 
    plt.close()
    
    # ignore
    sns.set_context(font_scale=0.7)
    fig, ax = plt.subplots()
    print(model_names, len(fold_performances))
    plot_model_comparison(model_names=model_names, performance_lists=fold_performances, style='violin', ax=ax)
    temp_path = f'{repository_path}manuscript/figures/individual/figure_4/[{source}][{spectrum}][model_comparison:no-cut]'
    plt.savefig(f'{temp_path}.pdf') 
    plt.savefig(f'{temp_path}.png', dpi=200) 
    plt.close()

    sns.set_context(font_scale=1)
    # 2.2.2: Pairwise Statistical Model Comparison # 

    temp_path = f'{repository_path}manuscript/tables/[{source}][{spectrum}][comparison_table]'

    pairwise_compare_models(model_names=model_names, model_score_arrays=fold_performances, n_train=n_train, n_test=n_test, save_dir=None, save_path=temp_path)

def classification_pipeline(source:str, models:list, model_names:list,repository_path:str,
                            context_path:str, qpo_path:str, 
                            model_hyperparameter_dictionaries:list,
                            context_preprocess_dictionary:dict, wh1=wh1, fold:int=0,
                            k:int=10, repetitions:int=2, spectrum:bool=False, 
                            additional_info=None): 
    
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml import collection
    from qpoml.utilities import roc_and_auc
    from qpoml.plotting import plot_roc

    # 1. Preparation for Pipeline #
    
    all_gridsearch_scores = []
    source_observation_counts = []

    if repository_path[-1]!='/':
        repository_path+='/'
    
    qpo_path = f'{repository_path}{qpo_path}' 
    context_path = f'{repository_path}{context_path}'

    # 2: Source-wise Machine Learning #

    n_total_qpos = len(pd.read_csv(qpo_path).index)
    print('Number of QPOs:', n_total_qpos)

    gridsearch_scores = []

    # MAKE GRID SEARCH SCORES PLOT? # 

    source_observation_counts.append(len(pd.read_csv(context_path).index))
    print('Source Observation Counts', source_observation_counts)

    for model_index, model in enumerate(models):

        model_name = model_names[model_index]

        notation_string = f'[{model_name}][{source}][{spectrum}]'
        if additional_info is not None: 
            for i, j in zip(list(additional_info.keys()), list(additional_info.values())):
                notation_string+=f'[{i}:{j}]'

        collec = collection()
        collec.load(qpo_csv=qpo_path, context_csv=context_path, context_preprocess=context_preprocess_dictionary, approach='classification', units={'frequency':'hz'})
        
        scores, _, _, best_params = collec.gridsearch(model=model, parameters=model_hyperparameter_dictionaries[model_index])

        column_names = list(best_params.keys())
        columns = [[i] for i in list(best_params.values())]

        best_configuration_df = pd.DataFrame()

        for temp_index in range(len(column_names)):
            best_configuration_df[column_names[temp_index]] = columns[temp_index]

        if source.replace('_',' ') == 'MAXI J1535-571':
            best_configuration_df.to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}[BestParams].csv', index=False)
        gridsearch_scores.append(scores)
        
        collec.evaluate(model=model, evaluation_approach='k-fold', folds=k, stratify=True, repetitions=repetitions, hyperparameter_dictionary=best_params)

        # .1 Confusion Matrix # 


        if wh1: 
            plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
        else: 
            plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')

        sns.set_context('paper', font_scale=1.4)
        fig, ax = plt.subplots(figsize=(4,4))
        y_set = list(set(np.array(collec.y_test).flatten()))
        cm_labels = None
        cm_type = None
        if len(y_set) == 2:
            labels = ['No QPO', 'QPO']
            cm_type = 'binary'

        else: 
            labels = [f'{counter} QPO' for counter in y_set]
            cm_type = 'multinomial'

        collec.plot_confusion_matrix(fold=fold, ax=ax, labels=labels)

        cm_path = f'{repository_path}manuscript/figures/individual/figure_7/{notation_string}[confusion_matrix-type={cm_type}]'
        fig.tight_layout()
        plt.savefig(f'{cm_path}.pdf')
        plt.savefig(f'{cm_path}.png', dpi=200)

        plt.clf()
        plt.close()

        sns.set_context(font_scale=1)

        # .2 ROC Curve # 
        if cm_type == 'binary':
            fig, ax = plt.subplots(figsize=(4,4))
            if wh1: 
                plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
            else: 
                plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
            sns.set_context('paper')
            fpr, tpr, std_tpr, auc, std_auc = collec.roc_and_auc()
            plot_roc(fpr=fpr, tpr=tpr, std_tpr=std_tpr, auc=auc, ax=ax, std_auc=std_auc)

            roc_path = f'{repository_path}manuscript/figures/individual/figure_7/{notation_string}[ROC]'
            fig.tight_layout()
            plt.savefig(f'{roc_path}.pdf')
            plt.savefig(f'{roc_path}.png', dpi=200)

        # .3 Feature Importances # 

        fig, ax = plt.subplots(figsize=(4,4))
        if wh1: 
            plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
        else: 
            plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
        
        sns.set_context('paper')
        collec.plot_feature_importances(model, fold=fold, style='box', ax=ax, kind='tree-shap')
        fi_path = f'{repository_path}manuscript/figures/individual/figure_9/{notation_string}[Feature-Importances]'
        fig.tight_layout()
        plt.savefig(f'{fi_path}.pdf')
        plt.savefig(f'{fi_path}.png', dpi=200)

        # save predictions, etc. 
        statistics = pd.DataFrame(collec.get_performance_statistics())
        if source.replace('_',' ') == 'MAXI J1535-571':
            pd.DataFrame(statistics).to_csv(f'{repository_path}final-push/output/pipeline/MAXI_J1535-571/{notation_string}[Performance_stats].csv', index=False)

model_hyperparameter_dictionaries = [{'normalize':[True, False]},
                                     {'min_samples_split':[4,6], 'min_samples_leaf':[3]}, 
                                     {'min_samples_split': [4,6], 'min_samples_leaf':[1]},
                                     {'min_samples_split':[4,6], 'min_samples_leaf':[1]}, 
                                     {'n_estimators':[500,1000], 'eta':[0.1]}]
# SHARE DICTIONARIES # 

maxi_spectrum_context_preprocess = dict(zip([f'rebin_channel_{i}' for i in range(19)], 19*['normalize']))

# ROUND ONE: GRS REGRESSION # 
print('starting round one')

regression_pipeline(source='GRS_1915+905', 
                    models=[LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor(), ExtraTreesRegressor()],#, XGBRegressor()], 
                    model_names=['Linear', 'DT', 'RF', 'ET', 'XGBoost'], 
                    qpo_path='final-push/data/pipeline/GRS/GRS_1915+105_QPO-Input.csv', 
                    context_path='final-push/data/pipeline/GRS/GRS_1915+105_Scalar-Input.csv', 
                    qpo_preprocess_dict={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}, 
                    context_preprocess_dict={'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}, 
                    model_hyperparameter_dictionaries=model_hyperparameter_dictionaries,
                    repository_path='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/')

# ROUND TWO: MAXI REGRESSION, SCALAR INPUT 
print('starting round two')

regression_pipeline(source='MAXI_J1535-571', 
                    models=[LinearRegression(), DecisionTreeRegressor()],#, RandomForestRegressor(), ExtraTreesRegressor(), XGBRegressor()], 
                    model_names=['Linear', 'DT', 'RF', 'ET', 'XGBoost'], 
                    qpo_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_QPO_regression.csv', 
                    context_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_Scalar-Input.csv', 
                    qpo_preprocess_dict={'frequency':'normalize','width':'normalize','normalization':'normalize'}, 
                    context_preprocess_dict={'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'}, 
                    model_hyperparameter_dictionaries=model_hyperparameter_dictionaries,
                    repository_path='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/')

# ROUND THREE: MAXI REGRESSION, SPECTRUM INPUT 
print('starting round three')

regression_pipeline(source='MAXI_J1535-571', 
                    models=[LinearRegression(), DecisionTreeRegressor()],#, RandomForestRegressor(), ExtraTreesRegressor(), XGBRegressor()], 
                    model_names=['Linear', 'DT', 'RF', 'ET', 'XGBoost'], 
                    qpo_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_QPO_regression.csv', 
                    context_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_Rebin-Spectra.csv', 
                    qpo_preprocess_dict={'frequency':'normalize','width':'normalize','normalization':'normalize'}, 
                    context_preprocess_dict=maxi_spectrum_context_preprocess, 
                    model_hyperparameter_dictionaries=model_hyperparameter_dictionaries,
                    spectrum=True,
                    repository_path='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/')

# ROUND FOUR: MAXI CLASSIFICATION, SCALAR INPUT, BINARY
print('starting round four')

classification_pipeline(source='MAXI_J1535-571', 
                        models=[RandomForestClassifier(), LogisticRegression()], 
                        model_names=['Random Forest', 'Logistic Regression'], 
                        context_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_Scalar-Input.csv', 
                        qpo_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_QPO-Input.csv',
                        model_hyperparameter_dictionaries=[{'n_estimators':[50,100,200]}, 
                                                           {'penalty':['l2'], 'C':[1, 5]}], 
                        context_preprocess_dictionary={'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'},
                        repository_path='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/')

# ROUND FIVE: MAXI CLASSIFICATION, SPECTRUM INPUT, BINARY
print('starting round five')

classification_pipeline(source='MAXI_J1535-571', 
                        models=[RandomForestClassifier(), LogisticRegression()], 
                        model_names=['Random Forest', 'Logistic Regression'], 
                        context_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_Rebin-Spectra.csv', 
                        qpo_path='final-push/data/pipeline/MAXI/MAXI_J1535-571_QPO-Input.csv',
                        model_hyperparameter_dictionaries=[{'n_estimators':[50,100,200]}, 
                                                           {'penalty':['l2'], 'C':[1, 5]}], 
                        context_preprocess_dictionary=maxi_spectrum_context_preprocess,
                        spectrum=True,
                        repository_path='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/')