import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns

plt.style.use('/mnt/c/Users/Research/Documents/GitHub/QPOML/qpoml/stylish-3.mplstyle')

sns.set_context('paper', font_scale=2.7)

df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_QPO-Input.csv')
df = df.merge(pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/regression/GRS_1915+105_Scalar-Input.csv'), on='observation_ID')
df = df.drop(columns=['observation_ID'])

fig, ax = plt.subplots(figsize=(5,5))

ax = sns.pairplot(df, corner=True)

fig.tight_layout()

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_eleven/qpo_pairplot.png', dpi=250)