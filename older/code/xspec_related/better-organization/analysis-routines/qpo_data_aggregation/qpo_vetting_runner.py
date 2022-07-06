#spell-checker: disable

def vetting_with_comments_run(): 
    import pandas as pd
    import numpy as np 
    import os

    from qpo_vetting_modules import hunter, make_vetting_plot

    full_ids = np.array(pd.read_csv('./code/xspec_related/good_ids.csv')['full_id'])

    comments = []

    plot_dir = './code/xspec_related/qpo_routines/make_vetting_plots/plots'

    out_file = 'prelim_vetting_classes.csv'

    already_labled = [i.replace('.png', '') for i in os.listdir(plot_dir) if i!='.gitkeep']
    full_ids = [i for i in full_ids if i not in already_labled]

    if not os.path.exists(out_file): 
        with open(out_file, 'w') as f: 
            f.write('full_id,comment'+'\n')
    
    for number, full_id in enumerate(full_ids):
        with open(out_file, 'a') as f:  
            canidates_dict, labels_dict = hunter(full_id)

            annot = {'algo_labels':labels_dict['canidate_labels']}

            try: 
                        
                    make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annot) 

                    user_input = input(full_id+" THOUGHTS ("+str(len(full_ids)-number)+' left): ')

                    annot = {'algo_labels':labels_dict['canidate_labels'], 
                        'my_thoughts':user_input}

                    make_vetting_plot(full_id, canidates_dict=canidates_dict, annotations_dict=annot, plot_dir=plot_dir) 

                    f.write(full_id+','+user_input+'\n')

            except: 
                print('ERROR WITH: '+full_id)
                continue 

            finally: 
                continue 

            # get user input, remake plot adding user input to the ax_dict['F'], and save without showing 

def initial_pass_runner(): 
    from qpo_vetting_modules import hunter, make_vetting_plot, initial_pass

    initial_pass() 

def review(): 
    from qpo_vetting_modules import reviewing_with_steiner

    reviewing_with_steiner()

#vetting_with_comments_run()
#initial_pass_runner() 
review()