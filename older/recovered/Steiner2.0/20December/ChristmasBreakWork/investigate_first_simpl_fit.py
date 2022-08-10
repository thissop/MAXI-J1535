#Import(s)
import os
from personalastropy.xspectools.XSPECtoolsv2 import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

report_file = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/in_between_run/rpg 1.975(simpl).txt'

initial_ids = []

log_temp = '/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/in_between_run/logs/simpl++++++++++_+.log'

with open('/home/thaddaeus/FMU/Steiner/ChristmasBreak/all_seg_ids.txt','r') as f:
    for line in f:
        line = line.replace('\n','')
        line_list = line.split('_')
        obsid = line_list[0]
        gti = line_list[1]
        test_file = log_temp.replace('++++++++++',obsid)
        test_file = test_file.replace('+',gti)
        if os.path.exists(test_file):
            initial_ids.append(line)

rpgs = []
bap = []
returnFitResults(IDs=initial_ids,path_temp=log_temp,fit_stat='pgstat',fit_params=['diskbb:Tin:6'],out_lists=[bap],rfsl=rpgs)

rpgs_only = []
with open(report_file,'w') as f:
    for item in rpgs: 
        item_list = item.split(':')
        rpg = float(item_list[1])
        rpgs_only.append(rpg)
        if rpg < 2:
            f.write(item_list[0]+'\n')

'''
plt.hist(rpgs_only)
plt.xlabel(r'$\chi^{2}/\nu$')
plt.ylabel('Count')
plt.show()
'''

