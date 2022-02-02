export HEADAS=/mnt/c/Users/Research/Downloads/heasoft-6.29/x86_64-pc-linux-gnu-libc2.31/
. $HEADAS/headas-init.sh
alias heainit=". $HEADAS/headas-init.sh"

xspec 
data /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0.jsgrp
none
none
backgrnd /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0.bg
response /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/nicer_d49_55575341.rmf
arf /mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/nicer_d49_55575341.arf
ignore **-0.5 1.5-2.3 10.0-**
ignore bad
source /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/common.tcl
statistic pgstat
setp back on
energies 0.01 200. 1000 log
model tbabs(simpl(diskbb))
3.2107 , 2 2 5 5
2.0 0.05 1.1 1.4 3.5 4.0
0.1 0.1 0.001 0.01 0.9 1.0
1
, , 0.2 0.2 2 3
, , 0.1 0.1 1000000000 1000000000
freeze 1
chatter 5 10
parallel leven 2
fit 250
n

tclout stat
scan $xspec_tclout "%f" pgstat
tclout dof
scan $xspec_tclout "%f" dof
set redpgstat [expr $pgstat / $dof]
log /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/logs/1050360103_0_before_error.txt
show data
show param
show fit