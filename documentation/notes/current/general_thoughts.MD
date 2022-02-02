# General Thoughts

## Dated Thoughts
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
