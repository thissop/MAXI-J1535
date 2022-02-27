#spell-checker: disable

def vetting_with_comments_run(): 
    import pandas as pd
    import numpy as np 

    from qpo_vetting_modules import hunter, make_vetting_plot

    full_ids = np.array(pd.read_csv('./code/xspec_related/good_ids.csv'))

    for full_id in full_ids: 
        canidate_dict, labels_dict = hunter()

        

        break 

vetting_with_comments_run()

