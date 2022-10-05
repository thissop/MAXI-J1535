def fix_order(): 

    import pandas as pd
    import numpy as np

    scalar_context_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/input.csv'
    qpo_path = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/output.csv'

    input_df = pd.read_csv(scalar_context_path)
    qpo_df = pd.read_csv(qpo_path)

    merged_df = input_df.merge(qpo_df, on='observation_ID')

    qpo_df = pd.DataFrame()
    qpo_df['observation_ID'] = merged_df['observation_ID']
    qpo_df['qpo_state'] = merged_df['qpo_state']

    qpo_df.to_csv(qpo_path, index=False)
    merged_df = merged_df.drop(columns=['qpo_state'])
    merged_df.to_csv(scalar_context_path, index=False)

def make_it_three_class(): 
    import pandas as pd 
    import numpy as np

    df1 = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_QPO-Input.csv')

    drop_columns =  ['first_rms_power', 'second_rms_power', 'third_rms_power']

    df2 = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/older/data/processed/2022/new_current_qpos.csv').drop(columns=drop_columns)

    merged = df1.merge(df2, on='observation_ID')

    print(len(np.where(merged['qpo_state']>0)[0]))
    print(len(merged.index))

    print(len(np.where(merged['num_qpos']==1)[0]))

    print(list(set(merged['confidence_class'])))

    drop = np.setdiff1d(list(merged), ['observation_ID', 'num_qpos'])
    merged = merged.drop(columns=drop)

    merged['num_qpos'] = np.array(merged['num_qpos']).astype(int)

    merged.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_QPO-multiclass.csv', index=False)

make_it_three_class()