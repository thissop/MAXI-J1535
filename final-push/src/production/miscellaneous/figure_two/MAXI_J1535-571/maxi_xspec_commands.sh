xspec
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
chatter 5 10
parallel leven 2
fit 750
n

chatter 10
show fit

show param 

notice 1.1-2.9

cpd \xs 
setplot energy
plot ldata chi
iplot 
time off
font roman
label top 
