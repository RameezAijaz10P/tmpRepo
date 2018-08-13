import pandas as pd
from mlxtend.frequent_patterns import apriori
no_of_stores = 5
frames=[]
print "#### READING THE STORE FROM THE h5 #####"
df = pd.read_hdf('Stores/store_1.h5', 'df')

# df = df.fillna(False)

print "#### running apriori #####"
df_apriori = apriori(df, min_support=0.00001, use_colnames=True)

print "#### deleting dataframe #####"
del df


print "#### creating store #####"
store = pd.HDFStore('Stores/apriori_store.h5')
store['df'] = df_apriori
store.close()

# scp -i ~/Downloads/take2.pem ubuntu@18.207.239.2:/dev/Stores/apriori_store_new.h5 /Users/patrick.krisko/Desktop