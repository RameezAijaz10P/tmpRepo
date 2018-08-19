import pandas as pd
from mlxtend.frequent_patterns import association_rules
import pickle
from common import peril_types, apriori_file_name, stores_dir, pkl_file_name

df = pd.read_hdf(stores_dir + apriori_file_name)
df = association_rules(df, metric='confidence', min_threshold=.000000000000000000000000000001)
rules_list = []
rules_dict = {}


def keyify_set(words):
    words = map(lambda word: str(word), list(words))
    return frozenset(words)


def create_trie():
    rt = dict()
    for key in rules_dict:
        current_dict = rt
        for word in key:
            current_dict = current_dict.setdefault(word, {})
        current_dict['_peril'] = rules_dict[key]
    return rt


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


root = create_trie()
with open(stores_dir + pkl_file_name, 'wb') as handle:
    pickle.dump(root, handle, protocol=pickle.HIGHEST_PROTOCOL)


