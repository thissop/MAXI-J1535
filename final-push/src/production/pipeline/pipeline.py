def pipeline(sources:list, 
             input_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline', 
             output_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/output/pipeline',
             figure_output_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures'):

    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt 
    from qpoml import collection
    from sklearn.ensemble import RandomForestRegressor as RF

    plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')

    # STEP ZERO: PRE-PIPELINE CHECKS # 

    n = len(sources)

    if input_directory[-1]!='/':
        input_directory+='/'

    if output_directory[-1]!='/':
        output_directory+='/'

    if figure_output_directory[-1]!='/': 
        figure_output_directory+='/'

    source_directories = [figure_output_directory+source+'/' for source in sources]
    for source_directory in source_directories:
        if not os.path.exists(source_directory):
            os.mkdir(source_directory)

    # STEP 1: MAKE COMBINED NET COUNTS FIGURE # 

    temp_MJDs = []
    temp_NCRs = [] # NetCountRates

    for source in sources: 
        context_df = pd.read_csv(input_directory+source+'_context.txt')
        spectral_df = pd.read_csv(input_directory+source+'_spectral_for_qpoml.txt')

        temp_df = context_df.merge(spectral_df, on='observation_ID')
        temp_MJDs.append(np.array(temp_df['MJD']))
        NCRs = np.array(temp_df['net_count_rate'])/np.median(temp_df['net_count_rate'])
        temp_NCRs.append(NCRs)
    
    if n>1: 
        fig, axs = plt.subplots(n, 1, figsize=(6,2*n))

        for i in range(n):
            ax = axs[i] 
            ax.scatter(temp_MJDs[i], temp_NCRs[i], s=2)
            
        fig.supylabel('Normalized Count Rate') # Source-Wise Median Normalized Net Count Rate
        fig.supxlabel('Date (MJD)')

    else: 
        fig, ax = plt.subplots(figsize=(6,2))
        ax.scatter(temp_MJDs[0], temp_NCRs[0], s=2)
        ax.set(ylabel='Normalized Count Rate', xlabel='Date (MJD)')
        ax.xaxis.set_ticklabels([])

    plt.subplots_adjust(hspace=0)
    plt.tight_layout()
    plt.savefig(figure_output_directory+'stacked_NCRs.pdf')
    plt.savefig(figure_output_directory+'stacked_NCRs.png', dpi=150)
    plt.clf()
    plt.close()

    # STEP 2: DO MACHINE LEARNING FOR EACH #

    for source_idx, source in sources: 
        source_directory = source_directories[source_idx]

        spectrum_context = './research and development/example_spectrum.csv'
        scalar_context = './research and development/example_scalar.csv'
        qpo = './research and development/example_qpo.csv'
        order_qpo = './research and development/example_qpo_order.csv'

        qpo_preprocess = {'frequency':[0.01,20], 'width':[0.001,4], 'amplitude':[0.001, 5]}

        qpo_csv = './qpoml/tests/references/fake_generated_qpos.csv'
        scalar_collection_csv = './qpoml/tests/references/fake_generated_scalar_context_with_categorical.csv'

        for regr, regr_name in zip([RF], ['RandomForest']):
            
            collec= collection()
            context_dict = {'gamma':[1.0,3.5],'T_in':[0.1,2.5],'qpo_class':'categorical'}
            collec.load(qpo_csv=qpo_csv, context_csv=scalar_collection_csv, context_type='scalar', context_preprocess=context_dict, 
                                qpo_preprocess={'frequency':[1,16], 'width':[0.1,1.6], 'amplitude':[1,6]}, qpo_approach='single')

            #collec.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=5, repetitions=4)

            random_forest_params = {'n_estimators':[100,200], 'min_samples_split':[2,3,4]}
            best_configuration, _, _ = collec.grid_search(model=regr, parameters=random_forest_params)

            with open('./qpoml/tests/outputs/grid_search_best_model.txt', 'w') as f: 
                f.write(','.join(best_configuration.keys())+'\n')
                f.write(','.join(best_configuration.values())+'\n')

            # FIX ^^^ so it actually saves and so you can use the best parameters below! 

            # Run model on best configuration from Grid Search # 
            collec.evaluate(model=regr, model_name='RandomForest', evaluation_approach='k-fold', folds=10)

            # FIX ^^^ so it takes into account reps as arg, as well as model kwargs! 

            # Save repeated k-fold mae/mse values for latter statistical test 

            statistics = collec.get_performance_statistics()

            fold_performance_df = pd.DataFrame.from_dict(statistics)
            fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
            temp_path = f'{output_directory}' # FIX THIS SO THAT IT saves all to same output dir, but calls source plot dirs differently!
            # maybe save different logs to csvs together in purpuse-unique folder
            fold_performance_df.to_csv(temp_path, index=False)

            # 2.1.1: Results Regression from 10th Fold # 
            fig, ax = plt.subplots(figsize=(4,4))
            collec.plot_results_regression(feature_name='frequency', which=[0], ax = ax, fold=9)
            temp_path = f'{source_directory}results-regression_fold={9}_model={regr_name}'
            plt.savefig(f'{temp_path}.pdf')
            plt.savefig(f'{temp_path}.png', dpi=200)
            plt.clf()
            plt.close()

            # 2.1.2: Feature Importances from 10th Fold # 
            fig, ax = plt.subplots(figsize=(6,6))
            collec.plot_feature_importances(model=regr, fold=9, kind='tree-shap', style='errorbar', ax=ax)
            temp_path = f'{source_directory}feature-importances_fold={9}_model={regr_name}'
            plt.savefig(f'{temp_path}.pdf')
            plt.savefig(f'{temp_path}.png', dpi=200)
            plt.clf()
            plt.close()



        # STEP 2.1: RUN GRID-SEARCH #   
        # for regressor in regressor: 
            # save grid search results

        # run k-fold with best 

pipeline(sources=['GRS_1915+105'])