import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.text.en import singularize
stop_words = set(stopwords.words('english'))
df = pd.read_csv('even-peril-data.csv')

testing_objects = []


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


for idx, row in df.iterrows():
    keywords = clean_words(df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'].split())
    new_obj = {
        'real_peril': df.at[idx, 'COVERED_EVENT_CODE'],
        'keywords': keywords,
        'predicted_perils': {},
        'true_positive': -1,
        'false_positive': -1,
        'num_pred_perils': -1
    }
    for word in keywords:
        new_obj['predicted_perils'][word] = {
            'CRCKSCRN': {},
            'LQDDMG': {},
            'LOST/UNREC': {},
            'STOLEN': {},
            'MLFUNC': {}
        }
    testing_objects.append(new_obj)


def recurse_add_probs(entry, orig_word, dictionary, index, max_len):
    if index < max_len:
        word = entry['keywords'][index]
        if word in dictionary:
            for peril in dictionary[word]['_peril']:
                peril_name = peril['peril']
                entry['predicted_perils'][orig_word][peril_name] = {
                    'confidence': peril['confidence'],
                    'support': peril['support']
                }
            recurse_add_probs(entry, orig_word, dictionary[word], (index + 1), max_len)


def chop_off(num):
    return num - (num%.1)


def get_winner(entry):
    winners_obj = {
        'CRCKSCRN': {'confidence': -1, 'support': -1},
        'LQDDMG': {'confidence': -1, 'support': -1},
        'MLFUNC': {'confidence': -1, 'support': -1},
        'LOST/UNREC': {'confidence': -1, 'support': -1},
        'STOLEN': {'confidence': -1, 'support': -1}
    }
    for key in entry['predicted_perils']: # Collecting all the perils from all keywords to one winner obj replacing the higher conf with lower
        for peril_key in winners_obj:
            peril_obj = entry['predicted_perils'][key][peril_key]
            if peril_obj != {} and peril_obj['confidence'] > winners_obj[peril_key]['confidence']:
                winners_obj[peril_key]['confidence'] = peril_obj['confidence']
                winners_obj[peril_key]['support'] = peril_obj['support']
    highest = -1
    winner_peril = ""
    for peril in winners_obj: # Getting winner out of winner obj
        if winners_obj[peril]["confidence"] > highest:
            if abs(winners_obj[peril]["confidence"] - highest) <= .1: # If confidence is not higher or lower than 0.1 consider support for winner
                if winners_obj[peril]['support'] > winners_obj[winner_peril]['support']:
                    winner_peril = peril
                    highest = winners_obj[peril]["confidence"]
            else:
                highest = winners_obj[peril]["confidence"]
                winner_peril = peril
    return {'winner': winner_peril, 'confidence': highest, 'all_perils': winners_obj}


summary = {"correct_count":0, "incorrect_count":0, "incorrect_entries":[]}

with open('Stores/trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)
    for entry in testing_objects:
        keywords_len = len(entry['keywords'])
        for idx in range(0, keywords_len):
            orig_word = entry['keywords'][idx]
            recurse_add_probs(entry, orig_word, trie, idx, keywords_len)
            entry['winners'] = get_winner(entry)
        # if 'winners' not in entry:
        #     print entry
        if 'winners' in entry and entry['real_peril'] == entry['winners']['winner']:
            summary["correct_count"] = summary["correct_count"] + 1
        else:
            summary["incorrect_count"] = summary["incorrect_count"] + 1
            if 'winners' in entry:
                summary["incorrect_entries"].append(
                    {
                        'real_peril': entry['real_peril'],
                        'keywords': entry['keywords'],
                        'winner': entry['winners']
                    }
                )




# # print testing_objects
# for obj in testing_objects:
#     print ""
#     print ""
#     print "Keywords", obj["keywords"]
#     print "real peril", obj["real_peril"]
#     print "winner", obj['winners']

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

        #     print incorrect_shit['winner']['peril']




