import pandas as pd 

main_df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv')
main_df = main_df.drop(columns=['C', 'D', 'E', 'F'])

update_df = pd.read_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/src/production/last_xspec/MAXI_spectral_results.csv')

main_df = main_df.merge(update_df, on='observation_ID')
print(main_df)
#main_df.to_csv('/mnt/c/Users/Research/Documents/GitHub/MAXI-J1535/final-push/data/pipeline/MAXI/[scalar-input][regression].csv', index=False)