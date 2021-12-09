* **Train/test/validation:** It seems that using a different train test validation scheme would be good for this. 
    * From [applied predictive modeling](https://vuquangnguyen2016.files.wordpress.com/2018/03/applied-predictive-modeling-max-kuhn-kjell-johnson_1518.pdf):
        * A test set is a single evaluation of the model and has limited ability to characterize the uncertainty in the results.
        * With small sample sizes:
            * The model may need every possible data point to adequately determine model values.
            * The uncertainty of the test set can be considerably large to the point where different test sets may produce very different results.
            * Resampling methods can produce reasonable predictions of how well the model will perform on future samples.