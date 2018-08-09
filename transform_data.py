import os
import re
from multiprocessing import Process
import pandas as pd
from nltk.corpus import stopwords
from itertools import combinations
from mlxtend.preprocessing import TransactionEncoder

peril_stops = ['']
stop_words = set(stopwords.words('english') + peril_stops)
max_no_of_keywords = 14
stores_dir_name = 'Stores'

if not os.path.exists(stores_dir_name):
    os.makedirs(stores_dir_name)

# Data Import and Reformat
df = pd.read_csv("testData.csv", encoding="latin2")
df = df.drop_duplicates()
df = df.drop(columns={"CUSTOMER_CASE_NBR", "NAME", "CREATED_DATE"})
df = df.rename(columns={"COVERED_EVENT_CODE": "ptype", "FAILURE_DESCRIPTIVE_TEXT": "description"})


def clean_desc(descr):
    desc = (re.sub(r'[^a-zA-Z ]', ' ', descr)).lower()  # Replace all non alpha / space characters
    desc = list(filter(lambda word: not(word in stop_words), desc.split(' ')))  # Filter out stop words
    return desc[:max_no_of_keywords]


def create_transactions(data_frame, process_no=1):
    all_transactions = []
    for idx, row in data_frame.iterrows(): # For each row
        keywords = clean_desc(row['description'])  # A list of key terms from description
        for length in range(1, len(keywords) + 1):
            for combo in list(combinations(keywords, length)):
                transaction = [row['ptype']] + list(combo)
                all_transactions.append(transaction)
    te = TransactionEncoder()
    te_array = te.fit(all_transactions).transform(all_transactions)
    df2 = pd.DataFrame(te_array, columns=te.columns_)
    store_name = '%s/store_%d.h5' % (stores_dir_name, process_no)
    print("Process %d writing %s" % (process_no, store_name))
    store = pd.HDFStore(store_name)
    store['df'] = df2
    store.close()


print("##### Processing Descriptions Keywords ######\n")

processes = []
total = len(df)
no_of_processes = total if total < 5 else 5
size = int(total/no_of_processes)

print('Total # of Processes: %d' % no_of_processes)
print('Total # of Rows: %d' % total)
print('Total # of Rows per Process: %d' % size)

for idx in range(no_of_processes):
    start = idx * size
    end = (idx + 1) * size
    if idx == no_of_processes - 1:
        end = total
    print("Process #%d processing keywords from %d to %d" % (idx, start, end))
    p = Process(target=create_transactions, args=(df[start:end], idx,))
    p.start()
    processes.append(p)
