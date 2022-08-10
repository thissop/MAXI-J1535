import numpy as np
import matplotlib.pyplot as plt
import os
#  Noticed Channels:  21-50,75-238
#  ignore **-0.5 1.5-2.2 10.0-**

def calculate_count_rate(IDs,pathtemp,channel_intervals,outlist): #let it have functionality to take in which channels to find count rate 
    #Import(s)
    import numpy as np
    from astropy.io import fits
    import os
    import shutil
    #Action 
    for item in IDs:
        obsid = item
        path = pathtemp.replace('++++++++++',obsid)
        orig = path
        temp_file = path.replace('.jsgrp','(temp).fits') 
        shutil.copyfile(orig, temp_file)
        hdul = fits.open(temp_file)
        channels_list = hdul[1].data['CHANNEL']
        counts_list = hdul[1].data['COUNTS']
        exp_time = float(hdul[1].header['EXPOSURE'])
        
        restricted_counts_list = []

        for elem in channel_intervals:
            sub_interval = np.array([])
            l_index = int((elem.split(':'))[0])
            u_index = int((elem.split(':'))[1])
            sub_interval = list(counts_list[l_index:u_index])
            restricted_counts_list.extend(sub_interval)

        count_rate = sum(restricted_counts_list)/exp_time
        os.remove(temp_file)

        outlist.append((obsid+':'+str(count_rate))) 

id_list= []
with open('/home/thaddaeus/FMU/Steiner2.0/permanent/ALL_NICER_IDs.txt','r') as f:
    for line in f:
        if '#' not in line:
            if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+line.replace('\n','')+'/jspipe/js_ni'+line.replace('\n','')+'_0mpu7_silver_GTI0.jsgrp')== True:
                id_list.append(line.replace('\n',''))

testy = []
bappy = []

pathex = '/home/thaddaeus/FMU/Steiner/thaddaeus/++++++++++/jspipe/js_ni++++++++++_0mpu7_silver_GTI0.jsgrp'
calculate_count_rate(IDs=id_list,pathtemp=pathex,channel_intervals=['21:238'],outlist=testy)
calculate_count_rate(IDs=id_list,pathtemp=pathex,channel_intervals=['21:50','75:238'],outlist=bappy)

#plot
from personalastropy.xspectools import XSPECtools as xt
x = []
xt.returnDates(id_list,pathex,x)

y = []
y2 = []
for elem in testy:
    y.append(float((elem.split(':')[1])))
for elem in bappy:
    y2.append(float((elem.split(':')[1])))
x = np.array(x)
y = np.array(y)
y2 = np.array(y2)

plt.plot(x,y,linewidth=1,markersize=5,color='maroon',label='NICER (0.5-10 keV)')
plt.scatter(x,y,s=5,color='maroon')
plt.yscale('log')
plt.xlim(58000,58400)
plt.legend()
plt.ylabel("Count rate (c/s)")
plt.xlabel("Date (MJD)")
plt.show()