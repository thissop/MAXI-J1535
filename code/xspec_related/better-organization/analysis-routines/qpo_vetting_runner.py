#spell-checker: disable

def vetting_with_comments_run(): 
    import pandas as pd
    import numpy as np 

    from qpo_vetting_modules import hunter, make_vetting_plot

    full_ids = np.array(pd.read_csv('./code/xspec_related/good_ids.csv'))

    for full_id in full_ids: 
        canidates_dict, labels_dict = hunter('1050360106_6')

        annot = {'algo_labels':labels_dict}

        make_vetting_plot('1050360106_6', canidates_dict=canidates_dict)



        break 

vetting_with_comments_run()

