def hunter_mk1(key, data_dir): 
    import numpy as np
    import pandas as pd
    from tqdm import tqdm 
    from scipy.signal import find_peaks
    
    ids = np.array(pd.read_csv(key)['full_id'])

    for full_id in tqdm(ids): 
        df = pd.read_csv('./code/xspec_related/qpo_routines/jan-1-2022/final_logs/'+full_id+'.csv')

        freqs = np.array(df['freq'])
        norms = np.array(df['norm'])
        redchis = np.array(df['redchi'])
        widths = np.array(df['fwhm'])
        fitstats = np.array(df['fit_stat'])
        min_freq, max_freq = np.min(freqs), np.max(freqs)

        # Rec chi. "peaks" aka valleys
        neg_fitstats = -1*fitstats
        min_height = np.min(neg_fitstats)+14
        chiPeakIndices, _ = find_peaks(neg_fitstats, height=min_height)
        chiPeakFreqs = freqs[chiPeakIndices]
        chiPeakIndices = chiPeakIndices[np.logical_or(chiPeakFreqs<0.8, chiPeakFreqs>1.2)] # was originally ignored betweeen 0.9-1.1 

        canidate_freqs = chiPeakFreqs
        canidate_widths = widths[chiPeakIndices]
        canidate_norms = norms[chiPeakIndices]

        fundamental_index = np.argmax(neg_fitstats[chiPeakIndices])
        
        fundamental_freq = canidate_freqs[fundamental_index]

        harmonic_status = np.empty(shape=len(canidate_freqs), dtype=np.str)

        harmonic_status[fundamental_index] = 'f'

        for canidate in np.delete(canidate_freqs, fundamental_index): # within 1% !! 
            
            canidate_index = np.where(canidate_freqs==canidate)
            
            for n in range(2,4): 
                harmonic = n*fundamental_freq
                subharmonic = fundamental_freq/n

                if canidate/harmonic < 1.01 and canidate/harmonic > 0.99: 
                    harmonic_status[canidate_index] = 'h'

                elif canidate/subharmonic < 1.01 and canidate/subharmonic > 0.99:
                    harmonic_status[canidate_index] = 's'

