import itertools
import os
import re
from multiprocessing import Process
import pandas as pd
from nltk.corpus import stopwords
from time import time
from mlxtend.preprocessing import TransactionEncoder
stop = stopwords.words('english')

cereal_df = pd.read_csv("testData.csv")

# Are they the same?
perilKeyWordMap = {}

description_key_word_array = []
long_description_key_word_array = []
max_no_of_keywords = 16


for eventCode in cereal_df['COVERED_EVENT_CODE']:
    perilKeyWordMap[eventCode] = [eventCode]

for idx, description in cereal_df['FAILURE_DESCRIPTIVE_TEXT'].iteritems():
    description_keywords = [cereal_df['COVERED_EVENT_CODE'][idx]]
    for word in description.split():
        word = word.lower()
        if word not in stop:
            word = re.sub('[^A-Za-z0-9]+', '', word)
            description_keywords.append(word)

    description_key_word_array.append(description_keywords[:max_no_of_keywords])
    if len(description_keywords) >= max_no_of_keywords:
        long_description_key_word_array.append(description_keywords)


print "____KeyWordArray____"
print description_key_word_array


def create_transactions(keywords_array, process_no=1, long_keywords=False):
    def contains_peril(sub_set, peril_name):
        if len(sub_set) < 2:
            return False
        for item in sub_set:
            if item == peril_name:
                return True
        return False
    # all_transactions = ""
    all_transactions_arr = []
    for keywords in keywords_array:
        peril = keywords[0]
        # transactions = []
        for length in range(0, len(keywords) + 1):
            for subset in itertools.combinations(keywords, length):
                if contains_peril(subset, peril):
                    all_transactions_arr.append(list(subset))
            # if length == len(keywords):
            #     transactions[len(transactions)-1] += '\n'
        # all_transactions += '\n'.join(transactions)
        # all_transactions_arr.append(transactions)
    te = TransactionEncoder()
    te_ary = te.fit(all_transactions_arr).transform(all_transactions_arr)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    store_name = 'Stores/store_'+str(process_no)+'.h5'
    print "Process no " + str(process_no) + " writing " + store_name
    store = pd.HDFStore(store_name)
    store['df'] = df
    store.close()
    # with open(os.path.join('Transactions', file_name), "w") as text_file:
    #         text_file.write(all_transactions)


# create_transactions(description_key_word_array)

print "##### Processing Descriptions Keywords ######"

print"###########################################"

transactions_folder = 'Stores'
if not os.path.exists(transactions_folder):
    os.makedirs(transactions_folder)


t0 = time()
processes = []
total = len(description_key_word_array)
no_of_processes = total if total < 5 else 5
size = int(total/no_of_processes)
print 'total no. of processes '+str(no_of_processes)
print 'total no. of rows '+str(total)
print 'total no of rows per process '+str(size)
for i in range(no_of_processes):
    start = i*size
    end = (i+1)*size
    if i == no_of_processes-1:
        end = total
    print "Process " + str(i) + " processing keywords from " + str(start) + " to " + str(end)
    p = Process(target=create_transactions, args=(description_key_word_array[start:end], i,))
    p.start()
    # p.join()
    processes.append(p)



print("Finished in %ss" % (time() - t0))
print "Number of description having more than "+str(max_no_of_keywords)+" keywords: "+str(len(long_description_key_word_array))

# for peril, keywords in perilKeyWordMap.iteritems():
#     for length in range(0, len(keywords) + 1):
#         for subset in itertools.combinations(keywords, length):
#             print(len(subset))
#             if contains_peril(subset, peril):
#                 file_text.append(', '.join(subset))




# with open("output_"+process_no+".txt", "w") as text_file:
#     for peril, keywords in perilKeyWordMap.iteritems():
#         text_file.write("{0}".format(peril) + " : {0}".format())



# print "LENGTH"
# print file_text