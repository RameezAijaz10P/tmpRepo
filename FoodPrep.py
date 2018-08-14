from TransformData import *

df = pd.read_csv('testData.csv')

testing_objects = []

for idx, row in df.iterrows():
    keywords = clean_words(df.at[idx, 'FAILURE_DESCRIPTIVE_TEXT'].split())
    testing_objects.append({
        'peril': df.at[idx, 'COVERED_EVENT_CODE'],
        'keywords': keywords
    })


for pkt in testing_objects:
    print pkt['peril'], pkt['keywords']
    # print pkt['peril'], pkt['keywords':3]
# print all_keywords_array
