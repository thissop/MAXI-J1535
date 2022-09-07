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