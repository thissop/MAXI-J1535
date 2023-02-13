def test_qpo_tensor_shape(): 
    from qpoml import collection
    from sklearn.linear_model import LinearRegression

    collec = collection()

    qpo_path = '/Users/yaroslav/Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/output-data.csv'
    context_path = '/Users/yaroslav/Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/input-data.csv'

    context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
    qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
    units = {'frequency':'Hz'}

    collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                        context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

    collec.evaluate(model=LinearRegression(), evaluation_approach='k-fold', folds=10)
    qpo_tensor = collec.qpo_tensor

    num_qpos = []

    max_simultaneous_qpos = 2

    import numpy as np
    for i in qpo_tensor: 
        num = int(len(np.where(i!=0.1)[0])/(len(collec.qpo_features)))
        num_qpos.append(num)

    print(num_qpos)

#test_qpo_tensor_shape()

def get_params_grid():
    from itertools import product

    parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    
    # Always sort the keys of a dictionary, for reproducibility
    
    params_grid = []
    items = sorted(parameters.items())
    keys, values = zip(*items)
    for v in product(*values):
        params = dict(zip(keys, v))
        params_grid.append(params)

    print(params_grid)

#get_params_grid()

def test_updated_train_test_split():
    from qpoml import collection
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor

    collec = collection()

    qpo_path = '/Users/yaroslav/Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/output-data.csv'
    context_path = '/Users/yaroslav/Documents/GitHub/MAXI-J1535/referee-feedback/first-round/blending/input-data.csv'

    context_preprocess_dict = {'A':'normalize','B':'normalize','C':'normalize','D':'normalize','E':'normalize','F':'normalize','G':'normalize'}
    qpo_preprocess_dict = {'frequency':'normalize', 'width':'normalize', 'rms':'normalize'}
    units = {'frequency':'Hz'}
    gridsearch_dictionary = {'min_samples_leaf':[1,2], 'min_samples_split':[2], 'n_estimators':[50,100]}

    collec.load(qpo_csv=qpo_path, context_csv=context_path, 
                        context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 

    collec.evaluate(model=RandomForestRegressor(), evaluation_approach='k-fold', folds=10, stratify=False, gridsearch_dictionary=gridsearch_dictionary)

test_updated_train_test_split()