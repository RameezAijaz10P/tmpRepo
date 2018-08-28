#!/usr/bin/env bash
echo 'Updating...'
sudo apt-get update

echo 'Installing Python 2.7'
sudo apt-get python2.7
sudo apt-get python-pip

echo 'Initializing Virtual Environment, getting Python Dependencies'
source ./venv/bin/activate
pip install pandas
pip install nltk
pip install mlxtend
pip install pattern
pip install tables

echo 'Getting NLTK packages'
python ./HelperScripts/install.py

echo 'Done!'
