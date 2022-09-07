import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

sns.set_style('darkgrid')
plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')
sns.set_context("paper") #font_scale=
sns.set_palette('deep')
seaborn_colors = sns.color_palette('deep')

plt.rcParams['font.family'] = 'serif'
plt.rcParams["mathtext.fontset"] = "dejavuserif"

#bi_cm = LinearSegmentedColormap.from_list("Custom", [seaborn_colors[0], (1,1,1), seaborn_colors[3]], N=20)

def regression_pipeline(sources:list, models:list, model_names:list, source_classes:list, source_instruments:list,
             qpo_preprocess_dictionaries:dict, context_preprocess_dictionaries:list,
             model_hyperparameter_dictionaries:list,
             input_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline', 
             output_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/output/pipeline',
             manuscript_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/',
             model_comparison_statistic:str='mae', k:int=10, repetitions:int=2, 
             units:dict=None):

    r''' 
    model_comparison_statistic : str
        either 'mae' or 'mse' 

    '''

    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml import collection
    from qpoml.plotting import plot_model_comparison
    from qpoml.utilities import compare_models

    #plt.rcParams["mathtext.fontset"] = "dejavuserif"
    #plt.style.use('https://gist.githubusercontent.com/thissop/44b6f15f8f65533e3908c2d2cdf1c362/raw/fab353d758a3f7b8ed11891e27ae4492a3c1b559/science.mplstyle')

    # 1: Preparation for Pipeline # 

    n = len(sources)
    source_n = len(sources)
    model_n = len(models)

    if input_directory[-1]!='/':
        input_directory+='/'

    if output_directory[-1]!='/':
        output_directory+='/'

    if manuscript_directory[-1]!='/':
        manuscript_directory+='/'

    figures_directory = manuscript_directory+'figures/'
    tables_directory = manuscript_directory+'tables/'

    source_figure_directories = [figures_directory+source+'/' for source in sources]
    source_output_directories = [output_directory+source+'/' for source in sources]
    for directory in [figures_directory, tables_directory]+source_figure_directories+source_output_directories:
        if not os.path.exists(directory):
            os.mkdir(directory)

    all_gridsearch_scores = []
    source_observation_counts = []

    alphabet = [str(chr(letter)).upper() for letter in range(97,123)] 

    # 2: Source-wise Machine Learning #

    for source_index, source in enumerate(sources): 

        source_figure_directory = source_figure_directories[source_index]

        scalar_context_path = f'{input_directory}{source}_Scalar-Input.csv'
        qpo_path = f'{input_directory}{source}_QPO-Input.csv'

        n_total_qpos = len(pd.read_csv(qpo_path).index)
        n_test = int(n_total_qpos/k)
        n_train = n_total_qpos-n_test

        qpo_preprocess_dict = qpo_preprocess_dictionaries[source_index]
        context_preprocess_dict = context_preprocess_dictionaries[source_index]

        fold_performances = []
        gridsearch_scores = []

        source_observation_counts.append(len(pd.read_csv(scalar_context_path).index))

        # 2.1: Machine Learning for Each Model # 

        for model_index, model in enumerate(models):

            model_name = model_names[model_index]

            collec= collection()
            collec.load(qpo_csv=qpo_path, context_csv=scalar_context_path, context_type='scalar',  
                        context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units) 

            # 2.1.1: GridSearch # 

            scores, _, _, best_params = collec.gridsearch(model=model, parameters=model_hyperparameter_dictionaries[model_index])

            column_names = list(best_params.keys())
            columns = [[i] for i in list(best_params.values())]

            best_configuration_df = pd.DataFrame()

            for temp_index in range(len(column_names)):
                best_configuration_df[column_names[temp_index]] = columns[temp_index]

            best_configuration_df.to_csv(f'{output_directory}{source}/{model_name}_BestParams.csv', index=False)

            gridsearch_scores.append(scores)

            # 2.1.2: k-fold on Best Configuration # 

            collec.evaluate(model=model, evaluation_approach='k-fold', folds=k, repetitions=repetitions, hyperparameter_dictionary=best_params) # evaluate-approach???

            # 2.1.3: Save and Plot Performance Across Folds # 

            statistics = collec.get_performance_statistics()

            fold_performance_df = pd.DataFrame.from_dict(statistics)
            fold_performance_df['fold']=[i for i in range(len(fold_performance_df.index))]
            temp_path = f'{output_directory}{source}/{model_name}_k-fold.csv'
            fold_performance_df.to_csv(temp_path, index=False)

            fold_performances.append(list(fold_performance_df[model_comparison_statistic]))

            # 2.1.4: Plot Results Regression from 10th Fold # 
            fig, ax = plt.subplots(figsize=(4,4))

            collec.plot_results_regression(feature_name='frequency', which=[0], ax = ax, fold=9)
            temp_path = f'{source_figure_directory}results-regression_fold={9}_model={model_name}'
            plt.savefig(f'{temp_path}.pdf')
            plt.savefig(f'{temp_path}.png', dpi=200)
            plt.close()

            # 2.1.5: Plot Feature Importances from 10th Fold # 
            fig, ax = plt.subplots(figsize=(6,6))

            collec.plot_feature_importances(model=model, fold=9, kind='tree-shap', style='box', ax=ax)
            temp_path = f'{source_figure_directory}feature-importances_fold={9}_model={model_name}'
            plt.savefig(f'{temp_path}.pdf')
            plt.savefig(f'{temp_path}.png', dpi=200)
            plt.close()

        # 2.2: All-Models One Source Results # 

        # 2.2.1: Plot Performances for all Models #
        fig, ax = plt.subplots()

        plot_model_comparison(model_names=model_names, performance_lists=fold_performances, metric=model_comparison_statistic, style='violin', ax=ax)
        temp_path = f'{source_figure_directory}{source}_model-comparison'
        plt.savefig(f'{temp_path}.pdf') 
        plt.savefig(f'{temp_path}.png', dpi=200) 
        plt.close()

        # 2.2.2: Pairwise Statistical Model Comparison # 
        first_model_names, second_model_names = ([], []) 
        t_values, p_values = ([], []) 
        first_better_probabilities, second_better_probabilities = ([], []) 

        for i, first_score_list in enumerate(fold_performances):
            first_median = np.median(first_score_list)
            for j in range(i+1, model_n):

                temp_model_names = [model_names[i], model_names[j]]
                second_score_list = fold_performances[j]
                second_median = np.median(second_score_list)

                sort_idx = np.argsort([first_median, second_median])

                temp_first_name = temp_model_names[sort_idx[0]]
                temp_second_name = temp_model_names[sort_idx[1]]

                first_model_names.append(temp_first_name)
                second_model_names.append(temp_second_name)

                temp_scores = [first_score_list, second_score_list]
                temp_first_scores = temp_scores[sort_idx[0]]
                temp_second_scores = temp_scores[sort_idx[1]]

                t, p = compare_models(temp_second_scores, temp_first_scores, n_train=n_train, n_test=n_test, approach='frequentist')
                first_better, second_better, _, _ = compare_models(temp_first_scores, temp_second_scores, n_train=n_train, n_test=n_test, approach='bayesian')
            
                t_values.append(t)
                p_values.append(p)
                first_better_probabilities.append(first_better)
                second_better_probabilities.append(second_better)

        temp_columns = [first_model_names, second_model_names, t_values, p_values, first_better_probabilities, second_better_probabilities]
        temp_names = ['First Model Name', 'Second Model Name', 't', 'p', '% Chance First Better', '% Chance Second Better']
        
        pairwise_results_df = pd.DataFrame()
        for i in range(len(temp_columns)): 
            pairwise_results_df[temp_names[i]] = temp_columns[i]
        
        temp_path = f'{tables_directory}{source}_pairwise-comparison'
        
        pairwise_results_df.to_csv(f'{temp_path}.csv', index=False)
        pairwise_results_df.to_latex(f'{temp_path}.tex', index=False, float_format="%.2f")

        # 2.3: Prepare for Step 3 # 

        all_gridsearch_scores.append(gridsearch_scores)

    # 3: Collective Post-Routine Analysis #

    # 3.2: Plot GridSearch Results Plot # 
    
    if source_n>1: 
    
        fig, axs = plt.subplots(figsize=(3,1*source_n)) # fix! 

        for temp_index, source in enumerate(sources): # fix!
            ax = axs[temp_index]
            
            x = np.arange(0, len(score_arr))
            
            ax.plot(x, score_arr, label=model_names[temp_index])
            
            ax.set(xlabel=source, xticks=[], yticks=[])
            ax.legend(loc='upper right', fontsize='small')

    else: 

        fig, ax = plt.subplots(figsize=(3,1))

        for temp_index, score_arr in enumerate(all_gridsearch_scores[0]):
            x = np.arange(0, len(score_arr))
            
            ax.plot(x, score_arr, label=alphabet[temp_index])
            
            ax.set(xlabel=source, xticks=[], yticks=[])
            ax.legend(loc='upper right', fontsize='x-small')
                
    fig.supxlabel('Model Permutation')
    fig.supylabel('Score')

    #plt.tight_layout()
    plt.subplots_adjust(hspace=0)

    temp_path = f'{figures_directory}GridSearchSummary'
    plt.savefig(f'{temp_path}.pdf')
    plt.savefig(f'{temp_path}.png', dpi=150)

    # 3.3: Source Observations Table # 

    observation_summary_df = pd.DataFrame()
    observation_summary_df['Source Name'] = sources
    observation_summary_df['Class'] = source_classes
    observation_summary_df['Instrument'] = source_instruments
    observation_summary_df['Number of Observations'] = source_observation_counts

    observation_summary_df.to_latex(f'{output_directory}ObservationsTable.tex', index=False)

