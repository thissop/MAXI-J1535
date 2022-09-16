import matplotlib.pyplot as plt 
import numpy as np

fig, ax = plt.subplots()
x = np.arange(0,5,1)

ax.scatter(x,x)
ax.set(xlabel='X', ylabel='Y')
fig.supxlabel('model?')

fig.tight_layout()

plt.savefig('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/development/testing/topical/fixing_violin_figure/quick_test.png')