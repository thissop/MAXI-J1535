import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt 
import seaborn as sns

fold = 9

collec = collection()

qpo_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'
context_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
units = {'frequency':'Hz'}

collec.load(qpo_csv=qpo_path, context_csv=context_path, context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=10)

y_test = collec.y_test
predictions = collec.predictions

def bias_report(predictions, y_test, feature_names:list, ax:None, fold:int=0):
    r'''
    
    Arguments
    ---------

    predictions 
        - list of shape (m, n) where (m) is number of 'rows' or instances/observations, and (n) is number of features. Can be for multiple folds, zeroth will be selected for study by default

    y_test 
        - same, but for true values

     
    '''

    from scipy import stats 

    predictions, y_test = (np.transpose(i) for i in [predictions[fold], y_test[fold]])

    diffs = [i-j for i, j in zip(predictions, y_test)]

    means = np.mean(np.abs(diffs), axis=1)
    stds = np.array([np.std(i) for i in np.abs(diffs)])

    plt.style.use('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/QPOML/qpoml/stylish.mplstyle')
    sns.set_context("paper") #font_scale=
    sns.set_palette('deep')
    seaborn_colors = sns.color_palette('deep')

    df = pd.DataFrame()

    for i in range(len(diffs)): 
        df[feature_names[i]] = diffs[i]

    fig, ax = plt.subplots()
    sns.boxplot(data=df, color=seaborn_colors[0])
    ax.set(xlabel='QPO Parameter', ylabel='Normalized Residual')

    ks_ps = {} 

    for i in range(len(diffs)):
        for j in range(i, len(diffs)-1):
            p = stats.kstest(diffs[i], diffs[j], alternative='two-sided')[1]
            ks_ps.update(f'{feature_names[i]}-{feature_names[j]}':[p])

    ks_df = pd.DataFrame(ks_ps)

    return ks_df 

bias_report(predictions, y_test, feature_names=['Frequency', 'Width', 'rms'])