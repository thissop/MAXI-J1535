def fix_prelim_classes(): 
    import pandas as pd
    
    full_ids = []
    classes = []

    review_num = 0
    with open('prelim_vetting_classes.csv', 'r') as f: 
        for _, line in enumerate(f): 
            if _ > 0:  
                linelist = line.split(',')
                full_ids.append(linelist[0])
                class_str = ' '.join(linelist[1:]).replace('\n','')
                classes.append(class_str)
                if '?' in class_str: 
                    review_num+=1
    
    df = pd.DataFrame(list(zip(full_ids, classes)), columns=['full_id', 'comment'])
    print(review_num)
    df.to_csv('prelim_vetting_classes.csv', index=False)

#fix_prelim_classes()

def num_qpos_initial(): 
    import pandas as pd
    import numpy as np

    import matplotlib.pyplot as plt

    num_qpos = np.array(pd.read_csv(r'code\xspec_related\better-organization\analysis-routines\qpo_data_aggregation\results\pre-steiner-compiled.csv')['num_qpos'])

    num_qpos = np.array([int(i) for i in num_qpos if i!='flagged'])

    qpo_obs_count = len(np.where(num_qpos>0)[0])
    total_qpos = np.sum(num_qpos)

    plt.hist(num_qpos)
    plt.xlabel('num qpos per obs')
    plt.ylabel('count')
    plt.title('obs with qpos: '+str(qpo_obs_count)+'\nTotal QPOs: '+str(total_qpos))
    plt.savefig('very initial dist.png')

#num_qpos_initial()