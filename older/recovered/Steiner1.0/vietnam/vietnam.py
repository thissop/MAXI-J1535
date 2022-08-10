import astropy
import os
import shutil
import sys
import numpy as np
import pandas as pd
from scipy import stats
import re

# Fit routines


def lower_end_v2():
    out = 'commands.txt'
    obsids = ['1050360111', '1050360112']

    def log_and_plot(uno):
        f.write(
            'log /home/thaddaeus/FMU/Steiner/vietnam/goodexamplesofbadresiduals/logs/'+uno+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')

        f.write('plot ldata rat mod chi'+'\n')
        f.write('iplot'+'\n')
        f.write(
            'hard /home/thaddaeus/FMU/Steiner/vietnam/goodexamplesofbadresiduals/plots/'+uno+item+'/png'+'\n')
        f.write('quit'+'\n')

    def fitcommands(ignore):
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write(ignore+'\n')
        f.write('ignore 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('cpd /xs'+'\n')
        f.write('setplot energy'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbfeo*simpl(diskbb)'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.7 0.01 3.2 3.3 4.3 4.4'+'\n')
        f.write('newpar 2'+'\n')
        f.write('0.6 0.02 0.01 0.15 3 5'+'\n')
        f.write('newpar 3'+'\n')
        f.write('1 0.01 0.01 0.04 3 5'+'\n')
        f.write('newpar 5'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 6'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 8'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1-3'+'\n')
        f.write('fit'+'\n')
        f.write('thaw 1-3'+'\n')
        f.write('fit'+'\n')
        f.write('freeze 1-3'+'\n')
        f.write('fit'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('plot ldata rat mod chi'+'\n')
        f.write('\n')
    for item in obsids:
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
            '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
        bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
            item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
        rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open(out, 'a') as f:
            fitcommands('ignore **-0.3')
            log_and_plot('0.3:')

            f.write('ignore **-1.0'+'\n')
            f.write('chatter 5'+'\n')
            f.write('fit'+'\n')
            log_and_plot('1:')

            f.write('ignore **-2.3'+'\n')
            f.write('chatter 5'+'\n')
            f.write('fit'+'\n')
            log_and_plot('2.3:')

            f.write('quit'+'\n')
            f.write('y'+'\n')


def lower_end():
    out = 'commands.txt'
    obsids = ['1050360103', '1050360104',
              '1050360105', '1050360106', '1050360107']

    def log_and_plot(uno):
        f.write('log /home/thaddaeus/FMU/Steiner/vietnam/logs/' +
                uno+item+'.log'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')

        f.write('plot ldata rat mod chi'+'\n')
        f.write('iplot'+'\n')
        f.write('hard /home/thaddaeus/FMU/Steiner/vietnam/plots/' +
                uno+item+'/png'+'\n')
        f.write('quit'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
        f.write('\n')

    def fitcommands(ignore):
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write(ignore+'\n')
        f.write('ignore 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('cpd /xs'+'\n')
        f.write('setplot energy'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbfeo*simpl(diskbb)'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.7 0.01 3.2 3.3 4.3 4.4'+'\n')
        f.write('newpar 2'+'\n')
        f.write('0.6 0.02 0.01 0.15 3 5'+'\n')
        f.write('newpar 3'+'\n')
        f.write('1 0.01 0.01 0.04 3 5'+'\n')
        f.write('newpar 5'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 6'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 8'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('thaw 2-3'+'\n')
        f.write('fit'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('plot ldata rat mod chi'+'\n')
        f.write('\n')
    for item in obsids:
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
            '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
        bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
            item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
        rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open(out, 'a') as f:
            f.write('###'+item+'###'+'\n')
            f.write('##-No Lower End-##'+'\n')
            fitcommands('\n')
            log_and_plot('0')

            f.write('##-1 KeV Lower End-##'+'\n')
            fitcommands('ignore **-1.0'+'\n')
            log_and_plot('1')

            f.write('##-2.3 KeV Lower End-##'+'\n')
            fitcommands('ignore **-2.3'+'\n')
            log_and_plot('2.3')


def laos():
    import os
    obsids = []
    key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'

    def fitcommands():
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write('ignore **-2.3 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('cpd /xs'+'\n')
        f.write('setplot energy'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbfeo*simpl(diskbb)'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.7 0.01 3 3.1 4.2 4.3'+'\n')
        f.write('newpar 2'+'\n')
        f.write('0.6 0.02 0.01 0.05 1 1.2'+'\n')
        f.write('newpar 3'+'\n')
        f.write('1 0.01 0.01 0.4 1.3 1.8'+'\n')
        f.write('newpar 5'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 6'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 8'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1-3'+'\n')
        f.write('fit'+'\n')
        f.write('thaw 1-3'+'\n')
        f.write('fit'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')
        f.write('plot ldata rat mod chi'+'\n')
        f.write('\n')

    def log_and_quit():
        f.write(
            'log /home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/logs/'+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
    with open(key, 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+line+'/jspipe/js_ni'+line+'_0mpu7_silver_GTI0.jsgrp') == True:
                    # if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+line+'.log') == True:
                    obsids.append(line)
    for item in obsids:
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
            '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
        bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
            item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
        rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/laos.txt', 'a') as f:
            fitcommands()
            log_and_quit()
            print(obsids)


def cambodia():
    import os
    obsids = []
    key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'

    def fitcommands():
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write('ignore **-1. 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbfeo*simpl(diskbb)'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.7 0.01 3 3.1 4.8 5'+'\n')
        f.write('newpar 2'+'\n')
        f.write('0.6 0.02 0.01 0.05 1.8 2'+'\n')
        f.write('newpar 3'+'\n')
        f.write('1 0.01 0.01 0.4 1.3 1.8'+'\n')
        f.write('newpar 5'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 6'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 8'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1-3'+'\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit'+'\n')
        f.write('thaw 1-3'+'\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit'+'\n')
        f.write('\n')

    def log_and_quit():
        f.write('log /home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/logs(global,gti1-4)/'+GTI+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
    with open(key, 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+line+'/jspipe/js_ni'+line+'_0mpu7_silver_GTI0.jsgrp') == True:
                    # if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+line+'.log') == True:
                    obsids.append(line)
    for item in obsids:
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp') == True:
            GTI = 'GTI0_'
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/cambodia.txt', 'a') as f:
                fitcommands()
                log_and_quit()
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI1.jsgrp') == True:
            GTI = 'GTI1_'
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI1.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI1.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/cambodia.txt', 'a') as f:
                fitcommands()
                log_and_quit()
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI2.jsgrp') == True:
            GTI = 'GTI2_'
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI2.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI2.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/cambodia.txt', 'a') as f:
                fitcommands()
                log_and_quit()
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI3.jsgrp') == True:
            GTI = 'GTI3_'
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI3.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI3.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/cambodia.txt', 'a') as f:
                fitcommands()
                log_and_quit()
        if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI4.jsgrp') == True:
            GTI = 'GTI4_'
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI4.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI4.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/cambodia.txt', 'a') as f:
                fitcommands()
                log_and_quit()


def tbabs():
    import os
    obsids = []
    key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'

    def fitcommands():
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write('ignore **-2.2 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbabs*simpl(diskbb)'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.0 0.01 1.5 1.501 4.5 4.8'+'\n')
        f.write('newpar 2'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 3'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 5'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('thaw 1'+'\n')
        f.write('notice 1.0-10.0'+'\n')
        f.write('fit'+'\n')
        f.write('\n')

    def log_and_quit():
        f.write(
            'log /home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/logs(tbabsloosest2)/'+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
        f.write('\n')
    with open(key, 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                # if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+line+'/jspipe/js_ni'+line+'_0mpu7_silver_GTI0.jsgrp') == True:
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+line+'.log') == True:
                    obsids.append(line)
    for item in obsids:
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
            '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
        bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
            item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
        rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/tbabs.txt', 'a') as f:
            fitcommands()
            log_and_quit()
    print(obsids)


def relxill():
    import os
    obsids = []
    key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'

    def tbabs_fitcommands():
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write('ignore **-2.2 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbabs(simpl(diskbb))'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.6 0.01 1.5 1.501 4.5 4.8'+'\n')
        f.write('newpar 2'+'\n')
        f.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
        f.write('newpar 3'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 5'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('thaw 1'+'\n')
        f.write('notice 1.0-10.0'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('lmod relxill .'+'\n')
        f.write('editmod tbabs(simpl(diskbb+relxill))')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('=2'+'\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('-1'+'\n')
        f.write('\n')
        f.write('freeze 19'+'\n')
        f.write('thaw 11'+'\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('chatter 10'+'\n')
        f.write('show param'+'\n')
        f.write('show fit'+'\n')

    def tbfeo_fitcommands():
        f.write('xspec'+'\n')
        f.write('xsect vern'+'\n')
        f.write('abun wilm'+'\n')
        f.write('data ' + jsgrp)
        f.write('none'+'\n')
        f.write('none' + '\n')
        f.write(bg)
        f.write(rmf)
        f.write(arf)
        f.write('ignore **-2.2 10.0-**'+'\n')
        f.write('ignore bad'+'\n')
        f.write('query yes'+'\n')
        f.write('statistic pgstat'+'\n')
        f.write('setp back on'+'\n')
        f.write('model tbabs(simpl(diskbb))'+'\n')
        f.write('/*'+'\n')
        f.write('newpar 1'+'\n')
        f.write('3.0 0.01 1.5 1.501 4.5 5.0'+'\n')
        f.write('newpar 2'+'\n')
        f.write('2 0.02 1.3 1.4 3.2 4.5'+'\n')
        f.write('newpar 3'+'\n')
        f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
        f.write('newpar 5'+'\n')
        f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
        f.write('chatter 5'+'\n')
        f.write('freeze 1'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('thaw 1'+'\n')
        f.write('notice 1.0-10.0'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('lmod relxill .'+'\n')
        f.write('editmod tbabs(simpl(diskbb+relxill))'+'\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('86,3 5,,')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('=2'+'\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('-1'+'\n')
        f.write('\n')
        f.write('freeze 19'+'\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit'+'\n')
        f.write('\n')
        f.write('editmod tbfeo(simpl(diskbb+relxill))'+'\n')
        f.write('3.0 0.01 1.5 1.501 4.5 4.8'+'\n')
        f.write('0.6,0.001 0.05 2 3'+'\n')
        f.write('1,0.1 0.3 3 4'+'\n')
        f.write('\n')
        f.write('parallel leven 2'+'\n')
        f.write('fit'+'\n')

    def tbabs_log_and_quit():
        f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill/'+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
        f.write('\n')

    def tbfeo_plot_log_and_quit():
        f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/'+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')

        f.write('cpd /xs'+'\n')
        f.write('setplot energy'+'\n')
        f.write('plot ldata euf mod chi'+'\n')
        f.write('iplot'+'\n')
        f.write('hard /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/plots/'+item+'.png/png'+'\n')
        f.write('quit'+'\n')

        f.write('chatter 5'+'\n')
        f.write('editmod cflux*tbfeo(simpl(diskbb+relxill))'+'\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('freeze 4-26'+'\n')
        f.write('parallell leven 2'+'\n')
        f.write('fit'+'\n')
        f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/cflux'+item+'.log'+'\n')
        f.write('chatter 10'+'\n')
        f.write('show data'+'\n')
        f.write('show fit'+'\n')
        f.write('show param'+'\n')
        f.write('log none'+'\n')
        f.write('quit'+'\n')
        f.write('y'+'\n')
    with open(key, 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if int(line) != 2130360205:
                    if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log'):
                        obsids.append(line)
    for item in obsids:
        jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
            '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
        bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
            item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
        rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
        arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
        with open('/home/thaddaeus/FMU/Steiner/vietnam/relxill.txt', 'a') as f:
            tbfeo_fitcommands()
            tbfeo_plot_log_and_quit()
# Analysis / plotting routines


def find_medians():
    import re
    import statistics as stat
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pyplt
    #key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'
    x = []
    z = []
    nHs = []
    Fes = []
    Os = []
    with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/logs(tbabsloosest2)/'+line+'.log') == True:
                    # if os.path.isfile('/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+line+'.log') == True:
                    x.append(line)

    for elem in x:
        filename = '/home/thaddaeus/FMU/Steiner/vietnam/calibratingtbfeo/logs(tbabsloosest2)/' + \
            elem+'.log'
        #filename = '/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+elem+'.log'
        with open(filename, 'r') as f:
            for line in f:
                z.append(line)
            for element in z:
                if 'PG-Statistic' in element:
                    pgelem = re.sub(' +', ',', element)
                    pgelemlist = pgelem.split(',')
                    pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                if 'nH' in element:
                    '''
                    if 'TBfeo' in element:
                        Oindex = z.index(element) + 1
                        element = re.sub(' +',',',element)
                        linelist = element.split(',')

                        nH = float(linelist[6])
                        if 3.25 < nH < 4.25:
                            nHs.append(nH)

                        Oline = z[Oindex]
                        Oline = re.sub(' +',',',Oline)
                        if 'TBfeo' in Oline:
                            Olist = Oline.split(',')
                            Oxy = float(Olist[5])
                            if 0.8> Oxy > 0.3 and 0.6 <pgstat < 3:
                                if Oxy != 0.200000: 
                                    Os.append(Oxy)

                        Feline = z[Oindex+1]
                        Feline = re.sub(' +',',',Feline)
                        if 'TBfeo' in Feline:
                            Felist = Feline.split(',')
                            Feval = float(Felist[5])
                            if 1.6 > Feval > 0.4:
                                Fes.append(Feval)
                    '''
                    element = re.sub(' +', ',', element)
                    linelist = element.split(',')
                    nH = float(linelist[6])
                    if 0.98 < pgstat < 1.25:
                        nHs.append(nH)

            z.clear()

    nHs = np.array(nHs)
    Os = np.array(Os)
    Fes = np.array(Fes)

    # print(nHs)
    '''
    print(np.percentile(nHs,[25,50,75]))
    print(stat.mean(nHs))

    print(np.percentile(Os,[25,50,75]))
    print(stat.mean(Os))

    print(np.percentile(Fes,[25,50,75]))
    print(stat.mean(Fes))
    '''
    # plot nh histogram

    def first_plot_method():
        fig, ax = plt.subplots(1, 1)
        ax.hist(nHs, density=True, bins=12, color='dimgrey')
        ax.set_title(
            'Normalized Histogram of nH Values with Centered Gaussian')
        ax.set_xlabel('nH')
        xt = plt.xticks()[0]
        xmin, xmax = min(xt), max(xt)
        lnspc = np.linspace(xmin, xmax, len(nHs))
        m, s = stats.norm.fit(nHs)  # get mean and standard deviation
        # now get theoretical values in our interval
        pdf_g = stats.norm.pdf(lnspc, m, s)
        ax.plot(lnspc, pdf_g)
        # ax.legend(['Gaussian'])

        ax.legend([r'$\mu$'+'='+str(m.round(2))+', ' +
                   r'$\sigma$'+'='+str(s.round(2))])
        # ax.text(4.5,0.9,'N. Obs: '+str(len(deg2$'+'/'+r'$\nu < 1.25$'))
        #ax.legend(((lnspc,pdf_g),(lnspc,pdf_gamma),(lnspc,pdf_beta)),('Norm','Gamma','Beta'),loc='upper right')
        plt.xticks
        plt.show()
    first_plot_method()
    '''
    def normed_hist():
        pyplt.hist(nHs, density=True)#,color='blue')
        xt = pyplt.xticks()[0]  
        xmin, xmax = min(xt), max(xt)  
        lnspc = np.linspace(xmin, xmax, len(nHs))
        m, s = stats.norm.fit(nHs) # get mean and standard deviation  
        pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
        pyplt.plot(lnspc, pdf_g, label="Norm")
        pyplt.title('nH')
        
        ag,bg,cg = stats.gamma.fit(nHs)  
        pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
        pyplt.plot(lnspc, pdf_gamma, label="Gamma")
        
        ab,bb,cb,db = stats.beta.fit(nHs)  
        pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
        pyplt.plot(lnspc, pdf_beta, label="Beta")
        
        pyplt.xticks
        pyplt.show()
    normed_hist()
    '''


def plot_tbfeo_relxill():
    import re
    import statistics as stat
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pyplt
    #key = '/home/thaddaeus/FMU/Steiner/PGX/myds.txt'
    x = []
    z = []
    nHs = []
    gammas = []
    Tins = []
    As = []
    incls = []
    pgs = []
    with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+line+'.log') == True:
                    x.append(line)

    for elem in x:
        filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+elem+'.log'
        with open(filename, 'r') as f:
            for line in f:
                z.append(line)
            for element in z:
                if 'PG-Statistic' in element:
                    pgelem = re.sub(' +', ',', element)
                    pgelemlist = pgelem.split(',')
                    pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                    pgs.append(pgstat)
                if 'nH' in element:
                    if 'TBabs' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        nH = float(elemlist[6])
                        if 0.9 < pgstat < 1.15:
                            nHs.append(nH)
                if 'simpl' in element:
                    if 'gamma' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        gamma = float(elemlist[5])
                        gammas.append(gamma)
                if 'diskbb' in element:
                    if 'Tin' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        Tin = float(elemlist[6])
                        Tins.append(Tin)
                if 'relxill' in element:
                    if 'deg' in element:
                        spinindex = z.index(element) - 1
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        incl = float(elemlist[6])
                        if incl > 50:
                            incls.append(incl)
                        spinline = re.sub(' +', ',', z[spinindex])
                        spinlist = spinline.split(',')
                        spin = float(spinlist[5])
                        if spin > 0.65:
                            As.append(spin)

            z.clear()
    
    print(len(nHs))
    print(len())

    '''
    nHs = np.array(nHs)
    gammas = np.array(gammas)
    Tins = np.array(Tins)
    As = np.array(As)
    incls = np.array(incls)
    # plot nh histogram

    def histogram_plot_routine():
      #import seaborn as sns

        fig, ax = plt.subplots(1, 1)
        ax.hist(nHs, density=True, bins=9, color='dimgrey')
        # inclination graph specifics:
        #fig.suptitle('Normalized Histogram of '+r'$\theta$'+' Values',fontsize=18)
        # ax.set_xlabel(r'$\theta$')

        # graph specfics:
        fig.suptitle('Normalized Histogram of nH Values', fontsize=18)
        ax.set_xlabel(nH)

        ax.set_title('N. Obs: '+str(len(nHs))+'; ' +
                     (r'$0.9 < \chi^2$'+'/'+r'$\nu < 1.25$'))
        xt = plt.xticks()[0]
        xmin, xmax = min(xt), max(xt)
        lnspc = np.linspace(xmin, xmax, len(nHs))
        m, s = stats.norm.fit(nHs)  # get mean and standard deviation
        # now get theoretical values in our interval
        pdf_g = stats.norm.pdf(lnspc, m, s)
        ax.plot(lnspc, pdf_g)
        ax.grid(axis='y')
        ag, bg, cg = stats.gamma.fit(nHs)
        pdf_gamma = stats.gamma.pdf(lnspc, ag, bg, cg)
        print(ag, bg, cg)
        pyplt.plot(lnspc, pdf_gamma)
        ax.legend([('Gaussian; '+r'$\mu$'+'='+str(m.round(2)) +
                    ', '+r'$\sigma$'+'='+str(s.round(2))), 'Erlang'])
        #ax.text(4.5,0.9,'N. Obs: '+str(len(nHs)))
        #ax.text(4.31,0.835,(r'$0.9 < \chi^2$'+'/'+r'$\nu < 1.25$'))
        plt.xticks
        plt.show()

    def a_plot_routine():
        #import seaborn as sns

        fig, ax = plt.subplots(1, 1)
        ax.hist(As, density=True, bins=9, color='dimgrey')
        fig.suptitle('Normalized Histogram of ' +
                     r'$\alpha$'+' Values', fontsize=18)
        ax.set_title('N. Obs: '+str(len(As))+'; ' +
                     (r'$0.9 < \chi^2$'+'/'+r'$\nu < 1.25$'))
        ax.set_xlabel(r'$\alpha$')

        xt = plt.xticks()[0]
        '''
        xmin, xmax = min(xt), max(xt)  
        lnspc = np.linspace(xmin, xmax, len(As))
        
        ab,bb,cb,db = stats.beta.fit(As)  
        pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
        pyplt.plot(lnspc, pdf_beta, label="Beta")

        ax.legend(['Beta'])
        '''
        plt.xticks
        plt.show()

    def fancy():
        import seaborn as sns
        sns.set_style('darkgrid')
        sns.distplot(nHs, bins=10)
        plt.title('hello')
        plt.legend(["KDE", "KdE"])
        plt.show()
    # fancy()
    '''

def relxill_evolution_plot_routine():
    import astropy
    from astropy.io import fits
    import os
    import matplotlib.pyplot as plt

    # Definitions
    MJDs = []
    pgs = []
    gammas = []
    Tins = []
    fracscats = []
    fracdisks = []

    # Get MJDs from fits files
    with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as key:
        for line in key:
            line = line.replace('\n', '')
            if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+line+'.log'):
                # print(test)
                with open('/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+line+'.log') as f:
                    for elem in f:
                        z = []
                        if 'PG-Statistic' in elem:
                            pgelem = re.sub(' +', ',', elem)
                            pgelemlist = pgelem.split(',')
                            pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                            if 0.9 < pgstat < 1.3:
                                orig = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+line + \
                                    '/jspipe/js_ni'+line+'_0mpu7_silver_GTI0.jsgrp'
                                target = '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                                    line+'/jspipe/js_ni'+line+'_0mpu7_silver_GTI0.fits'
                                shutil.copyfile(orig, target)
                                hdul = fits.open(target)
                                MJD = float(hdul[1].header['MJDSTART'])
                                MJDs.append(round(MJD, 5))
                                os.remove(target)
                                pgs.append(pgstat)
                                z.append(line)
                        for item in z:
                            with open('/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+line+'.log') as f:
                                for elem in f:
                                    if 'Gamma' in elem:
                                        if 'simpl' in elem:
                                            elemlist = (
                                                re.sub(' +', ',', elem)).split(',')
                                            gamma = round(
                                                float(elemlist[5]), 2)
                                            gammas.append(gamma)

                                    if 'Tin' in elem:
                                        elemlist = (
                                            re.sub(' +', ',', elem)).split(',')
                                        Tin = round(float(elemlist[6]), 2)
                                        Tins.append(Tin)

                                    if 'FracSctr' in elem:
                                        elemlist = (
                                            re.sub(' +', ',', elem)).split(',')
                                        fracscat = round(
                                            (100*float(elemlist[5])), 2)
                                        fracscats.append(fracscat)
                                        fracdisk = 100 - fracscat
                                        fracdisks.append(fracdisk)

    pgs = np.array(pgs)
    MJDs = np.array(MJDs)
    gammas = np.array(gammas)
    Tins = np.array(gammas)
    fracdisks = np.array(fracdisks)
    fracscats = np.array(fracscats)

    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].scatter(MJDs, pgs, color='black', marker='o')
    axs[0].set_ylabel('PG-Stat')
    axs[1].scatter(MJDs, gammas, color='red', marker='o')
    axs[1].set_ylabel('Gamma')
    axs[2].scatter(MJDs, Tins, color='blue', marker='o')
    axs[2].set_ylabel('Tin')

    plt.show()


def compare_tbfeo_tbabs():
    import re
    import statistics as stat
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pyplt
    # tbabs lists = _1, tbfeo lists = _2
    x1 = []
    x2 = []
    z1 = []
    z2 = []
    nHs1 = []
    nHs2 = []
    gammas1 = []
    gammas2 = []
    Tins1 = []
    Tins2 = []
    As1 = []
    As2 = []
    incls1 = []
    incls2 = []
    pgs1 = []
    pgs2 = []
    fracscats1 = []
    fracscats2 = []
    fracdisks1 = []
    fracdisks2 = []
    Os1 = []
    Fes1 = []

    # tbabs
    with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+line+'.log') == True:
                    x1.append(line)

    for elem in x1:
        filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill/'+elem+'.log'
        with open(filename, 'r') as f:
            for line in f:
                z1.append(line)
            for element in z1:
                if 'PG-Statistic' in element:
                    pgelem = re.sub(' +', ',', element)
                    pgelemlist = pgelem.split(',')
                    pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                    pgs1.append(pgstat)
                if 'nH' in element:
                    if 'TBabs' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        nH = float(elemlist[6])
                        if 0.9 < pgstat < 1.15:
                            nHs1.append(nH)
                if 'simpl' in element:
                    if 'gamma' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        gamma = float(elemlist[5])
                        gammas1.append(gamma)
                if 'diskbb' in element:
                    if 'Tin' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        Tin = float(elemlist[6])
                        Tins1.append(Tin)
                if 'relxill' in element:
                    if 'deg' in element:
                        spinindex = z1.index(element) - 1
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        incl = float(elemlist[6])
                        if incl > 50:
                            incls1.append(incl)
                        spinline = re.sub(' +', ',', z1[spinindex])
                        spinlist = spinline.split(',')
                        spin = float(spinlist[5])
                        if spin > 0.65:
                            As1.append(spin)

            z1.clear()

    nHs1 = np.array(nHs1)
    gammas1 = np.array(gammas1)
    Tins1 = np.array(Tins1)
    As1 = np.array(As1)
    incls1 = np.array(incls1)

    # tbfeo
    with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as f:
        for line in f:
            if '#' not in line:
                line = line.replace('\n', '')
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log') == True:
                    x2.append(line)

    for elem in x2:
        filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/' + \
            elem+'.log'
        with open(filename, 'r') as f:
            for line in f:
                z2.append(line)
            for element in z2:
                if 'PG-Statistic' in element:
                    pgelem = re.sub(' +', ',', element)
                    pgelemlist = pgelem.split(',')
                    pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                    pgs2.append(pgstat)
                if 'nH' in element:
                    if 'TBabs' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        nH = float(elemlist[6])
                        if 0.9 < pgstat < 1.15:
                            nHs2.append(nH)
                if 'simpl' in element:
                    if 'gamma' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        gamma = float(elemlist[5])
                        gammas2.append(gamma)
                if 'diskbb' in element:
                    if 'Tin' in element:
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        Tin = float(elemlist[6])
                        Tins2.append(Tin)
                if 'relxill' in element:
                    if 'deg' in element:
                        spinindex = z2.index(element) - 1
                        element = re.sub(' +', ',', element)
                        elemlist = element.split(',')
                        incl = float(elemlist[6])
                        if incl > 50:
                            incls2.append(incl)
                        spinline = re.sub(' +', ',', z2[spinindex])
                        spinlist = spinline.split(',')
                        spin = float(spinlist[5])
                        if spin > 0.65:
                            As2.append(spin)

            z2.clear()

    nHs2 = np.array(nHs2)
    gammas2 = np.array(gammas2)
    Tins2 = np.array(Tins2)
    As2 = np.array(As2)
    incls2 = np.array(incls2)

    # plot histograms

    import statistics
    for elem in pgs1:
        if elem > 2:
            pgs1.remove(elem)
    for elem in pgs2:
        if elem > 2:
            pgs2.remove(elem)

    print(statistics.mean(pgs1), statistics.mean(pgs2))


def relxill_final():
    import matplotlib.pyplot as plt
    from astropy.io import fits
    import seaborn as sns
    from scipy.stats import norm
    import statistics as stats
    sns.set_style('darkgrid')
    #list definitions:
    #x = []
    x = ['1130360222', '1130360206', '1130360229', '1130360185', '1130360232', '1130360187', '1130360202', '1130360201', '1130360227']
    z = [] 
    
    MJDs = []
    fluxes = []
    pgs = []
    nHs = []
    Os = []
    Fes = []
    Tins = []
    gammas = []
    scatfracs = []
    diskfracs = []
    incls = []
    As = []
    logxis = []
    gammauppers = []
    gammalowers = []
    scatuppers  = []
    scatlowers = []
    cfluxuppers = []
    cfluxlowers = []

    def limited_obs_routine():
        
        '''
        with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt','r') as f:
            for line in f:
                if '#' not in line:
                    line = line.replace('\n','')
                    if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log') == True:
                        x.append(line)
        '''
        for elem in x:
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+elem+'.log'
            with open(filename,'r') as f:
                for line in f:
                    z.append(line)    
                for element in z:
                    if 'PG-Statistic' in element:
                        pgelem = re.sub(' +',',',element)
                        pgelemlist = pgelem.split(',')
                        pgstat = float(pgelemlist[4])/float(pgelemlist[6])
                        pgs.append(pgstat)
                    if 'nH' in element:
                        if 'TBfeo' in element:
                            element = re.sub(' +',',',element)
                            elemlist = element.split(',')
                            nH = float(elemlist[6])
                            nHs.append(nH)
                    if 'TBfeo' in element: 
                        elementlist = (re.sub(' +',',',element).split(','))
                        if elementlist[4] == 'O':
                            Os.append(float(elementlist[5]))
                        elif elementlist[4] == 'Fe':
                            Fes.append(float(elementlist[5]))
                    if 'simpl' in element:
                        if 'Gamma' in element:
                            element = re.sub(' +',',',element)
                            elemlist = element.split(',')
                            gamma = float(elemlist[5])
                            gammas.append(gamma)
                        if 'FracSctr' in element: 
                            elementlist = (re.sub(' +',',',element).split(','))
                            scatfrac = 100*float(elementlist[5])
                            scatfracs.append(scatfrac)
                            diskfrac = 100 - scatfrac
                            diskfracs.append(diskfrac)
                        if 'logxi' in element:
                            elementlist = (re.sub(' +',',',element).split(','))
                            logxis.append(float(elementlist[5]))
                    if 'diskbb' in element:
                        if 'Tin' in element:
                            element = re.sub(' +',',',element)
                            elemlist = element.split(',')
                            Tin = float(elemlist[6])
                            Tins.append(Tin)
                    if 'relxill' in element:
                        if 'deg' in element:
                            spinindex = z.index(element) - 1
                            element = re.sub(' +',',',element)
                            elemlist = element.split(',')
                            incl = float(elemlist[6])
                            incls.append(incl)
                            spinline = re.sub(' +',',',z[spinindex])
                            spinlist = spinline.split(',')
                            spin = float(spinlist[5])
                            As.append(spin)
                z.clear()
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/cflux'+elem+'.log'
            with open(filename,'r') as f:
                for line in f:
                    if 'lg10Flux' in line:
                        linelist = (re.sub(' +',',',line).split(','))
                        fluxes.append(float(linelist[6]))
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/cflux'+elem+'.log'
            with open(filename,'r') as f:
                w = []
                cfluxbaps = []
                for line in f:
                    w.append(line.replace('\n',''))
                for chalk in w:
                    if 'err 3' in chalk:
                        indy = w.index(chalk)
                        errline = w[indy+1]
                        errlist = (re.sub(' +',';',errline)).split(';')
                        if errlist[1] == '3':
                            cfluxcoupled = errlist[4]
                            cfluxcoupled = cfluxcoupled.replace('(','')
                            cfluxcoupled= cfluxcoupled.replace(')','')
                            cfluxcoupled = cfluxcoupled.split(',')
                            cfluxlower = float((cfluxcoupled[0]).replace('-',''))
                            cfluxlowers.append(cfluxlower)
                            cfluxupper = float(cfluxcoupled[1])
                            cfluxuppers.append(cfluxupper)
                        else:
                            errline = w[indy+2]
                            errlist = (re.sub(' +',';',errline)).split(';')
                            if errlist[1] == '3':
                                cfluxcoupled = errlist[4]
                                cfluxcoupled = cfluxcoupled.replace('(','')
                                cfluxcoupled= cfluxcoupled.replace(')','')
                                cfluxcoupled = cfluxcoupled.split(',')
                                cfluxlower = float((cfluxcoupled[0]).replace('-',''))
                                cfluxlowers.append(cfluxlower)
                                cfluxupper = float(cfluxcoupled[1])
                                cfluxuppers.append(cfluxupper)
                            else: 
                                errline = w[indy+3]
                                errlist = (re.sub(' +',';',errline)).split(';')
                                if errlist[1] == '3':
                                    cfluxcoupled = errlist[4]
                                    cfluxcoupled = cfluxcoupled.replace('(','')
                                    cfluxcoupled= cfluxcoupled.replace(')','')
                                    cfluxcoupled = cfluxcoupled.split(',')
                                    cfluxlower = float((cfluxcoupled[0]).replace('-',''))
                                    cfluxlowers.append(cfluxlower)
                                    cfluxupper = float(cfluxcoupled[1])
                                    cfluxuppers.append(cfluxupper)

            if os.path.exists('/home/thaddaeus/FMU/Steiner/thaddaeus/'+elem+'/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.jsgrp'):
                orig = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+elem+'/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.jsgrp'
                target = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+elem+'/jspipe/js_ni'+elem+'_0mpu7_silver_GTI0.fits'
                shutil.copyfile(orig,target)
                hdul = fits.open(target)
                MJD = hdul[1].header['MJDSTART']
                MJDs.append(float(MJD))
                os.remove(target)
            
            #Get confidence intervals
            filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/err'+elem+'.log'
            with open(filename,'r') as f:
                gammabaps = []
                scatters = []
                for line in f:
                    linelist = (re.sub(' +',';',line)).split(';')
                    if linelist[1] == '5':
                        gammabaps.append(linelist[4])
                    elif linelist[1] == '6':
                        scatters.append(linelist[4])
                
                gammacoupled = gammabaps[0]
                gammacoupled = gammacoupled.replace('(','')
                gammacoupled = gammacoupled.replace(')','')
                gammacoupled = gammacoupled.split(',')
                gammalower = float((gammacoupled[0]).replace('-',''))
                gammalowers.append(gammalower)
                gammaupper = float(gammacoupled[1])
                gammauppers.append(gammaupper)

                scattercoupled = scatters[0]
                scattercoupled = scattercoupled.replace('(','')
                scattercoupled = scattercoupled.replace(')','')
                scattercoupled = scattercoupled.split(',')
                scatterlow = 100*float((scattercoupled[0]).replace('-',''))
                scatlowers.append(scatterlow)
                scatterup = 100*float(scattercoupled[1])
                scatuppers.append(scatterup)
    limited_obs_routine()
    
    '''
    #Clean some --- Add MJDs
    
    for elem in pgs:
        if  elem > 1.03 or elem < 0.97:
            elemindex = pgs.index(elem)
            pgs.remove(elem)
            listoflists = [MJDs,fluxes,nHs,Os,Fes,Tins,gammas,scatfracs,diskfracs,incls,As]
            for item in listoflists:
                item.remove(item[elemindex])
    for elem in Fes:
        if elem > 5:
            elemindex = Fes.index(elem)
            listoflists = [fluxes,MJDs,fluxes,pgs,nHs,Os,Fes,Tins,gammas,scatfracs,diskfracs,incls,As]
            for item in listoflists:
                item.remove(item[elemindex])
    '''
    #numpy-fy everything --- Add MJDs
    listoflists = [gammauppers,gammalowers,scatuppers,scatlowers,MJDs,fluxes,pgs,nHs,Os,Fes,gammas,Tins,scatfracs,diskfracs,incls,As]

    cfluxlowers = np.array(cfluxlowers)
    cfluxuppers = np.array(cfluxuppers)
    gammauppers = np.array(gammauppers)
    gammalowers = np.array(gammalowers)
    scatuppers = np.array(scatuppers)
    scatlowers = np.array(scatlowers)
    MJDs = np.array(MJDs)
    fluxes = np.array(fluxes)
    pgs = np.array(pgs)
    nHs = np.array(nHs)
    Os= np.array(Os)
    Fes = np.array(Fes)
    gammas = np.array(gammas)
    Tins = np.array(Tins)
    scatfracs = np.array(scatfracs)
    diskfracs = np.array(diskfracs)
    incls = np.array(incls)
    As = np.array(As)
    
    #Plot them baby
    def plot_pgs():
        fig, axes = plt.subplots()
        sns.distplot(pgs,bins=15,kde=False)
        fig.suptitle('Fit Statistic Distribution')
        axes.set_xlabel(r'$\chi^2$'+'/'+r'$\nu$')
        axes.set_ylabel('Number of Observations')
        plt.show()
        #plt.savefig('pgstat_histogram.png')
    def plot_tbfeo():
        f, axes = plt.subplots(1, 3, figsize=(7,7),sharey=True)
        plt.suptitle('Distributions of TBfeo Parameters',fontsize=17)
        f.text(0.04,0.5,'Number of Observations',va='center',rotation='vertical')
        chitext = '0.92 < ' + r'$\chi^2$' +'/' + r'$\nu$' +' < 1.1; N.Obs: ' + str(len(pgs))
        #f.text(0.91,0.5,chitext,va='center',rotation='vertical')
        plt.yticks(np.arange(0,10,3))

        sns.distplot(nHs,bins=3,kde=False,ax=axes[0])
        mu = round(stats.mean(nHs),2)
        sig = round(stats.stdev(nHs),2)
        axes[0].set_title('nH ('+r'$10^{22}$'+' '+r'$atoms$'+' '+r'$cm^{-2}$'+')')
        axes[0].set_xlabel(r'$\mu$'+'='+ str(mu) + ', '+ r'$\sigma$' + '=' + str(sig))
        axes[0].set_xticks(np.arange(2.5,5,0.5))
        
        sns.distplot(Os,bins=3,kde=False,ax=axes[1])
        axes[1].set_title('O (relative to solar)')
        mu = round(stats.mean(Os),2)
        sig = round(stats.stdev(Os),2)
        axes[1].set_xlabel(r'$\mu$'+'='+ str(mu) + ', '+ r'$\sigma$' + '=' + str(sig))
        axes[1].set_xticks(np.arange(0,3.1,0.75))

        sns.distplot(Fes,bins=3,kde=False,ax=axes[2])
        axes[2].set_title('Fe (relative to solar)')
        mu = round(stats.mean(Fes),2)
        sig = round(stats.stdev(Fes),2)
        axes[2].set_xlabel(r'$\mu$'+'='+ str(mu) + ', '+ r'$\sigma$' + '=' + str(sig))
        axes[2].set_xticks(np.arange(0.75,4,0.75))
        #plt.subplots_adjust(wspace=0.35)
        #plt.legend()
        plt.show()
        
        #plt.savefig('TBfeo_histograms.png')
    def plot_relxill_comps():
        fig, axes = plt.subplots(1,2)
        fig.text(0.04,0.5,'Number of Observations',va='center',rotation='vertical')
        chitext = '0.97 < ' + r'$\chi^2$' +'/' + r'$\nu$' +' < 1.03; N.Obs: ' + str(len(pgs))
        fig.text(0.5,0.02,chitext,ha='center')
        plt.suptitle('Restricted Distributions of Inclination and Spin',fontsize=16)
        sns.distplot(incls,bins=3,kde=False,ax=axes[0])
        axes[0].set_title(r'$\theta$')

        sns.distplot(As,bins=3,kde=False,ax=axes[1])
        axes[1].set_title(r'$a_*$')
        axes[1].set_yticks(np.arange(0,10,3))

        plt.show()

    def plot_evolution():
        import pandas as pd 

           
        fig, axes = plt.subplots(3,1,sharex=True)

        axes[0].errorbar(MJDs,fluxes,marker='o',yerr=[cfluxlowers,cfluxuppers],ls='none')
        axes[1].errorbar(MJDs,diskfracs,marker='o',yerr=[scatlowers,scatuppers],ls='none')
        axes[1].set_ylim(87,100)
        axes[2].errorbar(MJDs,gammas,marker='o',yerr=[gammalowers,gammauppers],ls='none')
        fig.suptitle('Evolution of Associated Parameters')
        
        axes[0].set_ylabel('log(flux)')
        chitext = '0.92 < ' + r'$\chi^2$' + '/' r'$\nu$' + ' < 1.1; ' + 'N. Obs = ' + str(len(pgs))
        axes[0].set_title(chitext,fontsize=10)
        axes[1].set_ylabel('Disk Fraction')
        axes[2].set_ylabel('Gamma')
        axes[2].set_xlabel('MJD')
        #axes[2].set_yticks(np.arange(1.5,3.5,0.5))
        
        #plt.subplots_adjust(hspace=0.1)
        
        plt.show()

    plot_evolution()
    
        
def barf():
    def times():
        with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt','r') as f:
                for line in f:
                    if '#' not in line:
                        line = line.replace('\n','')
                        filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log'
                        if os.path.isfile(filename) == True:
                            print(os.path.getmtime(filename))
    def pgs():
        x = []
        z = []
        pgs = []
        goodfiles = []
        def limited_obs_routine():
            with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt','r') as f:
                for line in f:
                    if '#' not in line:
                        line = line.replace('\n','')
                        if os.path.isfile('/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+line+'.log') == True:
                            x.append(line)

            for elem in x:
                filename = '/home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/'+elem+'.log'
                with open(filename,'r') as f:
                    for line in f:
                        z.append(line)    
                    for element in z:
                        if 'PG-Statistic' in element:
                            pgelem = re.sub(' +',',',element)
                            pgelemlist = pgelem.split(',')
                            pgindex = z.index(element)
                            dofline = z[pgindex+3]
                            doflist = (re.sub(' +',',',dofline).split(','))
                            pgstat = float(pgelemlist[4])/float(doflist[7])
                            if pgstat > 1.2:
                                continue
                            elif pgstat < 1.2 and pgstat > 0.95:
                                    goodfiles.append(elem)
                                    pgs.append(pgstat)
                    z.clear()
        limited_obs_routine()
        goodfiles = set(goodfiles)
        goodfiles = list(goodfiles)
        print(len(goodfiles))
        print(len(pgs))
        print(max(pgs))
        def tbfeo_fitcommands():
            f.write('xspec'+'\n')
            f.write('xsect vern'+'\n')
            f.write('abun wilm'+'\n')
            f.write('data ' + jsgrp)
            f.write('none'+'\n')
            f.write('none' + '\n')
            f.write(bg)
            f.write(rmf)
            f.write(arf)
            f.write('ignore **-2.2 10.0-**'+'\n')
            f.write('ignore bad'+'\n')
            f.write('query yes'+'\n')
            f.write('statistic pgstat'+'\n')
            f.write('setp back on'+'\n')
            f.write('model tbabs(simpl(diskbb))'+'\n')
            f.write('/*'+'\n')
            f.write('newpar 1'+'\n')
            f.write('3.0 0.01 1.5 1.501 4.5 5.0'+'\n')
            f.write('newpar 2'+'\n')
            f.write('2 0.02 1.3 1.4 3.2 4.5'+'\n')
            f.write('newpar 3'+'\n')
            f.write('0.3 0.01 0.001 0.005 0.99 0.999'+'\n')
            f.write('newpar 5'+'\n')
            f.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
            f.write('chatter 5'+'\n')
            f.write('freeze 1'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('thaw 1'+'\n')
            f.write('notice 1.0-10.0'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('lmod relxill .'+'\n')
            f.write('editmod tbabs(simpl(diskbb+relxill))'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('86,3 5,,')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('=2'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('-1'+'\n')
            f.write('\n')
            f.write('freeze 19'+'\n')
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n')
            f.write('\n')
            f.write('editmod tbfeo(simpl(diskbb+relxill))'+'\n')
            f.write('3.0 0.01 1.5 1.501 4.5 4.8'+'\n')
            f.write('0.6,0.001 0.05 2 3'+'\n')
            f.write('1,0.1 0.3 3 4'+'\n')
            f.write('\n')
            f.write('parallel leven 2'+'\n')
            f.write('fit'+'\n')

        def tbfeo_plot_log_and_quit():
            f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/'+item+'.log'+'\n')
            f.write('chatter 10'+'\n')
            f.write('show data'+'\n')
            f.write('show fit'+'\n')
            f.write('show param'+'\n')
            f.write('log none'+'\n')
            f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/err'+item+'.log'+'\n')
            f.write('freeze 1-3 13 14 19 20 23'+'\n')
            f.write('chatter 5 5'+'\n')
            f.write('fit'+'\n')
            f.write('err 5 6 8'+'\n')
            f.write('log none'+'\n')
            f.write('log /home/thaddaeus/FMU/Steiner/vietnam/relxill(tbfeo)/error_work/cflux'+item+'.log'+'\n')
            f.write('chatter 10 10'+'\n')
            f.write('show data'+'\n')
            f.write('show fit'+'\n')
            f.write('show param'+'\n')
            f.write('chatter 5 5'+'\n')
            f.write('editmod cflux*tbfeo(simpl(diskbb+relxill))'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('freeze 4-26'+'\n')
            f.write('thaw 8'+'\n')
            f.write('fit'+'\n')
            f.write('err 3'+'\n')
            f.write('log none'+'\n')
            f.write('quit'+'\n')
            f.write('y'+'\n')

        for item in goodfiles:
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+item + \
                '/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.jsgrp' + '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/' + \
                item+'/jspipe/js_ni'+item+'_0mpu7_silver_GTI0.bg' + '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf' + '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf' + '\n'
            with open('/home/thaddaeus/FMU/Steiner/vietnam/relxill.txt', 'a') as f:
                tbfeo_fitcommands()
                tbfeo_plot_log_and_quit()





    pgs()

relxill_final()