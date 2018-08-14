from TransformData import *

df = pd.read_csv('testData.csv')
tries = pd.read_hdf('Stores/trie.h5')

testing_objects = []

for idx, row in df.iterrows():
    keywords = clean_words(df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'].split())
    testing_objects.append({
        'real_peril': df.at[idx, 'COVERED_EVENT_CODE'],
        'keywords': keywords,
        'predicted_peril': [],
        'true_positive': -1,
        'false_positive': -1,
        'num_pred_perils': -1
    })


def recurse_add_probs(entry, dictionary, index, max_len):
    if index < max_len:
        word = entry['keywords'][index]
        if word in dictionary:
            entry['predicted_peril'].append(dictionary[word]['_peril'])
            recurse_add_probs(entry, dictionary[word], (index + 1), max_len)


# print tries
for entry in testing_objects:
    keywords_len = len(entry['keywords'])
    for idx in range(0, keywords_len):
        recurse_add_probs(entry, tries, idx, keywords_len)





