import pandas as pd
from mlxtend.frequent_patterns import association_rules


keywords=['CRCKSCRN','LQDDMG','STOLEN','MLFUNC','UNRECOV']

df = pd.read_hdf('/Users/patrick.krisko/Desktop/apriori_store_new.h5', 'df')
df = association_rules(df, metric="confidence", min_threshold=.000000000000000000000000000001)
print df
# print df
def has_peril(transaction):
    for word in keywords:
        if word in transaction and len(transaction) > 1:
            return True
    return False

rules = []
for idx, row in df.iterrows():
    if has_peril(df.at[idx, 'antecedents']) or has_peril(df.at[idx, 'consequents']):
        rules.append({
            "consequents": list(df.at[idx, 'consequents']),
            "antecedents": list(df.at[idx, 'antecedents']),
            "combined": list(df.at[idx, 'consequents'])+list(df.at[idx, 'antecedents']),
            "support": df.at[idx, 'support'],
            "confidence": df.at[idx, 'confidence']
        })
    # print list(df.at[idx, 'itemsets'])
    # if has_peril(df.at[idx, 'consequents']):
    #     rules.append({
    #         "rule": list(df.at[idx, 'consequents']),
    #         "support": df.at[idx, 'support']
    #     })

def get_peril(rule_list):
    for word in rule_list:
        if word in keywords:
            return word
    return ""

def get_perilless(rule_list, peril):
    perilless = []
    for word in rule_list:
        if not(word is peril):
            perilless.append(word)
    return perilless

prediction= {}
def perilExistInPrediction(prediction_list, peril):
    idx =0;
    for prediction in prediction_list:
        if peril is prediction['name']:
            return idx
        idx = idx +1
    return -1

# def getIndexOfPeril(prediction)

for rule in rules:
    peril = get_peril(rule['combined'])
    other_words = get_perilless(rule['combined'], peril)
    confidence = rule['confidence']
    support = rule['support']
    # for word in other_words:
    #     if not(word in prediction):
    #         prediction[word] = [{
    #             "name": peril,
    #             "support": support,
    #             "confidence": confidence
    #         }]
    #     else: # Word is in prediction
    #         for peril_type_obj in prediction[word]:
    #             if

#
# for rule in rules: # {antecedents: [...,...], consequents: [],
#     print rule
#     for word in rule['combined']:
#         if word not in keywords and word not in prediction:
#             prediction[word] = []
#             continue
#
#
#         if word in prediction: # we know its not a keyword
#             # if len(prediction[word]) is 0: # prediction[word] = []
#             #     prediction[word].append({
#             #         "name": get_peril(rule['combined']),
#             #         "support": rule['support'],
#             #         "confidence": rule['confidence']
#             #     })
#             # else:
#             #     # peril does exist
#             peril = get_peril(rule['combined'])
#
#             if perilExistInPrediction(prediction[word], peril) > -1:
#                 support = rule['support']
#                 index = perilExistInPrediction(prediction[word], peril)
#                 if support > prediction[word][index]['support']:
#                     prediction[word][index] = {
#                         "name": peril,
#                         "support": rule['support'],
#                         "confidence": rule['confidence']
#                     }
#             else: # peril does not exist
#                 prediction[word].append({
#                     "name": get_peril(rule['combined']),
#                     "support": rule['support'],
#                     "confidence": rule['confidence']
#                 })
            #
            #
            #
            # if len(prediction[word]) >0:
            #     peril = get_peril(rule, prediction[word]['name'])

# for key in prediction:
#     print key
# print prediction['still']
# {
#     crack: [{name : crk, support:0.5}]
# }