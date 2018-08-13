import pandas as pd
import numpy as np

min_count = 764 # From stolem
df = pd.read_csv("clean-peril-data.csv")
df = df.drop_duplicates()
df = df.loc[df['COVERED_EVENT_CODE']!='OTHER',:]
df['COVERED_EVENT_CODE'] = np.where(df['COVERED_EVENT_CODE'].isin(['LOST', 'UNRECOV']), 'LOST/UNREC', df['COVERED_EVENT_CODE'])
counters = {'LOST/UNREC': 0, 'STOLEN': 0, 'LQDDMG': 0, 'CRCKSRCN': 0, 'MLFUNC': 0}
for idx, row in df.iterrows():
    counters[df['COVERED_EVENT_CODE']] = counters[df['COVERED_EVENT_CODE']] + 1
    # print(df['COVERED_EVENT_CODE'])
print counters
df.to_csv('ass.csv', index=False)
