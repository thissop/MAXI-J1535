#This is just an excerpt, hence lots of variables are undefined

fig, axs = plt.subplots(6,1,sharex=True)
fig.subplots_adjust(hspace=0)

axs[0].plot(MJD,fluxes,color='blue',marker='o')
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

axs[3].plot(MJD,disktemp,color='blue',marker='o')
axs[3].set_ylabel('kTin (KeV)')
disktempmin = round(disktemp.min(),1)-0.1
disktempmax = round(disktemp.max(),1)+0.1
axs[3].set_ylim([disktempmin,disktempmax])
axs[3].set_yticks(np.arange(disktempmin,disktempmax,0.3))

axs[4].plot(MJD,gammalist,color='blue',marker='o')
axs[4].set_ylabel('Γ')
gammamin = round(gammalist.min(),1)-0.2
gammamax = round(gammalist.max(),0)+0.2
axs[4].set_ylim([gammamin,gammamax])
axs[4].set_yticks(np.arange(gammamin,gammamax,0.4))

axs[5].plot(MJD,pg,color='blue',marker='o')
axs[5].set_ylabel('Red. pgstat')
axs[5].set_ylim([0.9,1.3])
axs[5].set_yticks(np.arange(0.9,1.3,0.1))

plt.show()
