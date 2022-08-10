import numpy as np
import pandas as pd
import re 
import matplotlib.pyplot as plt
import os, shutil
import astropy 
from astropy.io import fits

key = 'IDs.txt'

MJD = []
gammalist = []
pg = []

#For -2
with open(key,'r') as key:
    for line in key:
        test = str(line)
        test = test.replace('\n','')
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+test+'.log'):
            #print(test)
            orig = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+test+'/jspipe/js_ni'+test+'_0mpu7_silver_GTI0.jsgrp'
            target = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+test+'/jspipe/js_ni'+test+'_0mpu7_silver_GTI0.fits'
            shutil.copyfile(orig,target)
            hdul = fits.open(target)
            bap = hdul[1].header['MJDSTART']
            #print(bap)
            MJD.append(bap)
            os.remove(target)
            
            raw = '/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+test+'.log'
            with open(raw,'r') as r:
                for line in r: 
                    if 'Gamma' in line:
                        raw = str(line)
                    if 'PG-Statistic' in line:
                        pgstatr = str(line)
                    if 'degrees of freedom' in line: 
                        dofr = str(line)

                raw = re.sub(' +',',',raw)
                rawlist = raw.split(',')
                gamma = float(rawlist[5])
                gammalist.append(gamma)

                pgstatr = re.sub(' +',',',pgstatr)
                pgstatl = pgstatr.split(',')
                pgstat = pgstatl[4]
                dofr = re.sub(' +',',',dofr)
                dofl = dofr.split(',')
                dof = dofl[7]

                redpg = round((float(pgstat)/int(dof)),3)
                pg.append(redpg)
    
xmin = round(min(MJD),0)-1
xmax = round(max(MJD),0)+1

gammamin = round(min(gammalist),1)-0.1
gammamax = round(max(gammalist),1)+0.1
pgstatmin = round(min(pg),1)-0.2
pgstatmax = round(max(pg),1)+0.2


MJD = np.array([MJD])
gammalist = np.array([gammalist])
pg = np.array([pg])
plt.figure()
plt.subplot(211)
plt.plot(MJD,gammalist,color='blue',marker='o',label='Nicer Pipeline Fits')
plt.xlabel('MJD')
plt.ylabel('Photon Index')
plt.title('Results from Best Fitting Models')
plt.xlim([xmin,xmax])
plt.ylim([gammamin,gammamax])
plt.xticks(np.arange(xmin,xmax,2))
plt.yticks(np.arange(gammamin,gammamax,0.2))

plt.subplot(212)
plt.plot(MJD,pg,color='red',marker='o')
plt.xlabel('MJD')
plt.ylabel('χ2/υ')
plt.title('Reduced PG Stat')
plt.xlim([xmin,xmax])
plt.ylim([pgstatmin,pgstatmax])
plt.xticks(np.arange(xmin,xmax,2))
plt.yticks(np.arange(pgstatmin,pgstatmax,0.2))
plt.subplots_adjust(hspace=0.5)
plt.show()

'''



raw = '/home/thaddaeus/xspec.log'
out = 'extract.txt'
MJD = [58020.566]
x2 = []
for element in MJD:
    x2.append(element)

#extract information from single file 
with open(raw,'r') as r:
    for line in r: 
        if 'PhoIndex' in line:
            raw = str(line)
        if 'PG-Statistic' in line:
            pgstatr = str(line)
        if 'degrees of freedom' in line: 
            dofr = str(line)

raw = re.sub(' +',',',raw)
rawlist = raw.split(',')
gamma = float(rawlist[5])

pgstatr = re.sub(' +',',',pgstatr)
pgstatl = pgstatr.split(',')
pgstat = pgstatl[4]

dofr = re.sub(' +',',',dofr)
dofl = dofr.split(',')
dof = dofl[7]

redpg = round((float(pgstat)/int(dof)),3)

y1 = []
y1.append(gamma)
y2 = []
y2.append(redpg)
print(y1)



#plot 

xmin = float(min(MJD))-1
xmax = float(min(MJD))+1
gammamin = float(min(y1))-0.25
gammamax = float(max(y1))+0.25
pgstatmin = float(min(y2))-0.25
pgstatmax = float(max(y2))+0.25

plt.figure()
plt.subplot(211)
plt.plot(MJD,y1,color='blue',marker='o',label='Nicer Pipeline Fits')
plt.xlabel('MJD')
plt.ylabel('Photon Index')
plt.title('Results from Best Fitting Models')
plt.xlim([xmin,xmax])
plt.ylim([gammamin,gammamax])
plt.xticks(np.arange(xmin,xmax,3))
plt.yticks(np.arange(gammamin,gammamax,0.3))

plt.subplot(212)
plt.plot(MJD,y2,color='red',marker='o')
plt.xlabel('MJD')
plt.ylabel('χ^2 / υ')
plt.title('Reduced PG Stat')
plt.xlim([xmin,xmax])
plt.ylim([pgstatmin,pgstatmax])
plt.xticks(np.arange(xmin,xmax,3))
plt.yticks(np.arange(pgstatmin,pgstatmax,0.3))
plt.subplots_adjust(hspace=0.5)
plt.show()
'''


