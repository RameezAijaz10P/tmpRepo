import itertools
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from common import stores_dir, clean_words

description_key_word_array = []
max_keywords = 14


def create_transactions(keywords_array):
    all_transactions_arr = []
    for keywords in keywords_array:
        peril = keywords.pop(0)
        max_range = 3 if len(keywords) >= 3 else len(keywords) + 1  # Max range not inclusive
        for length in range(1, max_range):
            for subset in itertools.combinations(keywords, length):  # For each combination
                if len(subset) > 0:
                    all_transactions_arr.append([peril] + list(subset))
    te = TransactionEncoder()
    te_ary = te.fit(all_transactions_arr).transform(all_transactions_arr)
    df_matrix = pd.DataFrame(te_ary, columns=te.columns_)
    store_name = stores_dir + 'transaction_store.h5'
    store = pd.HDFStore(store_name)
    store['df'] = df_matrix
    store.close()


df = pd.read_csv('/CSVs/trainData.csv')

for idx, description in df['FAILURE_DESCRIPTIVE_TEXT'].iteritems():
    description_keywords = [df.at[idx, 'COVERED_EVENT_CODE']] + clean_words(description.split())
    description_key_word_array.append(description_keywords[:max_keywords])

create_transactions(description_key_word_array)
