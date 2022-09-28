heainit

cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/MAXI_J1535-571/regression/qpo/jspipe_qpo/1050360105

xspec
chatter 0
data /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/MAXI_J1535-571/regression/qpo/jspipe_qpo/1050360105/js_ni1050360105_0mpu7_silver_GTI21-bin.pds

ignore **-1.0 20.0-**

model loren
0


freeze 1 
query yes 
fit

editmod loren+loren 
2.5907466334881044
0.284944
0.0044122

editmod loren+loren+loren 
5.026860711845576
0.550002
0.00101799

freeze 4-9

fit

cpd /ps
setplot energy
plot data
iplot 
label bottom Frequency (Hz)
label left Power (rms Normalized)
label top
font roman
t off
View 0.12 0.12
csize 2.0
rescale x 1. 15.
log y
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/1050360105_21[pds-data].ps/ps
quit 
plot model 
iplot
label top
font roman
t off
label X Frequency (Hz)
label Y Power (rms Normalized)
View 0.12 0.12
csize 2.0
rescale x 1. 15.
log y
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/1050360105_21[pds-model].ps/ps
quit
quit
y

cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/

xspec 
chatter 0
data /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360105/jspipe/js_ni1050360105_0mpu7_silver_GTI21.jsgrp
arf /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus//mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/nicer_d49_55575341.arf
ignore **-0.5 1.5-2.3 10.0-**
ignore bad
setp back on
model tbabs(diskbb+nthcomp)
3.2107 , 2 2 5 5
, , 0.2 0.2 2 3
, , 0.1 0.1 1000000000 1000000000
, , 1.1 1.2 3.5 4
50
=p2
1
0

freeze 1 5

query yes 
fit

notice 0.5-10.0
cpd /VPS
setplot energy 
plot data 
iplot 
font roman
t off
label top
View 0.12 0.12
csize 2.0
rescale x 0.5 10.
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/1050360105_21[spectrum-data].ps/ps
1050360105_21[spectrum-data]/ps
hard 1050360105_21[spectrum-data].ps/ps
quit

plot model 
iplot
font roman
t off
label top
View 0.12 0.12
csize 2.0
rescale x 0.5 20.
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/1050360105_21[spectrum-model].ps/ps
1050360105_21[spectrum-model]/ps
hard 1050360105_21[spectrum-model].ps/ps
quit 
quit
y 

python 
import os 

dir = '/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/manuscript/figures/figure_two/MAXI_J1535-571/'

old_plots = ['1050360105_21[pds-data].ps', '1050360105_21[pds-model].ps', '1050360105_21[spectrum-model].ps', '1050360105_21[spectrum-data].ps']

for f in old_plots: 
    os.system(f"ps2pdf {dir+f} {dir+f.replace('.ps','.pdf')}")
    os.remove(f"{dir+f}")

quit()

