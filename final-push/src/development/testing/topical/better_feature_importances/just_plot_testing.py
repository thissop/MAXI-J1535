import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

df = pd.DataFrame()

df['x'] = [4]
df['y'] = [3]
df['z'] = [7]

fig, ax = plt.subplots(figsize=(4,4))

sns.barplot(data=df, yerr=[0.25, 0.3, 0.4], edgecolor='black', linewidth=0.75, errwidth=10, capsize=10)

fig.tight_layout()

plt.savefig('/ar1/PROJ/fjuhsd/personal/thaddaeus/github/MAXI-J1535/final-push/src/development/testing/topical/better_feature_importances/temp.png', dpi=150)

