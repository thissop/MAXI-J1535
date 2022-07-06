import pandas as pd

nthcomp_df = pd.read_csv('./data/processed/2022/wrangled_nthcomp_spectral_data.csv')
nthcomp_df = nthcomp_df.rename(columns={'fit_stat':'nthcomp_fit_stat', 
                                        'reduced_fit_stat':'nthcomp_reduced_fit_stat'})

cols_to_drop = ['tin_before_error', 'diskbb_norm_before_error', 'gamma_before_error',
               'nthcomp_norm_before_error', 'nthcomp_fit_stat', 'nthcomp_reduced_fit_stat',
               'tin_after_error', 'diskbb_norm_after_error', 'gamma_after_error',
               'nthcomp_norm_after_error']

non_nthcomp_info_df = nthcomp_df.drop(columns=cols_to_drop)


#print(non_nthcomp_info_df)
# combined_info_df = 