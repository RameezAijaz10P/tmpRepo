import itertools
import re
import pandas as pd
from nltk.corpus import stopwords
from mlxtend.preprocessing import TransactionEncoder
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize
stop = stopwords.words('english')

cereal_df = pd.read_csv("trainData.csv")

# Are they the same?
perilKeyWordMap = {}

description_key_word_array = []
long_description_key_word_array = []
max_no_of_keywords = 20


for eventCode in cereal_df['COVERED_EVENT_CODE']:
    perilKeyWordMap[eventCode] = [eventCode]
print " ### ### # #Reaching the cleaning phase and creating the map"
for idx, description in cereal_df['FAILURE_DESCRIPTIVE_TEXT'].iteritems():
    description_keywords = [cereal_df['COVERED_EVENT_CODE'][idx]]
    for word in description.split():
        word = word.lower()
        stopWordsList = [item.encode('utf8') for item in stop]
        if word not in stopWordsList:
            word = re.sub('[^A-Za-z]+', '', word)
            if word:
                word = WordNetLemmatizer().lemmatize(word, 'v')
                word = singularize(word)
                description_keywords.append(word)

    description_key_word_array.append(description_keywords[:max_no_of_keywords])
    if len(description_keywords) >= max_no_of_keywords:
        long_description_key_word_array.append(description_keywords)


print "###### made the keyword array"
print "###### length of keyword array :" + str(len(description_key_word_array))


print "##### Descriptive keyword array  ########"
print description_key_word_array


def create_transactions(keywords_array, process_no=1, long_keywords=False):
    def contains_peril(sub_set, peril_name):
        if len(sub_set) < 2:
            return False
        for item in sub_set:
            if item == peril_name:
                return True
        return False
    all_transactions_arr = []
    idx = 0
    for keywords in keywords_array:
        if idx % 100 == 0:
            print "Working on keywords " + str(idx)
        idx = idx + 1
        peril = keywords[0]
        max_range = 6 if len(keywords) + 1 > 6 else len(keywords)
        for length in range(0, max_range):
            for subset in itertools.combinations(keywords, length):
                if contains_peril(subset, peril):
                    all_transactions_arr.append(list(subset))
    print "Doing the Transaction Encoding"
    te = TransactionEncoder()
    print "Fitting the transaction Array"
    te_ary = te.fit(all_transactions_arr).transform(all_transactions_arr)
    print "Getting the data frame"
    df = pd.DataFrame(te_ary, columns=te.columns_)
    print "CREATING STORE"
    store_name = '/dev/Stores/store_'+str(process_no)+'.h5'
    store = pd.HDFStore(store_name)
    store['df'] = df
    store.close()
    print "Store created"

print "##### Processing Descriptions Keywords ######"

print"###########################################"
create_transactions(description_key_word_array)
