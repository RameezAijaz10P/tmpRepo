import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from common import stores_dir, clean_words, get_trigrams, transaction_file_name

description_key_word_array = []
max_keywords = 20


def create_transactions(keywords_array):
    all_transactions_arr = []
    for keywords in keywords_array:
        peril = keywords.pop(0)
        all_transactions_arr += get_trigrams([peril], keywords)
    te = TransactionEncoder()
    te_ary = te.fit(all_transactions_arr).transform(all_transactions_arr)
    df_matrix = pd.DataFrame(te_ary, columns=te.columns_)
    store_name = stores_dir + transaction_file_name
    store = pd.HDFStore(store_name)
    store['df'] = df_matrix
    store.close()


df = pd.read_csv('CSVs/trainData.csv')

for idx, description in df['FAILURE_DESCRIPTIVE_TEXT'].iteritems():
    description_keywords = [df.at[idx, 'COVERED_EVENT_CODE']] + clean_words(description)
    description_key_word_array.append(description_keywords[:max_keywords])

create_transactions(description_key_word_array)
