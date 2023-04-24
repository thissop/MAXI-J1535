import matplotlib.pyplot as plt 

import matplotlib as mpl

#mpl.rcParams['lines.linewidth']   = 2
#mpl.rcParams['axes.linewidth']    = 2
#mpl.rcParams['xtick.major.width'] = 2
#mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.labelsize']   = 13
mpl.rcParams['xtick.labelsize']   = 13
mpl.rcParams['axes.labelsize']    = 13
#mpl.rcParams['legend.numpoints']  = 1
#mpl.rcParams['axes.labelweight']  = 'semibold'
mpl.rcParams['axes.titlesize']    = 13
#mpl.rcParams['axes.titleweight']  = 'semibold'
#mpl.rcParams['font.weight']       = 'semibold'

fig, ax = plt.subplots()

ax.scatter([1], [3])
ax.set_xlabel('lol')
ax.set_ylabel('haha')

plt.savefig('referee-feedback/first-round/updated-pipeline/[medium]-temp.png')