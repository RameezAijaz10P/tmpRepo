import pandas as pd
from mlxtend.frequent_patterns import apriori
from common import stores_dir, apriori_file_name, transaction_file_name

print "#### READING THE STORE FROM THE h5 #####"
df = pd.read_hdf(stores_dir + transaction_file_name, 'df')

print "#### running apriori #####"
df_apriori = apriori(df, min_support=0.01, use_colnames=True)

print "#### deleting dataframe #####"
del df

print "#### creating store #####"
store = pd.HDFStore(stores_dir + apriori_file_name)
store['df'] = df_apriori
store.close()

# scp -i ~/Downloads/take2.pem ubuntu@18.207.239.2:/dev/Stores/apriori_store_new.h5 /Users/patrick.krisko/Desktop
