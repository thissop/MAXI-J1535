#spell-checker: disable

def vetting_with_comments_run(): 
    import pandas as pd
    import numpy as np 
    import os

    from qpo_vetting_modules import hunter, make_vetting_plot

    full_ids = np.array(pd.read_csv('./code/xspec_related/good_ids.csv')['full_id'])

    comments = []

    plot_dir = './code/xspec_related/qpo_routines/make_vetting_plots/plots'

    for full_id in full_ids: 
        canidates_dict, labels_dict = hunter(full_id)

        annot = {'algo_labels':labels_dict['canidate_labels']}

        make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annot) 

        user_input = input(full_id+" THOUGHTS: ")

        annot = {'algo_labels':labels_dict['canidate_labels'], 
                 'my_thoughts':user_input}

        
        make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annot, plot_dir=plot_dir) 

        # get user input, remake plot adding user input to the ax_dict['F'], and save without showing 

    zipped = list(zip(full_ids, comments))
    df = pd.DataFrame(zipped, columns=['full_id', 'comment'])

    df.to_csv('prelim_vetting_classes.csv', index=False)

vetting_with_comments_run()

