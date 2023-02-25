def run_pipeline(pipeline_output_dir:str='/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/referee-feedback/first-round/updated-pipeline/output'): 

    import os
    import time 
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt 
    import seaborn as sns
    from qpoml.main import collection 
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor
    from sklearn.linear_model import LogisticRegression, LinearRegression

    from xgboost import XGBRegressor
    from sklearn.tree import DecisionTreeRegressor

    import warnings
    warnings.filterwarnings("ignore")

    wh1 = True

    if wh1: 
        plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')

    sns.set_context("paper") #font_scale=
    sns.set_palette('deep')
    seaborn_colors = sns.color_palette('deep')

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams["mathtext.fontset"] = "dejavuserif"

    output_dirs = []
    for output_dir in ['maxi_solo/spectrum_input_regression',
                       'maxi_solo/feature_input_regression', 
                       'maxi_solo/spectrum_input_binary_classification',
                       'maxi_solo/feature_input_binary_classification',
                       'maxi_solo/spectrum_input_multiclass_classification',
                       'maxi_solo/feature_input_multiclass_classification',
                       'grs_solo/feature_input_regression',
                       'mixed/feature_input_regression']:
        
        output_dir = os.path.join(pipeline_output_dir, output_dir)
        output_dirs.append(output_dir)
        if not os.path.exists(output_dir): 
            os.mkdir(output_dir)

    def run_classification(input_type:str, input_data_csv, output_data_csv, output_dir, multiclass:bool): 
        from qpoml.plotting import plot_roc

        classification_models = [RandomForestClassifier(), LogisticRegression()]
        classification_model_names = ['RandomForest', 'LogisticRegression']
        
        class_gridsearch_dictionaries  = [{'n_estimators': [50,100,150,200, 250, 500], 'min_samples_split': [2,4,6,8], 'min_samples_leaf': [1,3]}, {'C':[1,3,5]}]
        
        plot_dir = os.path.join(output_dir, 'plots')
        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)

        if input_type == 'spectrum': 
            context_preprocess = dict(zip([str(i) for i in range(19)], ['normalize' for i in range(19)]))
        elif input_type == 'features':
            context_preprocess = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'}

        for model, model_name, model_gridsearch_dictionary in zip(classification_models, classification_model_names, class_gridsearch_dictionaries):
            
            collec = collection(random_state=21)
            collec.load(context_csv=input_data_csv, qpo_csv=output_data_csv,
                        context_preprocess=context_preprocess, 
                        approach='classification', units={'frequency':'Hz'})

            collec.evaluate(model=model, folds=10, repetitions=1, gridsearch_dictionary=model_gridsearch_dictionary, stratify=True, multiclass=multiclass)

            # PLOTTING 

            # 1. Confusion Matrices 

            fig, ax = plt.subplots(figsize=(4,4))

            collec.plot_confusion_matrix(ax=ax)
            plt.savefig(os.path.join(plot_dir, f'[confusion-matrix][{model_name}].pdf'))
            plt.close()

            # 2. Feature Importances 

            fig, ax = plt.subplots(figsize=(4,4))

            collec.plot_feature_importances(model=model, ax=ax, hline=True)
            plt.savefig(os.path.join(plot_dir, f'[feature-importances][{model_name}].pdf'))
            plt.close()

            # 3. ROC and AUC 

            if not multiclass: 

                fig, ax = plt.subplots(figsize=(4,4))

                plot_roc(fpr=np.mean(collec.FPRs, axis=0), tpr=np.mean(collec.TPRs, axis=0), std_tpr=np.std(collec.TPRs, axis=0), auc=np.mean(collec.auc_scores), ax=ax, std_auc=np.std(collec.auc_scores))
                plt.savefig(os.path.join(plot_dir, f'[roc-auc][{model_name}].pdf'))
                plt.close()

    def run_regression(input_type:str, input_data_csv, output_data_csv, output_dir): 
        from qpoml.plotting import plot_model_comparison
        from qpoml.utilities import pairwise_compare_models
        
        regression_models = [ExtraTreesRegressor(), LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor()]#, XGBRegressor()]
        regression_model_names = ['ExtraTreesRegressor','LinearRegression', 'DecisionTreeRegressor', 'RandomForestRegressor']#, 'XGBRegressor']
        reg_model_names_short = ['ET', 'Linear', 'DT', 'RF']#, 'XGBoost']
        
        #'''
        regression_gridsearch_dictionaries = [
                                            {'n_estimators': [50,100,150,200,250,500], 'min_samples_split': [2,4,6,8], 'min_samples_leaf': [1,3,5]},
                                            {'fit_intercept':[True]},
                                            {'min_samples_split': [2,4,6,8], 'min_samples_leaf': [1,3]}, 
                                            {'warm_start':[True, False], 'n_estimators': [50,100,150,200,250,500], 'min_samples_split': [2,4,6,8], 'min_samples_leaf': [1,3,5]},
                                            #{'alpha':[0,0.25,0.5,0.75],'eta':[0.1, 0.5, 0.9],'max_depth':[3, 6 ,9],'n_estimators':[100]}
                                            ]
        #'''
        
        '''
        regression_gridsearch_dictionaries = [{'fit_intercept':[True]},
                                            {'min_samples_split': [2,4,6,8], 'min_samples_leaf': [1,3]}, 
                                            {'n_estimators': [50,100], 'min_samples_split': [2], 'min_samples_leaf': [3]},
                                            {'n_estimators': [50,100], 'min_samples_split': [2], 'min_samples_leaf': [3]}, 
                                            {'alpha':[0,0.25],'eta':[0.1],'max_depth':[3],'n_estimators':[100]}
                                            ]
        '''

        plot_dir = os.path.join(output_dir, 'plots')
        if not os.path.exists(plot_dir):
            os.mkdir(plot_dir)

        analysis_dir = os.path.join(output_dir, 'output')
        if not os.path.exists(analysis_dir):
            os.mkdir(analysis_dir)

        fold_performances = []
        gridsearch_scores = []

        test_n = None 
        train_n = None

        if input_type == 'spectrum': 
            context_preprocess = dict(zip([str(i) for i in range(19)], ['normalize' for i in range(19)]))
        elif input_type == 'features':
            context_preprocess = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'}

        test_ids = []
        train_ids = []

        for model, model_name, model_gridsearch_dictionary in zip(regression_models, regression_model_names, regression_gridsearch_dictionaries):
            
            collec = collection(random_state=21)
            collec.load(context_csv=input_data_csv, qpo_csv=output_data_csv,
                        context_preprocess=context_preprocess, 
                        qpo_preprocess={'frequency':'normalize','width':'normalize','norm':'normalize'}, 
                        approach='regression', units={'frequency':'Hz'})

            collec.evaluate(model=model, folds=10, repetitions=1, gridsearch_dictionary=model_gridsearch_dictionary, stratify=True)
            
            gridsearch_scores.append(collec.gridsearch_scores)
            fold_performances.append(collec.fold_performances)

            test_n = len(collec.test_observation_IDs)
            train_n = len(collec.train_observation_IDs)

            best_params_df = pd.DataFrame()

            best_params = collec.best_params 
            for param, param_val in zip(best_params.keys(), best_params.values()): 
                best_params_df[param] = [param_val]

            best_params_df.to_csv(os.path.join(analysis_dir, f'[{model_name}][best-params].csv'), index=False)

            train_ids = collec.train_observation_IDs
            test_ids = collec.test_observation_IDs


            # PLOTTING 

            # 1. Results Regression 

            fig, ax = plt.subplots(figsize=(4,4))

            collec.plot_results_regression('frequency', which=[0,1], ax=ax)
            plt.savefig(os.path.join(plot_dir, f'[frequency-results-regression][{model_name}].pdf'))
            plt.close()

            # 2. Feature Importances 

            try: 
                fig, ax = plt.subplots(figsize=(4,4))

                collec.plot_feature_importances(model=model, ax=ax, hline=True)
                plt.savefig(os.path.join(plot_dir, f'[feature-importances][{model_name}].pdf'))
                plt.close()

            except: 
                pass 

        # 3. Model Comparison

        fig, ax = plt.subplots(figsize=(5,4))

        plot_model_comparison(model_names=reg_model_names_short, performance_lists=fold_performances, style='violin', ax=ax, cut=0)
        plt.savefig(os.path.join(plot_dir, f'[models-comparisons].pdf'))

        # 4. Gridsearch Scores

        fig, ax = plt.subplots(figsize=(4,2))
        gridsearch_x = [list(range(0, len(i))) for i in gridsearch_scores]
        
        for i, x, y in zip(range(0, len(gridsearch_x)), gridsearch_x, gridsearch_scores):
            ax.plot(x, np.sort(y), label=reg_model_names_short[i])
        
        ax.legend()
        ax.set(xlabel='Hyperparameter Combination', ylabel='Median Absolute Error')
        plt.savefig(os.path.join(plot_dir, f'[gridsearch].pdf'))
        plt.close()

        # 5. Statistical Difference Testing 

        pairwise_compare_models(model_names=regression_model_names, model_score_arrays=fold_performances, 
                                n_train=train_n, n_test=test_n, save_dir=analysis_dir)

        # 6. Save IDs 
        
        grs_test_percent = 100*len([i for i in test_ids if '-' in i])/len(test_ids)
        grs_train_percent = 100*len([i for i in train_ids if '-' in i])/len(train_ids)
        with open(os.path.join(analysis_dir, 'IDs-split.txt'), 'w') as f: 
            f.write(f'Test IDs: (GRS: {round(grs_test_percent, 2)} %)'+','.join(test_ids)+'\n')
            f.write(f'Train IDs: (GRS: {round(grs_train_percent, 2)} %)'+','.join(train_ids)+'\n')

    # 1. MAXI SOLO  
    
    '''
    # 1.a. SPECTRUM INPUT REGRESSION
    print('1.a')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[energy-spectra][rebin-regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][two-feature-regression].csv'
    output_dir = output_dirs[0]
    run_regression('spectrum', input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir)

    # 1.b. FEATURES INPUT REGRESSION
    print('1.b.')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][two-feature-regression].csv'
    output_dir = output_dirs[1]
    run_regression('features', input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir)

    # 1.c. SPECTRUM INPUT BINARY CLASSIFICATION 
    print('1.c.')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[energy-spectra][rebin-regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][binary].csv'
    output_dir = output_dirs[2]
    run_classification('spectrum', input_data_csv=input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir, multiclass=False)

    # 1.d. FEATURES INPUT BINARY CLASSIFICATION 
    print('1.d.')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][binary].csv'
    output_dir = output_dirs[3]
    run_classification('features', input_data_csv=input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir, multiclass=False)

    # 1.e. SPECTRUM INPUT MULTICLASS CLASSIFICATION 
    print('1.e')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[energy-spectra][rebin-regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][multiclass].csv'
    output_dir = output_dirs[4]
    run_classification('spectrum', input_data_csv=input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir, multiclass=True)
    
    # 1.f. FEATURES INPUT MUILTICLASS CLASSIFICATION 
    print('1.f.')
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv'
    output_data_csv =  '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][multiclass].csv'
    output_dir = output_dirs[5]
    run_classification('features', input_data_csv=input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir, multiclass=True)

    
    # 2. GRS SOLO 
    
    # 2.a. FEATURES INPUT REGRESSION 
    print('2.a.')
    output_dir = output_dirs[-2]
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'
    output_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'
    run_regression('features', input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir)

    # 3. MIXED 

    # 3.a. FEATURES INPUT REGRESSION
    '''
    print('3.a.')
    output_dir = output_dirs[-1]
    input_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/blended/input-data.csv'
    output_data_csv = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/blended/output-data.csv'
    run_regression('features', input_data_csv, output_data_csv=output_data_csv, output_dir=output_dir)
    #'''

run_pipeline()