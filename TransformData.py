import itertools
import re
import pandas as pd
from nltk.corpus import stopwords
from mlxtend.preprocessing import TransactionEncoder
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize

peril_types = ['LOST/UNREC', 'STOLEN', 'MLFUNC', 'CRCKSCRN', 'LQDDMG']
stop_words = set(stopwords.words('english'))

description_key_word_array = []
max_no_of_keywords = 14
store_dir = "Stores/"


def clean_words(words):
    keywords = []
    for word in words:
        word = word.lower()
        if word not in stop_words:
            word = re.sub('[^A-Za-z]+', '', word)
            if word is not '':
                word = WordNetLemmatizer().lemmatize(word, 'v')
                word = singularize(word)
                keywords.append(str(word))
    return keywords



def contains_peril(sub_set, peril_name):
    for item in sub_set:
        if item == peril_name:
            return True
    return False


def create_transactions(keywords_array):
    all_transactions_arr = []
    for keywords in keywords_array:
        peril = keywords[0]
        max_range = 5 if len(keywords) + 1 > 5 else len(keywords) + 1
        for length in range(0, max_range):
            for subset in itertools.combinations(keywords, length): # For each combination
                if contains_peril(subset, peril) and len(subset) > 1:
                    all_transactions_arr.append(list(subset))
    te = TransactionEncoder()
    te_ary = te.fit(all_transactions_arr).transform(all_transactions_arr)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    store_name = store_dir + 'transaction_store.h5'
    store = pd.HDFStore(store_name)
    store['df'] = df
    store.close()


df = pd.read_csv("trainData.csv")


for idx, description in df['FAILURE_DESCRIPTIVE_TEXT'].iteritems():
    description_keywords = [df.at[idx, 'COVERED_EVENT_CODE']] + clean_words(description.split())
    description_key_word_array.append(description_keywords[:max_no_of_keywords])


create_transactions(description_key_word_array)
