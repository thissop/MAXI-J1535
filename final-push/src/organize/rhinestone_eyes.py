from qpoml import collection

spectrum_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt'
qpo_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/qpo_summary_for_qpoml.txt'

collection_one = collection()
collection_one.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

from sklearn.linear_model import RandomForestRegressor

regr = RandomForestRegressor()
collection_one.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=20)

import matplotlib.pyplot as plt 

fig, axs = plt.subplots(2,2, figsize=(12,12))

collection_one.plot_correlation_matrix(ax=axs[0,0])
collection_one.plot_dendrogram(ax=axs[0,1])
collection_one.plot_vif(ax=axs[1,0])
collection_one.plot_feature_importances(kind='tree-shap', ax=axs[1,1])

plt.tight_layout()
plt.savefig('./final-push/src/organize/initial_results', dpi=150)

collection_two = collection()
collection_two.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

collection_three = collection() 
collection_three.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

names = []
mses = []

names.append('LinearRegression')
mses.append(collection_one.get_performance_statistics()['mse'])

'''
regr = RandomForestRegressor(n_estimators=200)
collection_two.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=20)

names.append('RandomForest')
mses.append(collection_two.get_performance_statistics()['mse'])

regr = GradientBoostingRegressor(n_estimators=200)
collection_three.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=20)

names.append('GradientBoostingRegressor')
mses.append(collection_three.get_performance_statistics()['mse'])
'''

import pandas as pd 
import numpy as np

df = pd.DataFrame(np.transpose(mses), columns=names)

df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/organize/mse_temp.csv',index=False)

r'''

print('first plot')
fig, axs = plt.subplots(2,2, figsize=(12,12))

collection_one.plot_correlation_matrix(ax=axs[0,0])
collection_one.plot_dendrogram(ax=axs[0,1])
collection_one.plot_vif(ax=axs[1,0])
collection_one.plot_feature_importances(kind='tree-shap', ax=axs[1,1])

plt.tight_layout()
plt.savefig('./final-push/src/organize/initial_results', dpi=150)

print('second plot')

fig, axs = plt.subplots(5,2, figsize=(4,16))

for i in range(0,5):
    collection_one.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_one.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i+5)

#plt.tight_layout()
plt.savefig('./final-push/src/organize/rf_results_regression.png', dpi=150)
'''