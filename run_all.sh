#!/usr/bin/env bash
conf_file='HelperScripts/conf.txt'

if [ ! -f ${conf_file} ]
then
touch ${conf_file}
chmod a+w ${conf_file}
chmod a+r ${conf_file}
fi

echo What level of confidence would you like to run/test on, my dude?
read conf

echo ${conf} > ${conf_file}

read -r -p "Do you need to create transactions? [Y/n] " createTr
read -r -p "Do you need to train the model transactions? [Y/n] " trainMo

case "$createTr" in
    [yY][eE][sS]|[yY])
        echo Generating transactions
        python generate_transactions.py
        ;;
    *)
esac

case "$trainMo" in
    [yY][eE][sS]|[yY])
        echo Training the model at confidence level ${conf}
        python train_model.py
        ;;
    *)
esac

# Always create tries and test
echo Creating tries
python create_tries.py

echo Testing the model
python test_model.py

