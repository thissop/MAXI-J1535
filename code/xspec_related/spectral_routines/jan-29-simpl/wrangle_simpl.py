import os
import re
from tkinter import N
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

log_dir = './code/xspec_related/spectral_routines/jan-29-simpl/logs'

all_ids = list(pd.read_csv('./code/xspec_related/good_ids.csv')['full_id'])

results_dict = {'full_ids':[], 

                'simpl_tin':[], 
                'simpl_diskbb_norm':[],
                'simpl_gamma':[],
                'simpl_FracScat':[], 

                'fit_stat':[], 
                'reduced_fit_stat':[]}

# base sub dict: :{'search_string':r'', 'line_index':}
log_file_dict = {'simpl_tin':{'search_string':r'   5    3   diskbb     Tin', 'line_index':6}, 
                 'simpl_diskbb_norm':{'search_string':r'   6    3   diskbb     norm', 'line_index':5},
                 'simpl_gamma':{'search_string':r'   2    2   simpl      Gamma', 'line_index':5},
                 'simpl_FracScat':{'search_string':r'   3    2   simpl      FracSctr', 'line_index':5}, 
                 'fit_stat':{'search_string':r'Fit statistic  : PG-Statistic', 'line_index':4}}

for full_id in tqdm(all_ids):
    split_id = full_id.split('_')
    obs_id = split_id[0]
    gti = split_id[1]

    error_log = log_dir +'/'+full_id+ '.txt'
    if os.path.exists(error_log): 
        results_dict['full_ids'].append(full_id)
        with open(error_log, 'r') as f:
            f_lines = f.readlines()
            for line_index, line in enumerate(f_lines): 
                for search_term, search_array in zip(log_file_dict.keys(), log_file_dict.values()): 
                    if search_array['search_string'] in line: 
                        line_list = (re.sub(' +', '@@@', line)).split('@@@')
                        
                        queried_value = line_list[search_array['line_index']]

                        if search_term == 'fit_stat': 
                            fit_stat = float(queried_value)
                            dof_line_list = (re.sub(' +', '@@@', f_lines[line_index+3])).split('@@@')

                            dof = float(dof_line_list[7])

                            results_dict['reduced_fit_stat'].append(fit_stat/dof)

                        results_dict[search_term].append(queried_value)

                        break    
            
df = pd.DataFrame.from_dict(results_dict, orient='columns')

'''
for dict_list in results_dict.values(): 
    print(len(dict_list))
'''

nthcomp_df = pd.read_csv('./data/processed/2022/wrangled_nthcomp_spectral_data.csv')
nthcomp_df = nthcomp_df.rename(columns={'fit_stat':'nthcomp_fit_stat', 
                                        'reduced_fit_stat':'nthcomp_reduced_fit_stat'})

cols_to_drop = ['tin_before_error', 'diskbb_norm_before_error', 'gamma_before_error',
               'nthcomp_norm_before_error', 'nthcomp_fit_stat', 'nthcomp_reduced_fit_stat',
               'tin_after_error', 'diskbb_norm_after_error', 'gamma_after_error',
               'nthcomp_norm_after_error']

non_nthcomp_info_df = nthcomp_df.drop(columns=cols_to_drop)

all_values_df = df.merge(nthcomp_df, left_on='full_ids', right_on='full_ids')

df = df.merge(non_nthcomp_info_df, left_on='full_ids', right_on='full_ids')

df.to_csv('./data/processed/2022/simpl_wrangled.csv', index=False)


all_values_df.to_csv('./data/processed/2022/simpl_AND_nthcomp.csv', index=False)

old_qpo_df = pd.read_csv('./data/processed/2021/fixed_merged.csv')
old_qpo_df = pd.DataFrame(list(zip(old_qpo_df['out_ids'], old_qpo_df['num_qpos'])), columns=['out_ids', 'num_qpos'])

with_old_qpo_df = all_values_df.merge(old_qpo_df, left_on='full_ids', right_on='out_ids')

corr_df_cols = ['simpl_tin','simpl_diskbb_norm','simpl_gamma','simpl_FracScat','net_source_count_rate','hardness_ratio', 'num_qpos']
corr_df = with_old_qpo_df.drop(columns=[i for i in list(df) if i not in corr_df_cols])

corr_df = corr_df.drop(columns=['tin_before_error', 'diskbb_norm_before_error', 
                                'gamma_before_error', 'nthcomp_norm_before_error', 
                                'nthcomp_fit_stat', 'nthcomp_reduced_fit_stat', 'tin_after_error',
                                 'diskbb_norm_after_error', 'gamma_after_error', 
                                 'nthcomp_norm_after_error', 'out_ids'])

print(corr_df['simpl_gamma'])

corr_df = corr_df.astype(float)

corr_df = corr_df.corr()

sns.set(font_scale=0.5)
plt.style.use('seaborn-darkgrid')
plt.rcParams['font.family']='serif'
plt.rcParams['figure.dpi']=150
plt.rcParams['mathtext.fontset'] = 'cm'

fig, ax = plt.subplots(figsize=(6, 3))
mask = np.triu(np.ones_like(corr_df, dtype=bool))

tick_labels = ['diskbb '+r'$\mathrm{T}_{\mathrm{in}}$', 'diskbb norm', 'simpl '+r'$\Gamma$', 'Scattered Fraction', 'Net Source Count Rate', 'Hardness Ratio', '# QPO']

sns.heatmap(corr_df, mask=np.zeros_like(corr_df, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax, annot=True, annot_kws={'fontsize':'small'}, yticklabels=tick_labels,
            xticklabels=tick_labels)

plt.savefig('./code/xspec_related/spectral_routines/jan-29-simpl/simpl_corr.png', dpi=150, bbox_inches='tight')