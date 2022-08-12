data /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360105/jspipe/js_ni1050360105_0mpu7_silver_GTI21-bin.pds
none
response /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360105/jspipe/js_ni1050360105_0mpu7_silver_GTI21-fak.rsp
ignore **-1.0 20.0-**
query yes
cpd \xs
setplot energy
setplot xlog
plot data
iplot
label top
label bottom Frequency [Hz]
label left rms-Normalized Power
time off
font roman
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_two/1050360105_21_data.png/png
quit

model loren
0


freeze 1
fit
editmod loren+loren
0


freeze 1
fit
freeze 2
freeze 3
freeze 5
freeze 6
cpd \xs
setplot energy
setplot xlog
plot ldata

iplot

label top
label bottom Frequency [Hz]
label left rms-Normalized Power
time off
font roman
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_two/1050360105_21_background_ldata.png/png
quit


editmod loren+loren+loren
2.5,2 2 3 3


editmod loren+loren+loren+loren
5,4 4 6 6



fit
cpd \xs
setplot energy
setplot xlog
plot model
iplot
label top
label bottom Frequency [Hz]
label left rms-Normalized Power
time off
font roman
hard /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/miscellaneous/figure_two/1050360105_21_model.png/png
quit

