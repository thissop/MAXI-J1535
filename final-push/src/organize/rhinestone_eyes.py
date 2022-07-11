from qpoml import collection
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import pandas as pd 
import numpy as np
import seaborn as sns

spectrum_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt'
qpo_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/qpo_summary_for_qpoml.txt'

collection_one = collection()
collection_one.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

collection_two = collection()
collection_two.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

collection_three = collection() 
collection_three.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'})

'''
fig, ax = plt.subplots(figsize=(6,6))

collection_one.plot_correlation_matrix(ax=ax)

plt.savefig('./final-push/src/organize/correlation_matrix.png', dpi=150)
'''

names = []
mses = []

regr = ExtraTreesRegressor()
collection_one.evaluate(model=regr, model_name='ExtraTreesRegressor', evaluation_approach='k-fold', folds=20)
names.append('ExtraTreesRegressor')
mses.append(collection_one.get_performance_statistics()['mse'])

regr = RandomForestRegressor(n_estimators=200)
collection_two.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=20)
names.append('RandomForest')
mses.append(collection_two.get_performance_statistics()['mse'])

regr = LinearRegression()
collection_three.evaluate(model=regr, model_name='LinearRegression', evaluation_approach='k-fold', folds=20)
names.append('LinearRegression')
mses.append(collection_three.get_performance_statistics()['mse'])

for i in [collection_one, collection_two, collection_three]:
    print(i.get_data()[0][0])

# Make Plots # 

fig, axs = plt.subplots(1,3, figsize=(12,4))

collection_one.plot_feature_importances(ax=axs[0])
axs[0].set(title='Bar')

collection_one.plot_feature_importances(ax=axs[1])
axs[1].set(title='Point')

collection_one.plot_feature_importances(ax=axs[1])
axs[2].set(title='Violin')

plt.savefig('./final-push/src/organize/better_feature_importances_tree.png', dpi=150)


'''
fig, ax = plt.subplots(figsize=(6,6))

collection_one.plot_correlation_matrix(ax=ax)

plt.savefig('./final-push/src/organize/correlation_matrix.png', dpi=150)

sns.set_style('darkgrid')
sns.set_context("paper") #font_scale=
sns.set_palette('deep')

fig, axs = plt.subplots(2,2, figsize=(12,12))

collection_one.plot_dendrogram(ax=axs[0,1])
collection_one.plot_vif(ax=axs[1,0])
collection_one.plot_feature_importances(kind='tree-shap', ax=axs[1,1])

plt.tight_layout()
plt.savefig('./final-push/src/organize/initial_results_three_plots.png', dpi=150)

df = pd.DataFrame(np.transpose(mses), columns=names)

fig, ax = plt.subplots(figsize=(5,5))

sns.set_style('darkgrid')
sns.set_context("paper") #font_scale=
sns.set_palette('deep')

sns.violinplot(data=df, ax=ax)

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/organize/violins.png', dpi=150)

sns.set_style('darkgrid')
sns.set_context("paper") #font_scale=
sns.set_palette('deep')

fig, axs = plt.subplots(5,2, figsize=(4,16))
                             
for i in range(0,5):
    collection_one.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_one.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i+5)

plt.savefig('./final-push/src/organize/rf_results_regression.png', dpi=150)
'''