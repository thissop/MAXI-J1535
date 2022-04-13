def quick_plots(
    plot_dir: str = './code/xspec_related/qpo_routines/full_aggregation/post_agg_summary_things', 
    results_file: str ='./data/processed/2022/new_current_qpos.csv'): 

    import pandas as pd 

    import numpy as np

    import matplotlib.pyplot as plt

    df = pd.read_csv(results_file)

    num_qpos = np.array(df['num_qpos'])

    plt.hist(num_qpos)
    plt.xlabel('num qpos')
    plt.ylabel('count')

    plt.savefig(plot_dir+'/num_qpos.png')

    plt.clf()
    plt.close()

    plt.hist(df['confidence_class'])
    plt.xlabel('confidence class')
    plt.ylabel('count')
    plt.savefig(plot_dir+'/confidence_classes.png')

quick_plots()