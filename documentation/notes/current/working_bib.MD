# Working Bibliography

## Reading List

### Priority: 
- [ ] SN20
- [ ] P21
- [ ] QPO2020

### Other: 
* [Evaluating the Impact of Missing Data Imputation
through the use of the Random Forest Algorithm](https://arxiv.org/ftp/arxiv/papers/0812/0812.2412.pdf#:~:text=Results%20indicate%20that%20Random%20Forests,when%20compared%20with%20autoassociative%20networks.)
* [Accuracy of random-forest-based imputation of missing data in the presence of non-normality, non-linearity, and interaction
](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-020-01080-1)
* [When do random forests fail?](https://proceedings.neurips.cc/paper/2018/file/204da255aea2cd4a75ace6018fad6b4d-Paper.pdf)
* [A survey on missing data in machine learning
](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-021-00516-9)
* [XGBoost: A Scalable Tree Boosting System](https://arxiv.org/pdf/1603.02754.pdf)
    * Section 3.4 discusses how XGBOOST natively deals with missing values
* [The Smallest Sample Size for the Desired Diagnosis Accuracy](https://www.iaras.org/iaras/filedownloads/ijoct/2017/028-0004(2017).pdf)
    * Cancer data...talks about XGBoost performance on small datasets (even down to n=50)

* [Feature Engineering and Selection, 2019](https://machinelearningmastery.com/handle-missing-data-python/)
* [Applied Predictive Modeling, 2013](http://appliedpredictivemodeling.com/)

## Best Papers
- [ ] [Sreehari and Nandi 2020](https://arxiv.org/pdf/2101.06218.pdf): hereafter I'll refer to it as SN20. Title: *A Machine Learning approach for classification of accretion states of
Black hole binaries*
- [ ] [Pattnaik et al. 2021](https://pure.rug.nl/ws/portalfiles/portal/157958141/staa3899.pdf): hereafter I'll refer to this paper as P21. Title: *A machine-learning approach for classifying low-mass X-ray binaries based on their compact
object nature*
- [ ] [Ingram and Motta 2020](https://arxiv.org/pdf/2001.08758.pdf): hereafter I'll refer to this paper as QPO2020. Title: *A review of quasi-periodic oscillations from black hole X-ray binaries: observation and theory*
- [x] [Cuneo et al. 2020](https://arxiv.org/pdf/2006.03074.pdf): hereafter I'll refer to this paper as Cuneo2020. Title: *A NICER look at the state transitions of the black hole candidate MAXI J1535-571 during its reflares* 

## Notes

### Astrophysics

### Machine Learning

* [Applied Predictive Modeling, 2013](http://appliedpredictivemodeling.com/)
    * "… missing data can be imputed. In this case, we can use information in the training set predictors to, in essence, estimate the values of other predictors."
        * JBL says you can use "A constant value that has meaning within the domain, such as 0, distinct from all other values, a value from another randomly selected record; a mean, median or mode value for the column; a value estimated by another predictive model."
        
* [Feature Engineering and Selection, 2019](https://machinelearningmastery.com/handle-missing-data-python/)
    * "Many popular predictive models such as support vector machines, the glmnet, and neural networks, cannot tolerate any amount of missing values."
    * "Missing values are common occurrences in data. Unfortunately, most predictive modeling techniques cannot handle any missing values. Therefore, this problem must be addressed prior to modeling."
    * "When a predictor is discrete in nature, missingness can be directly encoded into the predictor as if it were a naturally occurring category."
    * "The simplest approach for dealing with missing values is to remove entire predictor(s) and/or sample(s) that contain missing values."