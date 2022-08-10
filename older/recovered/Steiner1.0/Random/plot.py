import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
csv = '/home/thaddaeus/Spectral Evolution of MAXI J1535-571 - Sheet1.csv'
df = pd.read_csv(csv,names=['ObsID','MJD','Net Count Rate (cts/s)','nH *(10^22)','nH lower limit','nH upper limit','Photon Index','Photon Index Lower','Photon Index Upper','diskbb Tin','Tin Lower','Tin Upper','cflux (0.6-10) - cgs','red chi'])
#df.plot(kind='line',x='MJD',y='Photon Index', marker='o',color='blue')
x1 = df['MJD'].tolist()
y1 = df['Photon Index'].tolist()
#x2 = [58004.34,58007.27,58008.26,58009.01,58010.93,58011.39,58012.12]
#y2 = [1.54,1.9,1.91,2.03,1.94,1.96,1.96]
#y2 = [1.022,1.0784,1.304,1.83,1.5,1.46,1.47,1.39,1.47]
y2 = df['red chi'].tolist()
'''
plt.plot(x1,y1,color='k',label='mine')
plt.plot(x1,y2,color='g',label='swift')
plt.xlim([58004,58013])
plt.ylim([1.4,2.3])
plt.xticks(np.arange(58004,58013,1))
plt.yticks(np.arange(1.4,2.5,0.3))
plt.show()
'''
plt.figure()
plt.subplot(211)
plt.plot(x1,y1,color='tab:blue',marker='o',label='Nicer Pipeline Fits')
plt.xlabel('MJD')
plt.ylabel('Photon Index')
plt.title('Results from Best Fitting Models')
plt.xlim([58004,58020])
plt.ylim([1,2.3])
plt.xticks(np.arange(58004,58020,3))
plt.yticks(np.arange(1,2.5,0.3))

x2 =[58005.304,58008,58008.98,58010,58011.865,58012.187,58013.216,58014.053,58019.006]
plt.subplot(212)
plt.plot(x2,y2,color='red',marker='o')
plt.xlabel('MJD')
plt.ylabel('υ')
plt.title('Reduced Chi Square')
plt.xlim([58004,58020])
plt.ylim([1,2])
plt.xticks(np.arange(58004,58020,3))
plt.yticks(np.arange(0.9,2,0.3))
plt.subplots_adjust(hspace=0.5)
plt.show()

