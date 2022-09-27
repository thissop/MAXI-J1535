def merge_them(): 

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

    merged = merged.drop(columns=['confidence_class', 'qpo_state', 'num_qpos'])

    merged.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/re-incorporate-maxi-qpos/test.csv', index=False)

merge_them()

def split_to_rows(): 
    import numpy as np
    fp = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/re-incorporate-maxi-qpos/test.csv'
    header = ','.join(['observation_ID', 'frequency', 'width', 'normalization'])
    lines = []
    with open(fp, 'r') as f: 
        for line in f: 
            if 'observation_ID' not in line: 
                line_list = np.array(line.split(','))
                obsid = line_list[0]
                lines.append(f'{obsid},{",".join(line_list[1:4])}')
                lines.append(f'{obsid},{",".join(line_list[4:7])}')
                #lines.append(f'{obsid},{",".join(line_list[7:10])}'.replace('\n', ''))

    with open(fp, 'w') as f: 
        f.write(header+'\n')
        for line in lines: 
            f.write(line+'\n')

split_to_rows()