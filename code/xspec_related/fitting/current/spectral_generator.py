def generate_commands(): 
    import numpy as np

    commands_list = np.array([])

    def to_list(value): 
        commands_list = np.append(commands_list, value)

    def nthcomp_fit_commands(log_temp, seg_id, f, jsgrp, bg, rmf, arf, values_dict):
        log_file = log_temp.replace('++++++++++',seg_id)
        to_list('xspec'+'\n')
        to_list('data ' + jsgrp+'\n')
        to_list('none'+'\n')
        to_list('none' + '\n')
        to_list('backgrnd '+bg+'\n')
        to_list('response '+rmf+'\n')
        to_list('arf '+arf+'\n')
        
        to_list('ignore **-0.5 1.5-2.3 10.0-**'+'\n') #Often modified
        
        to_list('ignore bad'+'\n')

        #to_list('query yes'+'\n') ''' Often modified '''

        to_list('statistic pgstat'+'\n')
        to_list('setp back on'+'\n')
        to_list('model tbabs(diskbb+nthcomp)'+'\n')
        
        to_list(nH+'\n')

        to_list('0.6 0.02 '+tin_lower+' '+tin_lower+' '+tin_upper+' '+tin_upper+'\n')
        to_list('\n')
        
        to_list('2 0.02 '+gamma_lower+' '+gamma_lower+' '+gamma_upper+' '+gamma_upper+'\n')  

        to_list(kTe+'\n')
        to_list('=p2'+'\n')
    
        to_list(inp_type+'\n')
        
        to_list(redshift+'\n')
        
        to_list('\n')
        to_list('freeze 1'+'\n')
        to_list('freeze 5'+'\n')
        to_list('freeze 7'+'\n')
        to_list('freeze 8'+'\n')
        to_list('chatter 5 10'+'\n')
        to_list('parallel leven 2'+'\n')
        to_list('fit '+str(iterations)+'\n') #query yes = False
        to_list('n'+'\n') #query yes = False
        to_list('chatter 5 10'+'\n')
        to_list('log '+log_file+'\n')
        to_list('show data'+'\n')
        to_list('show model'+'\n')
        to_list('show param'+'\n')
        to_list('show fit'+'\n')
        to_list('log none'+'\n')
    

values_dict = {
               'gam_soft_lower':1.2, 'gam_soft_upper':4.0,
               'gam_hard_lower':1.1, 'gam_hard_upper':4.0
               }