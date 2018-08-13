import pandas as pd
import numpy as np

MIN = 764
df = pd.read_csv("clean-peril-data.csv")
df = df.drop_duplicates()
# REMOVALS
df = df.loc[df['COVERED_EVENT_CODE']!='OTHER',:]
df = df.loc[df['COVERED_EVENT_CODE']!='NOTSATDEV',:]
# COMBINE LOST / STOLEN
df['COVERED_EVENT_CODE'] = np.where(df['COVERED_EVENT_CODE'].isin(['LOST', 'UNRECOV']), 'LOST/UNREC', df['COVERED_EVENT_CODE'])
counters = {'LOST/UNREC': 0, 'STOLEN': 0, 'LQDDMG': 0, 'CRCKSCRN': 0, 'MLFUNC': 0}
# FOR EACH ROW IN DF
drop_idxs = []
for idx, row in df.iterrows():
    counters[df.at[idx, 'COVERED_EVENT_CODE']] = counters[df.at[idx, 'COVERED_EVENT_CODE']] + 1
    if counters[df.at[idx, 'COVERED_EVENT_CODE']] > MIN:
        drop_idxs.append(idx)
df = df.drop(drop_idxs)
df.to_csv('ass.csv', index=False)
