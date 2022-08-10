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
fracdisk = []
fracscat = []
disktemp = []
fluxes = []

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
                    if 'FracSctr' in line: 
                        scatteredfraction = str(line)
                    if 'Tin' in line:
                        disktemperature = str(line)
                
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

                scatteredfraction = re.sub(' +',',',scatteredfraction)
                scatteredfractionlist = scatteredfraction.split(',')
                scafra = float(scatteredfractionlist[5])
                scafra = round(scafra,4)
                fracscat.append(scafra*100)

                diskfraction = 1-scafra
                diskfraction = round(diskfraction,4)
                diskfraction = diskfraction*100
                fracdisk.append(diskfraction)

                disktemperature = re.sub(' +',',',disktemperature)
                disktemperaturelist = disktemperature.split(',')
                dtemp = float(disktemperaturelist[6])
                dtemp = round(dtemp,4)
                disktemp.append(dtemp)
            #Get unabs fluxes
            fluxfile = '/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+test+'cflux.log'
            with open(fluxfile,'r') as f:
                for line in f:
                    if 'lg10Flux' in line:
                        line = re.sub(' +',',',line)
                        linelist = line.split(',')
                        flux = float(linelist[6])
                        fluxes.append(flux)
#convert lists to numpy arrays 
MJD = np.array([MJD])
gammalist = np.array([gammalist])
pg = np.array([pg])
fracdisk = np.array([fracdisk])
fracscat = np.array([fracscat])
disktemp = np.array([disktemp])
fluxes = np.array([fluxes])

#Set up figure 
fig, axs = plt.subplots(3,1,sharex=True)
fig.subplots_adjust(hspace=0)

'''
axs[0].plot(MJD,fluxes,color='black',marker='o')
axs[0].set_ylabel('Unabsorbed Flux')
fluxmin = round(fluxes.min(),0)-1
fluxmax = round(fluxes.max(),0)+1
axs[0].set_ylim([fluxmin,fluxmax])
axs[0].set_yticks(np.arange(fluxmin,fluxmax,0.75))

axs[1].plot(MJD,fracdisk,color='blue',marker='o')
axs[1].set_ylabel('Disk Frac. (%)')
axs[1].set_ylim([0,100])
axs[1].set_yticks(np.arange(0,100,25))

axs[2].plot(MJD,fracscat,color='red',marker='o')
axs[2].set_ylabel('Scattered Frac. (%)')
axs[2].set_ylim([0,100])
axs[2].set_yticks(np.arange(0,100,25))
'''
axs[0].plot(MJD,disktemp,color='blue',marker='o')
axs[0].set_ylabel('kTin (KeV)')
disktempmin = round(disktemp.min(),1)-0.1
disktempmax = round(disktemp.max(),1)+0.1
axs[0].set_ylim([disktempmin,disktempmax])
axs[0].set_yticks(np.arange(disktempmin,disktempmax,0.1))

axs[1].plot(MJD,gammalist,color='red',marker='o')
axs[1].set_ylabel('Γ')
gammamin = round(gammalist.min(),1)-0.2
gammamax = round(gammalist.max(),0)+0.2
axs[1].set_ylim([gammamin,gammamax])
axs[1].set_yticks(np.arange(gammamin,gammamax,0.2))

axs[2].plot(MJD,pg,color='black',marker='o')
axs[2].set_ylabel('Red. pgstat')
axs[2].set_ylim([0.9,1.3])
axs[2].set_yticks(np.arange(0.9,1.3,0.1))

plt.show()
