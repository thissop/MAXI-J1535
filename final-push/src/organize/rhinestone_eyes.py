from qpoml import collection
import matplotlib.pyplot as plt 

spectrum_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/spectral_summary_for_qpoml.txt'
qpo_csv = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/qpo_summary_for_qpoml.txt'

collection_one = collection()
collection_one.load(qpo_csv=qpo_csv, context_csv=spectrum_csv, context_type='scalar',context_preprocess={'gamma':'normalize','kTe':'normalize','nthcomp_norm':'normalize','diskbb_tin':'normalize','diskbb_norm':'normalize'}, qpo_preprocess={'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}, qpo_approach='single')

from sklearn.ensemble import RandomForestRegressor

regr = RandomForestRegressor()

collection_one.evaluate(model=regr, model_name='RandomForestRegressor', evaluation_approach='k-fold', folds=20, repetitions=2)

fig, axs = plt.subplots(2,2, figsize=(12,12))

collection_one.plot_correlation_matrix(ax=axs[0,0])
collection_one.plot_dendrogram(ax=axs[0,1])
collection_one.plot_vif(ax=axs[1,0])
collection_one.plot_feature_importances(kind='tree-shap', ax=axs[1,1])

plt.tight_layout()
plt.savefig('initial_results.png', dpi=150)

fig, axs = plt.subplots(5,2, figsize=(3,15))

for i in range(0,5):
    collection_one.plot_results_regression(ax=axs[i,0], which=[0], feature_name='frequency', fold=i)
    collection_one.plot_results_regression(ax=axs[i,1], which=[0], feature_name='frequency', fold=i)

#plt.tight_layout()
plt.savefig('initial_results_regression.png', dpi=150)