import pandas as pd 

df =  pd.read_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv')

new_df = pd.DataFrame()

'''
GRS
net_count_rate: A
gamma: B
nthcomp_norm: C
diskbb_tin: D
diskbb_norm: E
hardness: F

MAXI

A:simpl_FracScat
B:net_source_count_rate
C:tin_before_error
D:diskbb_norm_before_error
E:gamma_before_error
F:nthcomp_norm_before_error
G:hardness_ratio 

'''

# SORT TO SAME OUTPUT LETTER COLUMNS FOR EASE OF EXPLANATION

keep = ['A', 'B', 'D', 'E', 'F', 'G']
out_cols = ['A', 'B', 'C', 'D', 'E', 'F']

for i, j in zip(keep, out_cols):
    new_df[j] = df[i]

new_df.to_csv('final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv', index=False)

df =  pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv')

new_df = pd.DataFrame()

keep = ['B', 'C', 'D', 'E', 'F', 'G']
out_cols = ['A', 'B', 'C', 'D', 'E', 'F']

for i, j in zip(keep, out_cols):
    new_df[j] = df[i]

new_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/classification/MAXI_J1535-571_Scalar-Input.csv', index=False)