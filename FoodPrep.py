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
    for word in keywords:
        new_obj['predicted_perils'][word] = {
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
    return num - (num%.1)


def get_best_2(test_obj):
    winners_obj = {
        'CRCKSCRN': {'confidence': -1, 'support': -1},
        'LQDDMG': {'confidence': -1, 'support': -1},
        'MLFUNC': {'confidence': -1, 'support': -1},
        'LOST/UNREC': {'confidence': -1, 'support': -1},
        'STOLEN': {'confidence': -1, 'support': -1}
    }
    for keyword in test_obj['predicted_perils']:  # Collecting all the perils from all keywords to one winner obj replacing the higher conf with lower
        for peril_key in winners_obj:
            peril_obj = test_obj['predicted_perils'][keyword][peril_key]
            if peril_obj != {} and peril_obj['confidence'] > winners_obj[peril_key]['confidence']:
                winners_obj[peril_key]['confidence'] = peril_obj['confidence']
                winners_obj[peril_key]['support'] = peril_obj['support']
    numba_1 = { # REFACTOR THE OBJECTS
        "peril": "",
        "confidence": -1
    }
    numba_2 = { # JUST. DO IT.
        "peril": "",
        "confidence": -1
    }
    for peril_name in winners_obj: # Getting winner out of winner obj
        curr_conf = winners_obj[peril_name]["confidence"]
        if numba_1["peril"] == "":
            numba_1["peril"] = peril_name
            numba_1["confidence"] = curr_conf
        elif curr_conf > numba_1["confidence"]:
            numba_2["confidence"] = numba_1["confidence"]
            numba_2["peril"] = numba_1["peril"]
            numba_1["peril"] = peril_name
            numba_1["confidence"] = curr_conf
    return {"numba1": numba_1, "numba2": numba_2}


summary = {"correct_count":0, "incorrect_count":0, "incorrect_entries":[]}

with open('Stores/trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)
    for test_obj in test_objects:
        keywords_len = len(test_obj['keywords'])
        for idx in range(0, keywords_len):
            orig_word = test_obj['keywords'][idx]
            traverse_trie(test_obj, orig_word, trie, idx, keywords_len)
        test_obj['winners'] = get_best_2(test_obj)
        if test_obj['real_peril'] == test_obj['winners']['numba1']['peril'] or test_obj['real_peril'] == test_obj['winners']['numba2']['peril']:
            summary["correct_count"] = summary["correct_count"] + 1
        else:
            summary["incorrect_count"] = summary["incorrect_count"] + 1
            summary["incorrect_entries"].append(
                {
                    'real_peril': test_obj['real_peril'],
                    'keywords': test_obj['keywords'],
                    'winner': test_obj['winners']
                }
            )


print "\n\n ########## SUMMARY ########### \n\n"

print "correct_count", summary["correct_count"]

print "\n\n incorrect_count", summary["incorrect_count"]

# for incorrect_shit in summary['incorrect_entries']:
#     print "\n"
#     print "Actual Peril", incorrect_shit['real_peril']
#     print "Keywords", incorrect_shit['keywords']
#     print "Model Predicted Peril", incorrect_shit['winner']['winner']
#     for peril in incorrect_shit['winner']['all_perils']:
#         if incorrect_shit['winner']['all_perils'][peril]['confidence'] >= .5:
#             print "--->", peril, incorrect_shit['winner']['all_perils'][peril]
#             #
#             # print incorrect_shit['winner']['peril']

# def get_winner(entry):
#     winners_obj = {
#         'CRCKSCRN': {'confidence': -1, 'support': -1},
#         'LQDDMG': {'confidence': -1, 'support': -1},
#         'MLFUNC': {'confidence': -1, 'support': -1},
#         'LOST/UNREC': {'confidence': -1, 'support': -1},
#         'STOLEN': {'confidence': -1, 'support': -1}
#     }
#     for key in entry['predicted_perils']: # Collecting all the perils from all keywords to one winner obj replacing the higher conf with lower
#         for peril_key in winners_obj:
#             peril_obj = entry['predicted_perils'][key][peril_key]
#             if peril_obj != {} and peril_obj['confidence'] > winners_obj[peril_key]['confidence']:
#                 winners_obj[peril_key]['confidence'] = peril_obj['confidence']
#                 winners_obj[peril_key]['support'] = peril_obj['support']
#     highest_prod = -1
#     highest_conf = -1
#     winner_peril = ""
#     for peril in winners_obj: # Getting winner out of winner obj
#         curr_conf = winners_obj[peril]["confidence"]
#         curr_product = curr_conf * winners_obj[peril]["support"]
#         if curr_conf > highest_conf:
#             winner_peril = peril
#             highest_conf = curr_conf
#             highest_prod = curr_product
#     return {'winner': winner_peril, 'confidence': highest_prod, 'all_perils': winners_obj}




