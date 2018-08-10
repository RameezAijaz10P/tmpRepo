import os
import pandas as pd
from mlxtend.frequent_patterns import apriori

no_of_stores = 5
frames=[]
for store in range(0, no_of_stores):
    print "### adding store "+str(store)
    df = pd.read_hdf('/dev/Stores/store_'+str(store)+'.h5', 'df')
    frames.append(pd.read_hdf('/dev/Stores/store_'+str(store)+'.h5', 'df'))

for store in range(0, no_of_stores):
    if store == 0:
        df1.to_csv('file.csv', index=False)
    frames[store].to_csv('/dev/Stores/file.csv', index=False)
    del frames[store]


print "#### concatinating dataframes #####"

result = pd.read_csv('/dev/Stores/file.csv')

print "#### running fillna #####"
result = result.fillna(False)

print "#### training modal #####"
df_apriori = apriori(result, min_support=0.6)
del result

store = pd.HDFStore('/dev/Stores/apriori_store.h5')
store['df'] = df_apriori
store.close()