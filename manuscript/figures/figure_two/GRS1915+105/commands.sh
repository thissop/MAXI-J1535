heainit
xspec
cd /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/GRS_1915+105/qpo/external_PDS/40116-01-01-07

data power_0_249.pha

model loren+loren
0

0


freeze 1 4
query yes 

fit 

editmod loren+loren+loren 
1.592
0.187
13.724
freeze 7-9
fit
ignore **-0.1
ignore 10.0-**
setplot energy
plot data chi
iplot 
label bottom Frequency (Hz)
label left Power ()
label top
font roman
t off
co 4 on 2
#r y1 80 120
hard test.png/png
quit
quit
y