def classification_pipeline(sources:list, models:list, model_names:list, source_classes:list, source_instruments:list,
                            qpo_preprocess_dictionaries:dict, context_preprocess_dictionaries:list,
                            model_hyperparameter_dictionaries:list,
                            input_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline', 
                            output_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/output/pipeline',
                            manuscript_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/',
                            model_comparison_statistic:str='mae', k:int=10, repetitions:int=2): 
    
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from qpoml import collection
    from qpoml.plotting import plot_model_comparison

    # 1. Preparation for Pipeline #

    n = len(sources)
    source_n = len(sources)
    model_n = len(models)

    if input_directory[-1]!='/':
        input_directory+='/'

    if output_directory[-1]!='/':
        output_directory+='/'

    if manuscript_directory[-1]!='/':
        manuscript_directory+='/'

    figures_directory = manuscript_directory+'figures/'
    tables_directory = manuscript_directory+'tables/'

    source_figure_directories = [figures_directory+source+'/' for source in sources]
    source_output_directories = [output_directory+source+'/' for source in sources]
    for directory in [figures_directory, tables_directory]+source_figure_directories+source_output_directories:
        if not os.path.exists(directory):
            os.mkdir(directory)

    all_gridsearch_scores = []
    source_observation_counts = []

    alphabet = [str(chr(letter)).upper() for letter in range(97,123)] 

    # 2: Source-wise Machine Learning #

    for source_index, source in enumerate(sources): 

        source_figure_directory = source_figure_directories[source_index]

        scalar_context_path = f'{input_directory}{source}_Scalar-Input.csv'
        qpo_path = f'{input_directory}{source}_QPO-Input.csv'

        n_total_qpos = len(pd.read_csv(qpo_path).index)
        n_test = int(n_total_qpos/k)
        n_train = n_total_qpos-n_test

        context_preprocess_dict = context_preprocess_dictionaries[source_index]

        fold_performances = []
        gridsearch_scores = []

        source_observation_counts.append(len(pd.read_csv(scalar_context_path).index))

        # 2.1: Machine Learning for Each Model # 

        for model_index, model in enumerate(models):

            model_name = model_names[model_index]

            collec= collection()
            collec.load(qpo_csv=qpo_path, context_csv=scalar_context_path, context_type='scalar', context_preprocess=context_preprocess_dict) 

            

