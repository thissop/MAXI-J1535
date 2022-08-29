def combine_github_tables(dir:str='/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/sources/H1743-322/qpo/github-tables'): 
    '''
    
    notes
    -----
    this function is not relevant anymore; it was more of a one-off execution
    
    '''

    import os
    import pandas as pd

    os.chdir(dir)

    df1, df2, df3, df4 = (pd.read_csv(i) for i in ['H1732_group_1.txt', 'H1732_group_2.txt', 'H1732_group_3.txt', 'H1732_group_4.txt'])

    combined = pd.concat((df1, df2, df3, df4))

    print(combined)
    print(df1)

combine_github_tables()