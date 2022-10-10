import numpy as np 
import pandas as pd 
from qpoml import collection 
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import seaborn as sns
from qpoml.utilities import unprocess1d

import matplotlib.pyplot as plt 

fold = 9
folds = 10

collec = collection()

qpo_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[QPO][regression].csv'
context_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/GRS/[scalar-input][regression].csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
units = {'frequency':'Hz', 'width':'', 'rms':''}

collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=folds)

qpo_preprocess1d_tuples = collec.qpo_preprocess1d_tuples

predictions, y_test = (np.transpose(collec.predictions[fold]), np.transpose(collec.y_test[fold]))
keys = ['frequency', 'width', 'rms']

true_frequencies = unprocess1d(y_test[0], qpo_preprocess1d_tuples[keys[0]])
true_widths = unprocess1d(y_test[1], qpo_preprocess1d_tuples[keys[1]])
true_rms = unprocess1d(y_test[2], qpo_preprocess1d_tuples[keys[2]])

true = [true_frequencies, true_widths, true_rms]

predicted_frequencies = unprocess1d(predictions[0], qpo_preprocess1d_tuples[keys[0]])
predicted_widths = unprocess1d(predictions[1], qpo_preprocess1d_tuples[keys[1]])
predicted_rms = unprocess1d(predictions[2], qpo_preprocess1d_tuples[keys[2]])

predicted = [predicted_frequencies, predicted_widths, predicted_rms]

i, j, k = (np.array(true[z]) for z in range(3))
l, m, n = (np.array(predicted[z]) for z in range(3))
sums = ((i-l)**2)+((j-m)**2)+((k-n)**2)
diffs = sums**0.5

freq_diffs = np.abs(true_frequencies-predicted_frequencies)

results_df = pd.DataFrame()
data = [list(np.array(collec.observation_IDs)[collec.test_indices[fold]]), 
        diffs, freq_diffs,
        true_frequencies, true_widths, true_rms,
        predicted_frequencies, predicted_widths, predicted_rms]

column_names =['observation_ID', 'pythagorean_diff', 'freq_diff', 'true_freq', 'true_width', 'true_rms', 'pred_freq', 'pred_width', 'pred_rms']

out_df = pd.DataFrame()
for i, j in zip(data, column_names): 
    out_df[j]=i

out_df = out_df.sort_values(by=['pythagorean_diff'])

out_df.to_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/production/individual_figures/figure_5/grs_predictions_true.csv', index=False)

print(np.median(diffs))