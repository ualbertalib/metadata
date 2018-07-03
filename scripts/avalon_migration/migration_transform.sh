#!/bin/bash

# definicion arreglo de directorios
# directories=("original_foxml" "original_mods" "transformed")

# # cada i es el nombre de el directorio en el loop
# for i in "${directories[@]}"
# do
#    : 
#    # si no existe el directorio llamado $1 crealo
# 	if [ ! -d "$i" ]; then
# 		echo "Creating directories 'original_foxml', 'original_mods', and 'transformed'"
# 		mkdir ./$i
# 		echo "Directories created"
# 	fi
# done

echo "Getting list of Avalon records"
echo -n "Enter password:"
read -s pass
echo
##### Use lines below when getting foxml #####
# python3 ./get_query.py
# python3 ./get_list.py
# echo "Getting Avalon records"
# xargs -I wget --limit-rate=45k --wait=10 --random-wait --remote-encoding=utf-8 --user fedoraAdmin --password $pass -O './original_foxml/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/objectXML' < avalon_pids.txt


##### Use when getting mods records #####
echo "Getting list of Avalon media objects"
wget -O 'MediaObject_pids.txt' 'http://avalon.library.ualberta.ca:8080/solr/avalon/select?q=has_model_ssim%3Ainfo%3Afedora%2Fafmodel%3AMediaObject&rows=1000000&fl=id&wt=csv&indent=true'

echo "Getting Avalon mods records"
xargs -i wget --limit-rate=45k --wait=10 --random-wait --remote-encoding=utf-8 --user fedoraAdmin --password $pass -O 'original_mods/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/datastreams/descMetadata/content' < MediaObject_pids.txt


echo "Transforming records"
#run xslt(s)
# cd ~/metadata
rm original_mods/id.xml
rm original_mods/.gitignore
java -jar saxon9he.jar -s:original_mods -o:transformed/ -xsl:mods_transform.xsl
echo "*
!.gitignore" > original_mods/.gitignore
echo "Transformation successful"

# echo "Committing to Avalon Migration repository"
#add, commit and push to repo working branch
#add something to check difference?
#pull request?

date=$(date +%Y%m%d)
name="-avalon-mods.zip"
filename=$date$name
#zip folder with today's date
zip -r $filename transformed
echo "Transformation complete, files compressed into" $filename