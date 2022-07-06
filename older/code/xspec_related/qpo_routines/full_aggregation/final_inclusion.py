from local_funcs import quick_plot, hunter
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import re

#current_df = pd.read_csv('./data/processed/2022/current_qpos.csv')
current_df = pd.read_csv('new_current.csv')

excluded_df = pd.read_csv('./code/xspec_related/qpo_routines/full_aggregation/april-9/temp.csv')

excluded_ids = np.array(excluded_df['id'])
excluded_thoughts = np.array(excluded_df['thoughts'])

for index in range(len(current_df.index)): 
    row = current_df.iloc[index].tolist()
    
    id = row[0]
    con_class = row[-1]
    
    if id in ['1130360105_3', '1130360103_3', '1130360105_1']:

    #if con_class == -1:
        
        comment = excluded_thoughts[np.where(excluded_ids==id)[0]][0]
        
        correct_answer = False

        canidates_dict, _ = hunter(id)

        quick_plot(full_id=id, canidates_dict=canidates_dict, message=comment) 

        while not correct_answer: 
            user_choice = input(id+": ")

            if user_choice == 'none': # return none for all features for that QPO 
                confidence_class = int(input(id+" (CC): "))
                new_row = [id, 0] + 12*[np.nan] + [confidence_class]

                current_df.loc[index] = new_row 
                correct_answer=True
            
            elif user_choice=='choose' or user_choice == 'choose.replot':
                if user_choice=='chose.replot': 
                    quick_plot(full_id=id, canidates_dict=canidates_dict, message=comment)
                
                qpos_to_keep = [int(i) for i in re.sub(' +', ' ', input('Enter QPO indices to keep: ')).split(' ')]

                num_qpos = len(qpos_to_keep)
                
                qpo_props = []

                for i in qpos_to_keep: # needs to be zero indexed! 
                    qpo_props.append(canidates_dict['canidate_freqs'][i])
                    qpo_props.append(canidates_dict['canidate_widths'][i])
                    qpo_props.append(canidates_dict['canidate_norms'][i])
                    qpo_props.append(canidates_dict['canidate_rms_powers'][i])

                confidence_class = int(input(id+" (CC): "))
                new_row = [id, num_qpos] + qpo_props + ((3-num_qpos)*4)*[np.nan] + [confidence_class]

                current_df.loc[index] = new_row 
                correct_answer = True

            elif user_choice == 'skip': 
                new_row = row[0:len(row)-1]+[-2]
                current_df.loc[index] = new_row
                correct_answer = True


            print(current_df.loc[index].tolist())

current_df.to_csv('new_new_current.csv', index=False)