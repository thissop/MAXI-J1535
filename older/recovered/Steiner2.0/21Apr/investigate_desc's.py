def investigate_classes(key_file,old_dir,copy_dir):
    # Import(s)
    import pandas as pd
    import os
    import shutil
    
    # Action
    df = pd.read_csv(key_file)
    ids = list(df['filename'])
    classes = list(df['class'])
    
    for id, classif in zip(ids,classes):
        classif = str(classif)
        if classif =='1':
            shutil.copyfile(os.path.join(old_dir,id),os.path.join(copy_dir.replace('+++','one'),id))
        elif classif == '2':
            shutil.copyfile(os.path.join(old_dir,id),os.path.join(copy_dir.replace('+++','two'),id))
        elif classif == '3':
            shutil.copyfile(os.path.join(old_dir,id),os.path.join(copy_dir.replace('+++','three'),id))
        else:
            print(id,classif)
            
        
key = '/home/thaddaeus/FMU/Steiner2.0/21Apr/visual_results.csv'
investigate_classes(key_file=key,old_dir='/home/thaddaeus/FMU/Steiner2.0/21Apr/all_pds_plots',copy_dir='/home/thaddaeus/FMU/Steiner2.0/21Apr/classified_plots/class_+++')