'''
#last wroking ish \/
import numpy as np
import pandas as pd
import re 
import matplotlib.pyplot as plt
import os, shutil
import astropy 
from astropy.io import fits

key = 'IDs.txt'

MJD = []
gammalist = []
pg = []
keylist = []
#For -2
with open(key,'r') as key:
    for line in key:
        test = str(line)
        test = test.replace('\n','')
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+test+'.log'):
            #print(test)
            orig = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+test+'/jspipe/js_ni'+test+'_0mpu7_silver_GTI0.jsgrp'
            target = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+test+'/jspipe/js_ni'+test+'_0mpu7_silver_GTI0.fits'
            shutil.copyfile(orig,target)
            hdul = fits.open(target)
            bap = hdul[1].header['MJDSTART']
            #print(bap)
            MJD.append(bap)
            os.remove(target)
            keylist.append(test)
for test in keylist:    
    raw = '/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+test+'.log'
    with open(raw,'r') as r:
        for line in r: 
            if 'Gamma' in line:
                rawline = str(line)
                #print(rawline)
            if 'PG-Statistic' in line:
                pgstatr = str(line)
            if 'degrees of freedom' in line: 
                dofr = str(line)
        rawline = re.sub(' +',',',rawline)
        rawlist = rawline.split(',')
        #print(rawlist)
        gamma = float(rawlist[5])
        gammalist.append(gamma)

        pgstatr = re.sub(' +',',',pgstatr)
        pgstatl = pgstatr.split(',')
        pgstat = pgstatl[4]
        dofr = re.sub(' +',',',dofr)
        dofl = dofr.split(',')
        dof = dofl[7]

        redpg = round((float(pgstat)/int(dof)),3)
        pg.append(redpg)

xmin = round(min(MJD),0)-1
xmax = round(max(MJD),0)+1

gammamin = round(min(gammalist),1)-0.1
gammamax = round(max(gammalist),1)+0.1
pgstatmin = round(min(pg),1)-0.2
pgstatmax = round(max(pg),1)+0.2


MJD = np.array([MJD])
gammalist = np.array([gammalist])
pg = np.array([pg])
plt.figure()
plt.subplot(211)
plt.plot(MJD,gammalist,color='blue',marker='o',label='Nicer Pipeline Fits')
plt.xlabel('MJD')
plt.ylabel('Photon Index')
plt.title('Results from Best Fitting Models')
plt.xlim([xmin,xmax])
plt.ylim([gammamin,gammamax])
plt.xticks(np.arange(xmin,xmax,2))
plt.yticks(np.arange(gammamin,gammamax,0.2))

plt.subplot(212)
plt.plot(MJD,pg,color='red',marker='o')
plt.xlabel('MJD')
plt.ylabel('χ2/υ')
plt.title('Reduced PG Stat')
plt.xlim([xmin,xmax])
plt.ylim([pgstatmin,pgstatmax])
plt.xticks(np.arange(xmin,xmax,2))
plt.yticks(np.arange(pgstatmin,pgstatmax,0.2))
plt.subplots_adjust(hspace=0.5)
plt.show()
'''
'''



raw = '/home/thaddaeus/xspec.log'
out = 'extract.txt'
MJD = [58020.566]
x2 = []
for element in MJD:
    x2.append(element)

#extract information from single file 
with open(raw,'r') as r:
    for line in r: 
        if 'PhoIndex' in line:
            raw = str(line)
        if 'PG-Statistic' in line:
            pgstatr = str(line)
        if 'degrees of freedom' in line: 
            dofr = str(line)

raw = re.sub(' +',',',raw)
rawlist = raw.split(',')
gamma = float(rawlist[5])

pgstatr = re.sub(' +',',',pgstatr)
pgstatl = pgstatr.split(',')
pgstat = pgstatl[4]

dofr = re.sub(' +',',',dofr)
dofl = dofr.split(',')
dof = dofl[7]

redpg = round((float(pgstat)/int(dof)),3)

y1 = []
y1.append(gamma)
y2 = []
y2.append(redpg)
print(y1)



#plot 

xmin = float(min(MJD))-1
xmax = float(min(MJD))+1
gammamin = float(min(y1))-0.25
gammamax = float(max(y1))+0.25
pgstatmin = float(min(y2))-0.25
pgstatmax = float(max(y2))+0.25

plt.figure()
plt.subplot(211)
plt.plot(MJD,y1,color='blue',marker='o',label='Nicer Pipeline Fits')
plt.xlabel('MJD')
plt.ylabel('Photon Index')
plt.title('Results from Best Fitting Models')
plt.xlim([xmin,xmax])
plt.ylim([gammamin,gammamax])
plt.xticks(np.arange(xmin,xmax,3))
plt.yticks(np.arange(gammamin,gammamax,0.3))

plt.subplot(212)
plt.plot(MJD,y2,color='red',marker='o')
plt.xlabel('MJD')
plt.ylabel('χ^2 / υ')
plt.title('Reduced PG Stat')
plt.xlim([xmin,xmax])
plt.ylim([pgstatmin,pgstatmax])
plt.xticks(np.arange(xmin,xmax,3))
plt.yticks(np.arange(pgstatmin,pgstatmax,0.3))
plt.subplots_adjust(hspace=0.5)
plt.show()
'''