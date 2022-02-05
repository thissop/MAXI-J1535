# /mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/jan-29-simpl/testing_xspec/pyxspec_test.py
import xspec 
from xspec import *
def first_test(obs_id): 
    
    jsgrp = '/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360103/jspipe/js_ni1050360103_0mpu7_silver_GTI0.jsgrp'
    s1 = Spectrum(jsgrp)
    print('all loaded')
first_test('')