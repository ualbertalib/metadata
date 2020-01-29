#!/bin/sh
rm -f -r CanLink_env
git pull
mkdir CanLink_env
virtualenv CanLink_env
. CanLink_env/bin/activate
pip3 install -r requirements.txt 
chown www-data.www-data -R /home/ubuntu/CanLink/code/website/processing/


