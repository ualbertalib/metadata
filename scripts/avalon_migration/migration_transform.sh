#!/bin/bash

echo "Getting list of Avalon records"
python3 ./get_query.py
python3 ./get_list.py

echo "Getting Avalon records"
echo -n "Enter password:"
read -s pass
echo
#get foxml
#xargs -i wget --limit-rate=200k --wait=5 --random-wait --user fedoraAdmin --password $pass -O './original_foxml/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/objectXML' < avalon_pids.txt
#get desc_metadata
xargs -i wget --limit-rate=45k --wait=10 --random-wait --user fedoraAdmin --password $pass -O './original_mods/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/datastreams/descMetadata/content' < MediaObject_pids.txt

echo "Transforming records"
#run xslt(s)

echo "Committing to Avalon Migration repository branch ______"
#add, commit and push to repo working branch
#add something to check difference?
#pull request?

echo "Transformation complete, compressing files"
#zip folder with today's date
echo "Done"