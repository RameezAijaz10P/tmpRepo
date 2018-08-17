import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize
stop_words = set(stopwords.words('english'))
test_df = pd.read_csv('testData.csv')

test_objects = []


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


for idx, row in test_df.iterrows():
    keywords = clean_words(test_df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'].split())
    new_obj = {
        'real_peril': test_df.at[idx, 'COVERED_EVENT_CODE'],
        'keywords': keywords,
        'predicted_perils': {},
        'true_positive': -1,
        'false_positive': -1
    }
    for keyword in keywords:
        new_obj['predicted_perils'][keyword] = {
            'CRCKSCRN': {},
            'LQDDMG': {},
            'LOST/UNREC': {},
            'STOLEN': {},
            'MLFUNC': {}
        }
    test_objects.append(new_obj)


def traverse_trie(entry, orig_word, dictionary, index, max_len):
    if index < max_len: # Outside of keywords array
        word = entry['keywords'][index] # Word can be at deeper level of trie dictionary
        if word in dictionary: # If word is in current level of trie dictionary
            for peril_obj in dictionary[word]['_peril']:
                peril_name = peril_obj['peril']
                entry['predicted_perils'][orig_word][peril_name] = {
                    'confidence': peril_obj['confidence'],
                    'support': peril_obj['support']
                }
            traverse_trie(entry, orig_word, dictionary[word], (index + 1), max_len)


def chop_off(num):
    return num - (num % .1)


def get_best_2(test_obj):
    winners_obj = {
        'CRCKSCRN': {'confidence': -1, 'support': -1},
        'LQDDMG': {'confidence': -1, 'support': -1},
        'MLFUNC': {'confidence': -1, 'support': -1},
        'LOST/UNREC': {'confidence': -1, 'support': -1},
        'STOLEN': {'confidence': -1, 'support': -1}
    }
    for keyword in test_obj['predicted_perils']:
        for peril_key in winners_obj:
            peril_obj = test_obj['predicted_perils'][keyword][peril_key]
            if peril_obj != {} and peril_obj['confidence'] > winners_obj[peril_key]['confidence']:
                winners_obj[peril_key]['confidence'] = peril_obj['confidence']
                winners_obj[peril_key]['support'] = peril_obj['support']
    primary_peril, secondary_peril, primary_conf, secondary_conf = '', '', -1, -1
    for peril_name in winners_obj:  # Getting winner out of winner obj
        curr_conf = winners_obj[peril_name]['confidence']
        if primary_peril == '':  # Uninitialized
            primary_peril, primary_conf = peril_name, curr_conf
        elif curr_conf > primary_conf:
            secondary_peril, secondary_conf = primary_peril, primary_conf
            primary_peril, primary_conf = peril_name, curr_conf
    return {
        'primary': {'peril': primary_peril, 'confidence': primary_conf},
        'secondary': {'peril': secondary_peril, 'confidence': secondary_conf
        }
    }


summary = {'correct_count': 0, 'incorrect_count': 0, 'incorrect_entries': []}

with open('Stores/trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)
    for test_obj in test_objects:
        keywords_len = len(test_obj['keywords'])
        for idx in range(0, keywords_len):
            orig_word = test_obj['keywords'][idx]
            traverse_trie(test_obj, orig_word, trie, idx, keywords_len)
        test_obj['winners'] = get_best_2(test_obj)
        if test_obj['real_peril'] == test_obj['winners']['primary']['peril'] or test_obj['real_peril'] == test_obj['winners']['secondary']['peril']:
            summary['correct_count'] = summary['correct_count'] + 1
        else:
            summary['incorrect_count'] = summary['incorrect_count'] + 1
            summary['incorrect_entries'].append({
                'real_peril': test_obj['real_peril'],
                'keywords': test_obj['keywords'],
                'winner': test_obj['winners']
            })


print '\n\n ########## SUMMARY ########### \n\n'

print 'correct_count', summary['correct_count']

print '\n\n incorrect_count', summary['incorrect_count']

# for incorrect_shit in summary['incorrect_entries']:
#     print '\n'
#     print 'Actual Peril', incorrect_shit['real_peril']
#     print 'Keywords', incorrect_shit['keywords']
#     print 'Model Predicted Peril', incorrect_shit['winner']['winner']
#     for peril in incorrect_shit['winner']['all_perils']:
#         if incorrect_shit['winner']['all_perils'][peril]['confidence'] >= .5:
#             print '--->', peril, incorrect_shit['winner']['all_perils'][peril]
#             #
#             # print incorrect_shit['winner']['peril']



