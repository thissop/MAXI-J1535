# General Thoughts

## Dated Thoughts

* 4/9/2022
   * it's interesting how the shapley importances show that the models leverage a hard and soft channel first most importantly, and then two more hards and then a soft. 
   *  [force plots](https://miro.medium.com/max/1400/1*F40hOH_QlubjQuaiqzOPig.png) and [shap decision plots](https://shap-lrjball.readthedocs.io/en/docs_update/example_notebooks/plots/decision_plot.html) could be useful 
        * show true vs predicted in results, then show shap feature importances, a force plot, and a shap decision plot in discussion?  

* 4/5/2022: 
   * two thoughts for today: 
       1. [this](https://scikit-learn.org/stable/modules/cross_validation.html) may be an issue?
       2. I wonder if we should style the paper as both a proof of concept/methodological test to develop methods for a future paper predicing QPO properties based on spectral data for numerous sources, as well as an interesting investigation in MAXI-J1535-571 in itself. Mention this throughout paper, maybe also talk about a future thing to work on is more automated QPO detection/characterization vetting procedure.    

* 4/3/2022
    * Found a paper that compared random forest and a simplier linear regression in cancer data, sample size was similiar to ours (n=440 ish): [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4610387/)    
    * **Things to read on SHAP/Tree SHAP/Shapley:**
      1. https://christophm.github.io/interpretable-ml-book/shapley.html
      2. https://christophm.github.io/interpretable-ml-book/shap.html#fn69
      3. https://www.datatrigger.org/post/interpretable_machine_learning_shap/

* 3/10/2022
    * In addition to how I have been plotting QPOs from the same PDS in unique colors compared to their peers on the color scale (gotta check if this is continuous), I think I should also use different markers for the different confidence classes they come from (so e.g. I can see how well the broad one is fit). 
    * For a bit I was nervous about the justification for ML in this paper, but now I realize that including data from the wider QPOs is gonna require ML because it will mess up linear regression. 
    * Something I should do is add a "confidence stage" classification column so I can back track which inclusions introduce errors into the model (mention this to Dr. Steiner)...I wish I did this earlier. So far I think I'll only have two confidence stages by the end of tonight: the original classes I explored on sunday in collab, as well as the new classes I'll add that are broader. 
        * make sure at least two of the broader classes are in the test set? --> imbalenced class problem is still in the paper, let's go!  
    * Also, something I was thinking about is should I plot normal (i.e. not normalized) frequencies against their predictions and calculate mae/mse on them? 
    * List of things to email: 
        * Fit parameters for simple doubles cliffs; examples: [1050360113_1, 1050360113_4, 1130360110_3]
            * Similar doubles but slightly different shapes: [1130360105_3,1130360106_1]
        * Ask about rare case of triple with cliff: [1130360106_0, 1130360108_2, 1130360110_1]
    * Plan for 3/10/2022 Night Work: 


* 3/10/2022
    * For a bit I was nervous about the justification for ML in this paper, but now I realize that including data from the wider QPOs is gonna require ML because it will mess up linear regression. 
    * Also, something I was thinking about is should I plot normal (i.e. not normalized) frequencies against their predictions and calculate mae/mse on them? 
    * List of things to email: 
        * Fit parameters for simple doubles cliffs; examples: [1050360113_1, 1050360113_4, 1130360110_3]
            * Similar doubles but slightly different shapes: [1130360105_3,1130360106_1]
        * Ask about rare case of triple with cliff: [1130360106_0, 1130360108_2, 1130360110_1, ]
    * Plan for 3/10/2022 Night Work: 
    
* 3/6/2022
    * I wonder if we should critique the ML approach for state classification by Sreehari and Nandi because they discuss including normalized MJD in their clustering models...some different sources online suggest how you shouldn't use it in this context because you couldn't then use the predictive model in the future as future dates wouldn't be included in the training data set (paraphrased from [this article](https://towardsdatascience.com/machine-learning-with-datetime-feature-engineering-predicting-healthcare-appointment-no-shows-5e4ca3a85f96))...we could say something like "In contrast to the approach of Sreehardi and Nandi (2021), we specifically do not use observation times as input features in any of our models as we are specifically designing the models so that they can be used as valid predictors of QPO properties in future observations..."
    * From a different [article](https://towardsdatascience.com/avoid-these-deadly-modeling-mistakes-that-may-cost-you-a-career-b9b686d89f2c), since Sreehardi and Nandi are doing the normalization of the MJD data time values for each source individually, I think this is a big issue, because these values then become psuedo-"ID" values. See the following excerpt: 
        * > Be careful about any DateTime field of the yymmdd:hhmmss format. You cannot employ this variable in any tree-based methods. As shown in the exhibit, this variable appears on the top of the variable importance chart. The reason is that this field almost becomes a unique identifier for each record. It is as if you employ the ‘id’ field in your decision trees. I am certain you need to derive year, month, day, weekday, etc. from this field. Remember, feature engineering is to capture repeatable patterns, such as month or week of the year, in order to predict the future. In some models, you may use ‘year’ as a variable just to explain any special volatility in the past. But you will never use the raw DateTime field as a predictor.
    * From the same article, decision trees do not make any assumptions for the distributions of the target variables, and **most importantly,** "decision trees and boosted tree algorithms are immune to multicollinearity" as "among perfectly correlated variables, a decision tree will choose only one of the variables that provide the best split"
    * Apparently you should create dummy variables / on hot encoding for categorical variables 
    * I think I should instead of doing min-max standardization, fit a z-score standardizer on all in the input features, and then applying that z-score standardizer to the test data 
    * Also, will probably need to redact a bunch of stuff from this repo before making it public lol
    * Apparently spearman technique can measure non-linear correlations 
    * I think I'm not going to show the dendrogram plots in the paper...in the part where I make feature selections in the KNN-Ridge regression on XSPEC features, I'll just mention the issue of multicollinearity for linear models (and how it's actually not an issue for tree models like Random Forest), and then say I select values within the clusters to run the ridge on 
    * Nice wording from sklearn: "handle multicollinearity by performing hierarchical clustering on the features’ Spearman rank-order correlations, picking a threshold, and keeping a single feature from each cluster."
        * Thus, we could say something like "Although multicollinearity is not an issue for tree models like Random Forest, for this KNN-Ridge model, we account for it by performing a hierarchical clustering of the Spearman rank-order correlations between the fitted features, using a threshold of *x* to select representative features from each cluster" 
            * This will likely leave me with disk normalization and gamma? 
    * Very interesting blurb from sklearn: 
        * > When two features are correlated and one of the features is permuted, the model will still have access to the feature through its correlated feature. This will result in a lower importance value for both features, where they might actually be important. One way to handle this is to cluster features that are correlated and only keep one feature from each cluster.

* 2/27/2022
    * I think I am going to take a break from reading papers related to this project / writing the paper (at least take a break from writing the astro aspect of it) for the time being, perhaps until after AP exams because my RAM won't be able to handle all the information I'll need to read and know to be able to write for this until after APs I think. 

* 2/1/2022
    * "When MAXI J1535-571 is dim and Cir X-1 is bright, there is a contamination from Cir X-1. We limit the source region for MAXI J1535 to avoid contamination by Cir X-1. Thus the count-rate of MAXI J1535 is about the half of the real one in the plots and data." - MAXI Website .... ??????
* 1/24/2022
    * Yes, I think I should definitely used Shapley or SHAP values with regards to feature importance...see this really useful article: [link](https://christophm.github.io/interpretable-ml-book/shapley.html)
        * It would be really cool to mention "a method from coalitional game theory" in the paper. 
* 1/23/2022
    * I wonder if after seeing how poor data fixes doesn't help we then show the 2d hist of log(red chi) vs log(brightness) or something
    * we can also use random forest / xgboost importances with binary flag inputs or additional input of just the normalized red chis to see how important those are
    * can models be informative even though the red chi ^2 is bad? what do these look like? 
    * I also wonder how many of the old ids were dropped, and how many of the new ones have qpos
        * it may be bad if some were dropped because this would possibly affect classification 
    * exposure times in pds files are `1` placeholders...the actual values are stored in their corresponding spectral `.jsgrp` files. 
    * "the correlation between intensity and QPO frequency is a known one"
    * should probably read these three articles on permutation testing // feature importance: [first](https://scikit-learn.org/stable/modules/permutation_importance.html), [second](https://explained.ai/rf-importance/), and [third](https://christophm.github.io/interpretable-ml-book/feature-importance.html). 
        * that third link seems to have a bunch of other links worth reading too...like about Shapley Values vs SHAP values...speaking of which, I think I should measure feature importances with permutation *and* Shapley/SHAP values ... for robust reasons, as well as for the reason that it would be cool to incorporate a little game theory into the paper :smiling_imp:

* 1/21/2022
    * I wonder what the accuracy of the model will be like based on the dates of the time values associated with the train/test observations...it seems like this source would be an interesting exploration because our data is coming from multiple outbursts...like could the QPO properties change (for states of similiar hardness) between outbursts? 
    * it seems like we have a reason why our experamentation with data points of varying quality (as determined by XSPEC) ... a lot of the brightest observations (with good qpos, etc.) have very poor reduced chi square values...is the model I used in xspec not good for these high luminosity cases? because it seems to provide data that is accurate enough for good classification capabilities. 
        * if I discuss this in the paper, probably discuss after showing how the missing value methods didn't really make a difference (at least for RandomForest and XGBoost)...*suspense*
         


* 1/16/2022
    * Should probably read this before writing about the machine learning (general classes of machine learning): [link](https://machinelearningmastery.com/a-tour-of-machine-learning-algorithms/)
        * Remember the difference between discriminative and generative models
    * Extremely helpful article about three different ways to calculate feature importances with XGBOOST (and can be applied to Random Forest as well): [link](https://mljar.com/blog/feature-importance-xgboost/)
        * Should probably read this sklearn article about F-test vs permutation based importances (as explored with a random forest model) as well: [link](https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html)

* 1/15/2022
    * Typing ```"\\wsl$``` in the address bar of 

* 1/1/2022
    * Machine learning mastery article on Histogram Gradient Boosting: [link](https://machinelearningmastery.com/histogram-based-gradient-boosting-ensembles/)

* 12/29/2021 
    * Note how the SN20 paper doesn't have error bars on their time vs gamma/tin/etc. plot 
    * I am allowed to submit work from published papers to Regeron STS! 
    * I would like to include a plot of MAXI J1535-371 itself...I downloaded a couple images from the [MAXI website](http://maxi.riken.jp/mxondem/), we'll see if they have high enough resolution. 

## Before Dating
* It seems that we would be innovating with this work as a quick search on ADS reveals no similiar works have been published(?):  
![nasa ads](images/nasa_ads_bhb_ml.PNG)
* This plot seems interesting, relevant, and informative:  
![hyper parameter dist](images/hyperparameter_dist.png)
* Is the plot in this paper an appropriate way to show maximum accuracy: https://arxiv.org/pdf/1903.07167.pdf
* This is the one with the grid search plot: https://arxiv.org/pdf/2109.10503.pdf
