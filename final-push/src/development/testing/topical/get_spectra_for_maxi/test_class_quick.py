import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from qpoml import collection
from qpoml.utilities import roc_and_auc
from qpoml.plotting import plot_roc
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

spectrum_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Rebin-Spectra.csv'
qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_QPO-Input.csv'

model_name = 'LogisticRegression'
source = 'MAXI'

labels = [f'rebin_channel_{i}' for i in range(19)]

context_preprocess_dictionary = dict(zip(labels, len(labels)*['normalize']))

collec = collection()
collec.load(qpo_csv=qpo_path, context_csv=spectrum_path, context_preprocess=context_preprocess_dictionary, approach='classification', units={'frequency':'hz'})

collec.evaluate(model=LogisticRegression(), evaluation_approach='k-fold', folds=10, stratify=True)

# .1 Confusion Matrix # 
plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
sns.set_context('paper')
fig, ax = plt.subplots(figsize=(4,4))
collec.plot_confusion_matrix(fold=0, ax=ax, labels=['No QPO', 'QPO'])

cm_path = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/get_spectra_for_maxi/{model_name}-{source}-confusion_matrix'
fig.tight_layout()
plt.savefig(f'{cm_path}.png', dpi=200)

plt.clf()
plt.close()

# .2 ROC Curve # 

fig, ax = plt.subplots(figsize=(4,4))
plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish.mplstyle')
sns.set_context('paper')
fpr, tpr, std_tpr, auc, std_auc = collec.roc_and_auc()
plot_roc(fpr=fpr, tpr=tpr, std_tpr=std_tpr, auc=auc, ax=ax, std_auc=std_auc)

roc_path = f'/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/get_spectra_for_maxi/{model_name}-{source}-ROC'
fig.tight_layout()
plt.savefig(f'{roc_path}.png', dpi=200)