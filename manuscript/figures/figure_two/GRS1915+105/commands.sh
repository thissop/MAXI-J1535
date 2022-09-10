heainit
xspec
cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/40116-01-01-07

data power_0_249.pha

model loren
0


freeze 1
query yes 

fit 

editmod loren+loren 
1.592
0.187
13.724
freeze 4-6
fit
ignore **-0.1
ignore 10.0-**
cpd /ps
setplot energy
plot data
iplot 
label bottom Frequency (Hz)
label left Power (Leahy Normalized)
label top
font roman
t off
View 0.12 0.12
csize 2.0
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[pds-data].ps/ps
quit 
plot model 
iplot
label top
font roman
t off
label X Frequency (Hz)
label Y Power (Leahy Normalized)
View 0.12 0.12
csize 2.0
rescale x 0.1 10
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[pds-model].ps/ps
quit
quit
y

cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/40116-01-01-07

xspec 
chatter 0
data /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/spectral/external_spectra/40116-01-01-07/src_pcu2.pha
model tbabs*(diskbb+nthcomp)
/*
query yes 
ignore **-2.5 30.0-**
fit 

setplot energy 
cpd /VPS
plot data 
iplot 
font roman
t off
label top
View 0.12 0.12
csize 2.0
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-data].ps/ps
quit


plot model 
iplot
font roman
t off
label top
View 0.12 0.12
csize 2.0
hard  /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-model].ps/ps
quit 
quit
y 

ps2pdf "/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-model].ps" "/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-model].pdf"
ps2pdf "/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-data].ps" "/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/40116-01-01-07[spectrum-data].pdf"

python 
import os 

dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/GRS1915+105/'

old_plots = ['40116-01-01-07[spectrum-model].ps', '40116-01-01-07[spectrum-data].ps', '40116-01-01-07[pds-model].ps', '40116-01-01-07[pds-data].ps']

for f in old_plots: 
    os.system(f"ps2pdf {dir+f} {dir+f.replace('.ps','.pdf')}")
    os.remove(f"{dir+f}")

quit()

