import os
import pandas as pd
from mlxtend.frequent_patterns import apriori

no_of_stores = len([name for name in os.listdir('Stores') if os.path.isfile(os.path.join('Stores', name))])
frames=[]
for store in range(0, no_of_stores):
    print "### adding store "+str(store)
    df = pd.read_hdf('Stores/store_'+str(store)+'.h5', 'df')
    frames.append(pd.read_hdf('Stores/store_'+str(store)+'.h5', 'df'))

print "#### concatinating dataframes #####"

result = pd.concat(frames)

print "#### running fillna #####"
result = result.fillna(False)

print "#### training modal #####"
df_apriori = apriori(result, min_support=0.6)

store = pd.HDFStore('Stores/apriori_store')
store['df'] = df_apriori
store.close()
