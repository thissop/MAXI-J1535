#Import(s)
import os
from re import I
from personalastropy.xspectools.XSPECtoolsv2 import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Action

#Get IDs

sids = []
with open('/home/thaddaeus/FMU/Steiner2.0/20December/ChristmasBreakWork/FromOtherComp/in_between_run/rpg 1.975(simpl).txt','r') as f:
    for line in f:
        line = line.replace('\n','')
        line_list = line.split('_')
        obsid = line_list[0]
        gti = line_list[1]
        
        jsgrp_temp = '/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp'
        
        jsgrp_file = jsgrp_temp.replace('++++++++++',obsid)
        jsgrp_file = jsgrp_file.replace('+',gti)

        if os.path.exists(jsgrp_file)==True:
            sids.append(line)

count_rates = []
returnCountRates(IDs=sids,data_path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp',channel_ints=['50:299','300:999'],bg_path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.bg',out_list=count_rates)

count_rates_only = []

for item in count_rates:
    count_rate = float(item.split(':')[1])
    count_rates_only.append(count_rate)

dates = []
returnDates(IDs=sids,path_temp='/home/thaddaeus/FMU/Steiner2.0/permanent/data/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI+.jsgrp',out_list=dates)

dates_only = []
for item in dates:
    date = float(item.split(':')[1])
    dates_only.append(date)

fig, axs = plt.subplots(7,1,sharex=True)
for i in range(0,7):
    axs[i].tick_params(axis='both',which='major',labelsize=6)


axs[0].scatter(dates_only,count_rates_only,s=3,color='maroon',label='NICER (0.5-10 keV)')
axs[0].set_ylabel('Count rate (c/s)',fontsize=5)
axs[0].set_ylim(bottom=0)
#axs[0].set_xlim(,)
axs[0].set_yscale('symlog')
axs[0].set_yticks(ticks=[1,10,100,1000])
axs[0].legend(loc='upper right',fontsize=6)

axs[6].set_xlabel('Time (MJD)',fontsize=6)

#plt.subplots_adjust(hspace=0)
plt.show()

