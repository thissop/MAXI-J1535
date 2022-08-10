def returnConfidenceIntervals(IDs,pathtemp,pnumbers,listnames):
    #Imports
    import string
    import re
    #Action
    for item in IDs:
        obsid = item
        path = pathtemp.replace('++++++++++',obsid)
        for elem in pnumbers:
            temporarylist = []
            alphabet_list = list(string.ascii_lowercase)
            with open(path,'r') as f:
                for line in f:
                    if any(element in line for element in alphabet_list):
                            continue
                    else:
                        if len(line) > 3:
                            line = line.replace('#','')
                            line = line.replace('\n','')
                            linelist = (re.sub(' +',',',line)).split(',')
                            linelist = linelist[1:]
                            if linelist[0] == str(elem):
                                lower = linelist[3]
                                upper = linelist[4]
                                lower = lower.replace('(','')
                                upper = upper.replace(')','')
                                
                                if linelist[2] == '0':
                                    if linelist[1] != '0':
                                        upper = 'PHUZ'
                                        lowerandupper = str(abs(float(lower)))+':'+upper
                                        obsidandci = str(obsid)+':'+lowerandupper
                                        temporarylist.append(obsidandci)
                                    else:
                                        lowerandupper='PHLZ:PHUZ'
                                        obsidandci = str(obsid)+':'+lowerandupper
                                        temporarylist.append(obsidandci)
                                elif linelist[1] == '0':
                                    if linelist[2] != 0:
                                        lower = 'PHLZ'
                                        lowerandupper = lower+':'+str(abs(float(upper)))
                                        obsidandci = str(obsid)+':'+lowerandupper
                                        temporarylist.append(obsidandci)
                                else:
                                    lowerandupper = str(abs(float(lower)))+':'+str(abs(float(upper)))
                                    obsidandci = str(obsid)+':'+lowerandupper
                                    temporarylist.append(obsidandci)
                                
            if len(temporarylist) == 0:
                failederrorstring = str(obsid)+':NaN:NaN'
                listnames[(pnumbers.index(elem))].append(failederrorstring)
                break

            else:
                for element in temporarylist: 
                    if 'PHLZ' not in element:
                        if 'PHUZ' not in element: 
                            listnames[(pnumbers.index(elem))].append(element) 
                            break
                    if 'PHLZ' or 'PHUZ' in element:
                        listnames[(pnumbers.index(elem))].append(element) 
                        break
                                
                                    
gammas = []
scatfracs = []
Tins = []
pathTemp = '/home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/logs/error++++++++++.log'

idlist = []
import os 
with open('/home/thaddaeus/FMU/Steiner/PGX/myds.txt', 'r') as f:
    for line in f:
        if '#' not in line:
            line = line.replace('\n','')
            if os.path.exists('/home/thaddaeus/FMU/Steiner2.0/20October/Fits_v1/logs/error'+line+'.log') == True:
                idlist.append(line)

returnConfidenceIntervals(IDs=idlist,pathtemp=pathTemp,pnumbers=[5,6,8],listnames=[gammas,scatfracs,Tins])
print(gammas)
print(scatfracs)
print(Tins)