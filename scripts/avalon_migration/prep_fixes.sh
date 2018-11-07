#!/bin/bash

# avalon:37702 avalon:37703 AvalonClip:1 Bookmark:960
# curl -vv --user $pass --limit-rate 45K sleep 1s --request DELETE --config data/derivative_urls.txt

usr="fedoraAdmin"
sp=":"
echo -n "Enter password:"
read -s pw
echo

# fedora="http://avalon.library.ualberta.ca:8080/fedora/objects/"
# urlend="/datastreams/sectionsMetadata"
# logmessage="?logMessage=Delete%20reference%20to%20empty%20MasterFile"

# curl -vv --user "$usr$sp$pw" -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:21435.xml' $fedora"avalon:21435"$urlend$logmessage
# curl -vv --user "$usr$sp$pw" -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:38370.xml' $fedora"avalon:38370"$urlend$logmessage
# curl -vv --user "$usr$sp$pw" -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:38594.xml' $fedora"avalon:38594"$urlend$logmessage
# curl -vv --user "$usr$sp$pw" -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:39253.xml' $fedora"avalon:39253"$urlend$logmessage
# curl -vv --user "$usr$sp$pw" -H "Content-Type: text/xml" --request PUT --data '@transformed_sectionsMetadata/avalon:19900.xml' $fedora"avalon:19900"$urlend$logmessage

curl -vv --user "$usr$sp$pw" -speed-limit 2 --speed-time 30 --limit-rate 45K sleep 1s --request DELETE --config data/phantom_masterfile-urls.txt 

curl -vv --user "$usr$sp$pw" -speed-limit 2 --speed-time 30 --limit-rate 45K sleep 1s --request DELETE --config data/derivative-urls.txt 