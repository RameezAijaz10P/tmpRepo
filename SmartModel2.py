import pandas as pd
from mlxtend.frequent_patterns import association_rules
# from TransformData import peril_types
from TransformData import store_dir

peril_types=['CRCKSCRN', 'LQDDMG', 'STOLEN', 'MLFUNC', 'UNRECOV']

# df = pd.read_hdf('/Users/patrick.krisko/Desktop/apriori_store_new.h5', 'df')
df = pd.read_hdf(store_dir + "apriori_store.h5")
df = association_rules(df, metric='confidence', min_threshold=.000000000000000000000000000001)


def keyify_set(words):
    words = list(words)
    words = map(lambda word: str(word), words)
    words = sorted(words)
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
    print 'Rule:',  rule
    print 'Perils:'
    for match in rules_dict[rule]:
        print "-->"+match['peril']