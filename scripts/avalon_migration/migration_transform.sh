#!/bin/sh

# definicion arreglo de directorios
directories=("original_foxml" "original_mods" "transformed")

# cada i es el nombre de el directorio en el loop
for i in "${directories[@]}"
do
   : 
   # si no existe el directorio llamado $1 crealo
	if [ ! -d "$i" ]; then
		echo "Creating directories 'original_foxml', 'original_mods', and 'transformed'"
		mkdir ./$i
		echo "Directories created"
	fi
done

##### Use when getting foxml #####
# echo "Getting list of Avalon records"
# echo -n "Enter password:"
# read -s pass
# python3 ./get_query.py
# python3 ./get_list.py
# echo "Getting Avalon records"
# xargs -I wget --user fedoraAdmin --password $pass -O './original_foxml/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/objectXML' < avalon_pids.txt


##### Use when getting mods records #####
echo "Getting list of Avalon media objects"
wget -O 'MediaObject_pids.txt' 'http://avalon.library.ualberta.ca:8080/solr/avalon/select?q=has_model_ssim%3Ainfo%3Afedora%2Fafmodel%3AMediaObject&rows=1000000&fl=id&wt=csv&indent=true'
echo "Getting Avalon mods records"
xargs -i wget --limit-rate=45k --wait=10 --random-wait --remote-encoding=utf-8 --user fedoraAdmin --password $pass -O './original_mods/{}.xml' 'http://avalon.library.ualberta.ca:8080/fedora/objects/{}/datastreams/descMetadata/content' < MediaObject_pids.txt
rm id.xml

#remove and add gitignore or dummy file
#send example of visibility record

echo "Transforming records"
#run xslt(s)
cd ~/metadata
java -jar /opt/SaxonHE9-8-0-12J/saxon9he.jar -s:scripts/avalon_migration/original_mods -o:scripts/avalon_migration/transformed/ -xsl:scripts/avalon_migration/mods_transform.xsl 
echo "Transformation successful"

echo "Committing to Avalon Migration repository"
#add, commit and push to repo working branch
#add something to check difference?
#pull request?

echo "Transformation complete, compressing files"
#zip folder with today's date