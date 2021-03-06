from __future__ import division
import pickle
import pandas as pd
from common import clean_words, peril_types, stores_dir, pkl_file_name


test_df = pd.read_csv('CSVs/testData.csv')
test_objects = []
summary = {'correct_count': 0, 'correct_count_1': 0, 'correct_count_2': 0,'incorrect_count': 0, 'incorrect_entries': []}


class TestObject:
    def __init__(self, real_peril, keywords, story):
        self.real_peril = real_peril
        self.keywords = keywords
        self.predicted_perils = {}
        for keyword in keywords:
            self.predicted_perils[keyword] = {}
            for peril_type in peril_types:
                self.predicted_perils[keyword][peril_type] = {}
        self.true_positive = -1
        self.false_positive = -1
        self.winners = {}
        self.story = story

    def get_info(self):
        return {
            'real_peril': self.real_peril,
            'keywords': self.keywords,
            'winners': self.winners,
            'story': self.story
        }

    def num_keywords(self):
        return len(self.keywords)

    # Return the perils with top 2 confidence, with associated names and confidence level
    def get_best_2(self):
        winners_obj = {}
        for peril_type in peril_types:
            winners_obj[peril_type] = {'confidence': -1, 'support': -1}
        for word in self.predicted_perils:
            for peril_key in winners_obj:
                peril_obj = self.predicted_perils[word][peril_key]
                # If confidence level for word is greater than what has been seen before, replace
                if peril_obj != {} and peril_obj['confidence'] > winners_obj[peril_key]['confidence']:
                    winners_obj[peril_key]['confidence'] = peril_obj['confidence']
                    winners_obj[peril_key]['support'] = peril_obj['support']
        # Keep track of top 2 perils, with their confidence
        primary_peril, secondary_peril, primary_conf, secondary_conf = '', '', -1, -1
        for peril_name in winners_obj:
            curr_conf = winners_obj[peril_name]['confidence']
            if primary_peril == '':
                primary_peril, primary_conf = peril_name, curr_conf
            elif curr_conf > primary_conf:
                secondary_peril, secondary_conf = primary_peril, primary_conf
                primary_peril, primary_conf = peril_name, curr_conf
        return {
            'primary': {'peril': primary_peril, 'confidence': primary_conf},
            'secondary': {'peril': secondary_peril, 'confidence': secondary_conf}
        }


# Work way recursively through trie-dictionary, adding _peril to the test object 'entry'
def traverse_trie(entry, orig_word, dictionary, index):
    if index < entry.num_keywords():  # Outside of keywords array
        word = entry.keywords[index]  # Word can be at deeper level of trie dictionary
        if word in dictionary and '_peril' in dictionary[word]:  # If word is in current level of trie dictionary
            for peril_obj in dictionary[word]['_peril']:
                peril_name = peril_obj['peril']
                entry.predicted_perils[orig_word][peril_name] = {
                    'confidence': peril_obj['confidence'],
                    'support': peril_obj['support']
                }
            traverse_trie(entry, orig_word, dictionary[word], (index + 1))


# Create a "test object" for each row in the Data Frame.
for idx, row in test_df.iterrows():
    keywords = clean_words(test_df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'])
    curr_peril = test_df.at[idx, 'COVERED_EVENT_CODE']
    NewTestObj = TestObject(curr_peril, keywords, test_df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'])
    test_objects.append(NewTestObj)

with open(stores_dir + pkl_file_name, 'rb') as handle:
    trie = pickle.load(handle)
    for test_obj in test_objects:
        for idx in range(0, test_obj.num_keywords()):
            start_word = test_obj.keywords[idx]
            traverse_trie(test_obj, start_word, trie, idx)
        test_obj.winners = test_obj.get_best_2()
        if test_obj.real_peril == test_obj.winners['primary']['peril']:
            summary['correct_count'] += 1
            summary['correct_count_1'] += 1
        elif test_obj.real_peril == test_obj.winners['secondary']['peril']:
            summary['correct_count_2'] += 1
            summary['correct_count'] += 1
        else:
            summary['incorrect_count'] += 1
            summary['incorrect_entries'].append(test_obj.get_info())

total = summary['correct_count'] + summary['incorrect_count']
print '########## SUMMARY ###########'
print '######### TESTING %d ROWS ###########\n\n' % total
print 'Correct Within Top 2', summary['correct_count'], "%.4f%%" % ((summary['correct_count']/ total) * 100)
print 'First Winner Correct', summary['correct_count_1'], "%.4f%%" % ((summary['correct_count_1']/total) * 100)
print 'Second Winner Correct', summary['correct_count_2'], "%.4f%%" % ((summary['correct_count_2']/total) * 100)
print 'Incorrect', summary['incorrect_count'], "%.4f%%" % ((summary['incorrect_count']/total) * 100)

'''
bad_columns = ['actual', 'story', 'keywords', 'top', 'confidence', 'second', 'confidence']
rows = []

for entry in summary['incorrect_entries']:
    rows.append([
        entry['real_peril'],
        entry['story'],
        entry['keywords'],
        entry['winners']['primary']['peril'],
        entry['winners']['primary']['confidence'],
        entry['winners']['secondary']['peril'],
        entry['winners']['secondary']['confidence']
    ])

bad_df = pd.DataFrame(rows, columns=bad_columns)
bad_df.to_csv('CSVs/wrong.csv')
'''
