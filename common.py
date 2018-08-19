import re
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize
from nltk.corpus import stopwords

peril_types = ['LOST/UNREC', 'STOLEN', 'MLFUNC', 'CRCKSCRN', 'LQDDMG']
stores_dir = 'Stores/'
apriori_file_name = 'apriori_store_01.h5'
transaction_file_name = 'transaction_store.h5'
pkl_file_name = 'tries.pkl'
stop_words = set(stopwords.words('english'))


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


def get_trigrams(peril, keywords):
    unigrams = map(lambda word: peril + [word], keywords)
    bigrams = map(lambda tup: peril + list(tup), zip(keywords, keywords[1:]))
    trigrams = map(lambda tup: peril + list(tup), zip(keywords, keywords[1:], keywords[2:]))
    return unigrams + bigrams + trigrams
