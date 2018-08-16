import pandas as pd
from mlxtend.frequent_patterns import association_rules
import pickle

df = pd.read_hdf('/Users/patrick.krisko/Desktop/apriori_store_0005.h5')
df = association_rules(df, metric='confidence', min_threshold=.000000000000000000000000000001)
peril_types = ['LOST/UNREC', 'STOLEN', 'MLFUNC', 'CRCKSCRN', 'LQDDMG']


def keyify_set(words):
    words = list(words)
    words = map(lambda word: str(word), words)
    words = frozenset(words)
    return words


rules_list = []
for idx, row in df.iterrows():
    consequents = set(df.at[idx, 'consequents'])
    consequent = consequents.pop()
    if len(consequents) is 0 and consequent in peril_types:
        rules_list.append({
            'peril': consequent,
            'associated_words': keyify_set(df.at[idx, 'antecedents']),
            'support': df.at[idx, 'support'],
            'confidence': df.at[idx, 'confidence']
        })

rules_dict = {}
for rule in rules_list:
    new_obj = {
        'peril': rule['peril'],
        'support': rule['support'],
        'confidence': rule['confidence']
    }
    if rule['associated_words'] not in rules_dict:
        rules_dict[rule['associated_words']] = []
    rules_dict[rule['associated_words']].append(new_obj)

for rule in rules_dict:
    rules_dict[rule].sort(key=lambda x: x['confidence'], reverse=True)


def create_trie(*rules):
    root = dict()
    for rule in rules_dict:
        current_dict = root
        for word in rule:
            current_dict = current_dict.setdefault(word, {})
        current_dict['_peril'] = rules_dict[rule]
    return root


root = create_trie(rules_dict)
with open('Stores/trie.pickle', 'wb') as handle:
    pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)


