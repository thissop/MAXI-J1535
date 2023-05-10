from qpoml.main import collection


grs_qpo_path = 'final-push/data/pipeline/GRS/[QPO][regression].csv'
grs_context_path = 'final-push/data/pipeline/GRS/[scalar-input][regression].csv'

collec.load(qpo_csv=qpo_path, context_csv=context_path,
                    context_preprocess=context_preprocess_dict, qpo_preprocess=qpo_preprocess_dict, units=units, approach='regression') 
