def get_plot(id: str): 
    from PIL import Image
    import requests

    url = 'https://raw.githubusercontent.com/thissop/MAXI-J1535/main/code/xspec_related/qpo_routines/full_aggregation/plot_dists/quad-panels/'
    url += id + '.png'
    im = Image.open(requests.get(url, stream=True).raw)

    return im

def run_grid_search(grid, X, y, n_splits: int = 10, model: str = 'randomforest'): 
    import numpy as np
    from sklearn.model_selection import StratifiedKFold
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    
    skf = StratifiedKFold(n_splits=n_splits)

    if model=='randomforest': 

        grid_dict = {'n_estimators':[50, 100, 500, 1000],
                'min_samples_split':[2,4,6,8],
                'min_samples_leaf':[1,2,3]}

        keys = grid_dict.keys()
        grid_matrix = []
        grid_scores = []
        for i in grid_dict[keys[0]]: 
            for j in grid_dict[keys[1]]: 
                for k in grid_dict[keys[2]]: 
                    combination = [i,j,k]
                    grid_matrix.append(combination)

        for combination in grid_matrix: 
            scores = []
            for train_index, test_index in skf.split(X, y):

                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]

                regr = RandomForestRegressor(n_estimators=combination[0], 
                                             min_samples_split=combination[1], 
                                             min_samples_leaf=combination[2])
                regr.fit(X_train,y_train)

                predictions = regr.predict(X_test)
                
                score = regr.score(y_test, predictions)
                scores.append(score)
            
            grid_scores.append(np.mean(scores))
    
        return grid_matrix, grid_scores

    elif model=='linear':
        scores = []
        for train_index, test_index in skf.split(X, y):

            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            regr = LinearRegression()
            regr.fit(X_train,y_train)

            predictions = regr.predict(X_test)
            
            score = regr.score(y_test, predictions)
            scores.append(score)

        return scores, np.mean(scores)
