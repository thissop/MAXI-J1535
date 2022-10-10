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

qpo_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][two-feature-regression].csv'
context_path = '/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv'

context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'normalization':'normalize'}
units = {'frequency':'Hz', 'width':None, 'rms':None}

collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

stratify_dictionary = pd.read_csv('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/data/pipeline/MAXI/[QPO][binary].csv').to_dict(orient='list')
print(stratify_dictionary)
collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=folds, stratify=stratify_dictionary)
