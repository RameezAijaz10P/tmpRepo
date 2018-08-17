echo 'Updating...'
sudo apt-get update

echo 'Installing Python 2.7'
sudo apt-get python2.7
sudo apt-get python-pip

echo 'Initializing Virtual Environment, getting Python Dependencies'
source /venv/bin/activate
pip install pandas
pip install nltk
pip install mlxtend
pip install pattern
pip install tables

echo 'Getting NLTK packages'
python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
exit()

echo 'Creating Store directories and files'
sudo mkdir /dev/Stores
sudo touch transaction_store.h5
sudo touch apriori_store_01.h5
sudo touch apriori_store_001.h5
sudo touch apriori_store_0005.h5
sudo chmod a+w transaction_store.h5
sudo chmod a+w apriori_store_01.h5
sudo chmod a+w apriori_store_001.h5
sudo chmod a+w apriori_store_0005.h5

echo 'Done!'
