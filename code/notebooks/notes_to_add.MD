## Other Ideas
* Good link for [Multi-Output Regression](https://machinelearningmastery.com/multi-output-regression-models-with-python/)
* I think the idea of moving away from neural networks is also good because the sample is so incredibly small. 
* Some simplier regression machine learning algorithms that support multiple outputs directly: 
    * LinearRegression (an related such as RidgeRegression and LASSORegression)
    * DecisionTreeRegressor
    * RandomForestRegressor (and related)
* Another good idea is to train multiple iterations of the same model and average their predictions (I did this in my most recent version of the neural network-knn ensemble...the variance was really bad tho haha). 
* I wonder if there are outliers in the dataset ... sklearn library has a couple nice outlier detection algos (e.g. OneClassSVM, LocalOutlierFactor, IsolationForest, etc. See this [link](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_anomaly_comparison.html#sphx-glr-auto-examples-miscellaneous-plot-anomaly-comparison-py))
* The multi-output regression article I linked up above also discusses this interesting concept called chain multi-output regression. 
      * From the article: "if a multioutput regression problem required the prediction of three values y1, y2 and y3 given an input X, then this could be partitioned             into three dependent single-output regression problems as follows: 1. Given X, predict y1; 2. Given X and yhat1, predict y2; 3. Given X, yhat1, and yhat2, predict y3 
         
* Not sure if this article is helpful, but here's the arXiv link: [link](https://arxiv.org/pdf/1901.00248.pdf). 
* sklearn also has this interesting feature called [sklearn.multioutput.MultiOutputRegressor¶
](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html) which "consists of fitting one regressor per target...a simple strategy for extending regressors that do not natively support multi-target regression." 
