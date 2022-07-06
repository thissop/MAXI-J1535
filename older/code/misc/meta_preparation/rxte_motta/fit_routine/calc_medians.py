def weighted_median(data, weights):
    """
    Args:
      data (list or numpy.array): data
      weights (list or numpy.array): weights
    """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = 0.5 * sum(s_weights)
    if any(weights > midpoint):
        w_median = (data[weights == np.max(weights)])[0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx:idx+2])
        else:
            w_median = s_data[idx+1]
    return w_median

def calc_them(output:str): 
    import pandas as pd
    import numpy as np

    df = pd.read_csv(output)


    objects = np.array(df['source'])
    objects_set = list(set(objects))
    all_nhs = np.array(df['nH'])
    all_rollovers = np.array(df['kT_e'])
    all_red_stats = np.array(df['red_pgstat'])

    median_nhs = []
    median_rollovers = []
    

    for source in objects_set: 
        mask = np.where(objects==source)[0]
        source_nhs = all_nhs[mask]
        source_rollovers = all_rollovers[mask]
        red_stats = 1/all_red_stats[mask]

        median_nhs.append(weighted_median(source_nhs, red_stats))
        median_rollovers.append(weighted_median(source_rollovers, red_stats))

    median_df = pd.DataFrame(list(zip(objects_set, median_nhs, median_rollovers)), 
                             columns=['source', 'median nH', 'median kTe'])

    median_df.to_csv('medians.csv', index=False)


