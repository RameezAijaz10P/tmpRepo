import pandas as pd

df = pd.read_hdf('/Users/patrick.krisko/Desktop/apriori_store_new.h5', 'df')
print df
df.to_csv('./Stores/ass.csv')
