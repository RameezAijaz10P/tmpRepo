import re
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize
from nltk.corpus import stopwords

peril_types = ['LOST/UNREC', 'STOLEN', 'MLFUNC', 'CRCKSCRN', 'LQDDMG']
stores_dir = '/Stores'
apriori_file_name = 'apriori_store_01.h5'
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