def net_count_rate_plots(sources=['GRS 1915+105', 'MAXI J1535-571'],
                         date_csvs:list=['/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_dates.csv', '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_dates.csv'],
                         context_csvs:list=['/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv', '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/input.csv'], 
                         y_colums:list=['A','B'],
                         figures_directory:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures'): 

    import numpy as np
    import pandas as pd 

    # 0. Preparation #

    if figures_directory[-1]!='/':
        figures_directory+='/'

    # 1.1: Plot Combined Net Counts # 

    temp_MJDs = []
    temp_NCRs = [] # NetCountRates

    source_n = len(date_csvs)

    for i in range(source_n):
        date_df = pd.read_csv(date_csvs[i])
        source_df = date_df.merge(pd.read_csv(context_csvs[i]), left_on='observation_ID', right_on='observation_ID')

        temp_MJDs.append(np.array(source_df['MJD']))
        temp_NCRs.append(np.array(source_df[y_colums[i]])) 
    
    if source_n>1: 
        fig, axs = plt.subplots(source_n, 1, figsize=(6,2*source_n))

        for i in range(source_n):
            ax = axs[i] 
            if sources[i] == 'MAXI J1535-571':
                c = np.array(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/output.csv')['qpo_state'])
                ax.scatter(temp_MJDs[i], temp_NCRs[i], s=2, c=c)
            else: 
                ax.scatter(temp_MJDs[i], temp_NCRs[i], s=2)
            
            
            ax.xaxis.set_ticklabels([])
            
        fig.supylabel('Normalized Count Rate', fontsize='small') # Source-Wise Median Normalized Net Count Rate
        fig.supxlabel('Date (MJD)', fontsize='small')

    else: 
        fig, ax = plt.subplots(figsize=(6,2))

        ax.scatter(temp_MJDs[0], temp_NCRs[0], s=2)
        ax.set_ylabel('Normalized Count Rate', fontsize='small') 
        ax.set_xlabel('Date (MJD)', fontsize='small')
        ax.xaxis.set_ticklabels([])

    plt.subplots_adjust(hspace=0)
    #plt.tight_layout()
    plt.savefig(f'{figures_directory}stacked_NCRs.pdf')
    plt.savefig(f'{figures_directory}stacked_NCRs.png', dpi=200)
    plt.close()

#net_count_rate_plots()