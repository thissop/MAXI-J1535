import os

key = 'IDs.txt'
out = 'grppha commands.txt'
x = []
#For MaxiJ1535-4:
with open(key,'r') as k, open(out,'a') as o:
    for line in k:
        if '#' not in line:
            name = str(line)
            if name not in x:
                x.append(name)
                name = name.strip('\n')
                jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.jsgrp'+ '\n'
                pha = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.pha'+ '\n'
                if os.path.isfile('/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.jsgrp'): 
                    o.write('heainit'+'\n')
                    o.write('grppha'+'\n')
                    o.write(jsgrp)
                    o.write(pha)
                    o.write('group min 30'+'\n')
                    o.write('exit'+'\n')
print(len(x))
#For MAXIJ1535- 2: 
'''
with open(key,'r') as k, open(out,'a') as o:
    for line in k:
        if '#' not in line:
            name = str(line)
            if name not in x:
                x.append(name)
                name = name.strip('\n')
                jsgrp = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.jsgrp'+ '\n'
                pha = '/home/thaddaeus/FMU/Steiner/thaddaeus/'+name+'/jspipe/js_ni'+name+'_0mpu7_silver_GTI0.pha'+ '\n'
                o.write('heainit'+'\n')
                o.write('grppha'+'\n')
                o.write(jsgrp)
                o.write(pha)
                #o.write('group 1 1501 3'+'\n')
                o.write('group min 30'+'\n')
                o.write('exit'+'\n')
                '''
