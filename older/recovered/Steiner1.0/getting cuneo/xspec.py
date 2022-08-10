key = 'obslist.txt'
out = 'xspec commands.txt'
import os
import re 

x = []
with open(key,'r') as k:
    for line in k:
        x.append(line)
with open(key,'r') as k, open(out,'w') as out:
    for line in k:
        if '#' not in line:
            name = str(line)
            name = name.strip('\n')
            name = name[0:10]
            
            jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.jsgrp'+ '\n'
            #pha = 'data '+'/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.pha'+ '\n'
            bg = 'backgrnd ' + '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.bg'+ '\n'
            rmf = 'response '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.rmf'+ '\n'
            arf = 'arf '+'/home/thaddaeus/FMU/Steiner/thaddaeus/nicer_d49_55575341.arf'+ '\n'
            head = '###########' + '\n'
            ignore = 'ignore **-2.0 10.-**'+'\n'
        #abun = 'abun wilm'+'\n'
        #model = 'model tbabs*cflux(nthcomp+diskbb)'+'\n'
        #model = 'model phabs(power+diskbb)'+'\n'
            query = 'query yes'+'\n'
            energies = 'energies 0.01 100 1000 log' + '\n'
        #tbabs = '3.6'+'\n'
        ###################
            def intro():
                '''
                log /home/thaddaeus/FMU/Steiner/PGX/MAXI2/1050360104.log
                show data
                show param
                show fit
                log none
                plot chi ldata
                iplot
                hard /home/thaddaeus/FMU/Steiner/PGX/MAXI2_BF_Images/1050360104/png
                quit

                log /home/thaddaeus/FMU/Steiner/PGX/MAXI2/1050360104cflux.log
                chatter 5 5 
                freeze 1-3 5 6 8 9
                editmod cflux*tbfeo*simpl(diskbb)
                0.6
                10

                fit
                chatter 10 10
                show param
                log none
                quit
                y
                '''
                #out.write('log '+'/home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+name+'.log'+'\n')
                out.write('log '+'/home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+name+'.log'+'\n')
                out.write('show data'+'\n')
                out.write('show param'+'\n')
                out.write('show fit'+'\n')
                out.write('log none'+'\n')
                out.write('plot ldata rat mod chi'+'\n')
                out.write('iplot'+'\n')
                #out.write('hard '+'/home/thaddaeus/FMU/Steiner/PGX/MAXI2_BF_Images/'+name+'/png'+'\n')
                out.write('hard '+'/home/thaddaeus/FMU/Steiner/PGX/MAXI4_BF_Images/'+name+'/png'+'\n')
                out.write('quit'+'\n')
                #log the cflux 
                #out.write('log /home/thaddaeus/FMU/Steiner/PGX/MAXI2/'+name+'cflux.log'+'\n')
                out.write('log /home/thaddaeus/FMU/Steiner/PGX/MAXI4/'+name+'cflux.log'+'\n')
                out.write('chatter 5 5'+'\n')
                out.write('freeze ###1-3 5 6 8 9'+'\n')
                out.write('editmod cflux*tbfeo*simpl(diskbb)###'+'\n')
                out.write('0.6'+'\n')
                out.write('10'+'\n')
                out.write('\n')
                out.write('fit'+'\n')
                out.write('chatter 10 10'+'\n')
                out.write('show param'+'\n')
                out.write('log none'+'\n')
                out.write('quit'+'\n')
                out.write('y'+'\n')
                out.write('\n')
                
                out.write('heainit'+'\n')
                out.write('xspec'+'\n')
                out.write('xsect vern'+'\n')
                out.write('abun wilm'+'\n')
                out.write('data '+ jsgrp)
                out.write('none'+'\n')
                out.write('none' + '\n')
                out.write(bg)
                out.write(rmf)
                out.write(arf)
                out.write(ignore)
                out.write('ignore bad'+'\n')
                #out.write(abun)
                out.write(query)
                out.write(energies)
                out.write('statistic pgstat'+'\n')
                out.write('cpd /xs'+'\n')
                out.write('setplot energy'+'\n')
                out.write('setp back on'+'\n')

            def simpldiskbb():
                out.write('model tbfeo*simpl(diskbb)'+'\n')
                out.write('/*'+'\n')
                out.write('newpar 1'+'\n')
                out.write('3.7 0.01 3.2 3.5 4 4.1'+'\n')
                out.write('newpar 2'+'\n')
                out.write('1 0.02 0.01 0.2 5 6'+'\n')
                out.write('newpar 5'+'\n')
                out.write('2 0.02 1.3 1.4 2.75 3.2'+'\n')
                out.write('newpar 6'+'\n')
                out.write('0.3 0.01 0.001 0.001 0.99 1'+'\n')
                out.write('newpar 8'+'\n')
                out.write('0.7 0.02 0.1 0.15 2.8 3'+'\n')
                out.write('chatter 5'+'\n')
                out.write('fit'+'\n')
                out.write('\n')
                out.write('thaw 2-3'+'\n')
                out.write('newpar 3'+'\n')
                out.write('1 0.01 0.001 0.01 3 5'+'\n')
                out.write('fit'+'\n')
                out.write('chatter 10'+'\n')
                out.write('show param'+'\n')
                out.write('show fit'+'\n')
                out.write('plot ldata rat mod chi'+'\n')

                #gaussian
                out.write('\n')
                out.write('editmod tbfeo*simpl(diskbb)+gau'+'\n')
                out.write('6.4 0.01 6.3 6.35 6.45 6.5'+'\n')
                out.write('0.2 0.01 0.005 0.005 0.5 0.9'+'\n')
                out.write('/*'+'\n')
                out.write('chatter 5'+'\n')
                out.write('fit'+'\n')
                out.write('chatter 10'+'\n')
                out.write('show param'+'\n')
                out.write('show fit'+'\n')
                out.write('plot ldata rat mod chi'+'\n')
                
                #Second (Si) gaussian
                out.write('\n')
                out.write('editmod tbfeo*simpl(diskbb)+gau+gau'+'\n')
                out.write('1.8 0.01 1.65 1.7 1.9 1.95'+'\n')
                out.write('0.2 0.01 0.005 0.005 0.5 0.5'+'\n')
                out.write(',,-5 -2 ,,'+'\n')
                out.write('chatter 5'+'\n')
                out.write('fit'+'\n')
                out.write('chatter 10'+'\n')
                out.write('show param'+'\n')
                out.write('show fit'+'\n')
                out.write('plot ldata rat mod chi'+'\n')

                #Actually Write 'em
                
            out.write(head)
            intro()
            simpldiskbb()
                

            '''
            #nthcomp only
            out.write('******************************'+'\n')
            intro()
            out.write('model tbabs(nthcomp)'+'\n')
            #out.write(tbabs)
            out.write('1.5'+'\n')
            out.write('20'+'\n')
            out.write('0.4'+'\n')
            out.write('1'+'\n')
            out.write('\n')
            out.write('\n')
            out.write('fit'+'\n')
            #nthcomp + diskbb 
            intro()
            out.write('model tbabs(nthcomp+diskbb)'+'\n')
            out.write(tbabs)
            out.write('2'+'\n')
            out.write('30'+'\n')
            out.write('0.6'+'\n')
            out.write('1'+'\n')
            out.write('\n')
            out.write('\n')
            out.write('0.6'+'\n')
            out.write('\n')
            out.write('fit'+'\n')
            #nthcomp + diskbb + gaussian
            intro()
            out.write('model tbabs(nthcomp+diskbb+gau)'+'\n')
            out.write(tbabs)
            out.write('2.2'+'\n')
            out.write('50'+'\n')
            out.write('0.8'+'\n')
            out.write('1'+'\n')
            out.write('\n')
            out.write('\n')
            out.write('1.18'+'\n')
            out.write('\n')
        '''